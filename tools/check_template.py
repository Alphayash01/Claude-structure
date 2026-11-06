"""Validate template/ against the spec data in template_spec.py.

Usage:
  python tools/check_template.py               # full check of template/
  python tools/check_template.py --files A.md  # per-file checks only
  python tools/check_template.py --usage       # which files use each placeholder
"""
import argparse
import posixpath
import re
import sys
from pathlib import Path

from template_spec import (
    ALLOWED_MERMAID_TYPES, DENYLIST, FILES, GUIDE, PURPOSE_PREFIX, REGISTRY,
    REPO_LINK_PREFIX, REQUIRED_FILES, FileSpec,
)

DEFAULT_ROOT = Path(__file__).resolve().parent.parent / "template"
EXTERNAL = ("http://", "https://", "mailto:")

FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})\s*([\w-]*)")
PLACEHOLDER_RE = re.compile(r"\{\{([A-Z_]+)\}\}")
INLINE_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
REF_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
FRONT_KEY_RE = re.compile(r"^([a-z_-]+):\s*(.*)$")
ADD_RE = re.compile(r"<!--\s*ADD\b")
ADD_SLOT_RE = re.compile(r"<!--\s*ADD:")
DENY_RES = [(term, re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)) for term in DENYLIST]


def ph(name):
    return "{{" + name + "}}"


def parse(text):
    """Return (line_no, line, fence_lang, kind) rows; kind is text/open/code/close."""
    rows, fence = [], None
    for n, line in enumerate(text.splitlines(), 1):
        m = FENCE_RE.match(line)
        if fence is None and m:
            fence = (m.group(1)[0], len(m.group(1)), m.group(2).lower())
            rows.append((n, line, fence[2], "open"))
        elif fence and m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] and not m.group(2):
            rows.append((n, line, fence[2], "close"))
            fence = None
        else:
            rows.append((n, line, fence[2] if fence else None, "code" if fence else "text"))
    return rows


def text_lines(rows):
    return [(n, line) for n, line, _, kind in rows if kind == "text"]


def slugify(heading):
    return re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")


def heading_slugs(text):
    counts, slugs = {}, set()
    for _, line in text_lines(parse(text)):
        m = HEADING_RE.match(line)
        if not m:
            continue
        slug = slugify(m.group(1))
        if slug in counts:
            counts[slug] += 1
            slugs.add(f"{slug}-{counts[slug]}")
        else:
            counts[slug] = 0
            slugs.add(slug)
    return slugs


def check_placeholders(rel, rows):
    errors = []
    for n, line, _, _ in rows:
        start = line.find("{{")
        while start != -1:
            end = line.find("}}", start + 2)
            token = line[start:end + 2] if end != -1 else line[start:]
            m = PLACEHOLDER_RE.fullmatch(token)
            if not m:
                errors.append(f"{rel}:{n}: malformed placeholder {token!r}")
            elif m.group(1) not in REGISTRY:
                errors.append(f"{rel}:{n}: unregistered placeholder {token}")
            start = line.find("{{", start + len(token)) if end != -1 else -1
    return errors


def check_comments(rel, rows):
    # Blank out fenced lines first: a Mermaid arrow (-->) must not count as a comment close.
    text = "\n".join(line if kind == "text" else "" for _, line, _, kind in rows)
    pos = 0
    while (start := text.find("<!--", pos)) != -1:
        end = text.find("-->", start + 4)
        nxt = text.find("<!--", start + 4)
        if end == -1 or (nxt != -1 and nxt < end):
            return [f"{rel}:{text.count(chr(10), 0, start) + 1}: unclosed HTML comment"]
        pos = end + 3
    return []


def check_code(rel, rows):
    errors, pending = [], None
    for n, line, lang, kind in rows:
        if kind == "open":
            pending = n if lang == "mermaid" else None
        elif kind == "code":
            if ADD_RE.search(line):
                errors.append(f"{rel}:{n}: ADD marker inside code block")
            if lang == "mermaid":
                if "{{" in line or "ADD:" in line:
                    errors.append(f"{rel}:{n}: marker inside mermaid block")
                if pending and line.strip():
                    if not line.strip().startswith(ALLOWED_MERMAID_TYPES):
                        errors.append(f"{rel}:{n}: unsupported mermaid diagram type")
                    pending = None
        elif kind == "close" and pending:
            errors.append(f"{rel}:{pending}: unsupported mermaid diagram type")
            pending = None
    return errors


def link_targets(rows):
    for n, line in text_lines(rows):
        visible = INLINE_CODE_RE.sub("", line)
        for m in INLINE_LINK_RE.finditer(visible):
            yield n, m.group(1)
        m = REF_LINK_RE.match(visible)
        if m:
            yield n, m.group(1)


def resolve(rel, target):
    """Return (kind, path, anchor) with path posix and root-relative, or None to skip."""
    if target.startswith(EXTERNAL):
        return None
    if target.startswith(REPO_LINK_PREFIX):
        kind, raw, base = "repo", target[len(REPO_LINK_PREFIX):], ""
    elif target.startswith("{{"):
        return None
    elif target.startswith("/") and not target.startswith("//"):
        # Root-relative: GitHub resolves it from the repo root, so it survives a file move.
        kind, raw, base = "root", target[1:], ""
    else:
        kind, raw, base = "rel", target, posixpath.dirname(rel)
    path, _, anchor = raw.partition("#")
    resolved = posixpath.normpath(posixpath.join(base, path)) if path else rel
    return kind, resolved, anchor


def check_links(root, rel, rows, spec, strict):
    # Exact-case paths: Windows file lookups ignore case, GitHub links do not.
    existing = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
    errors, linked = [], set()
    for n, target in link_targets(rows):
        resolved = resolve(rel, target)
        if resolved is None:
            continue
        kind, path, anchor = resolved
        linked.add(path)
        where = f"{rel}:{n}:"
        if path == ".." or path.startswith(("../", "/")):
            errors.append(f"{where} link escapes template: {target}")
        elif rel.startswith(".github/") and kind in ("rel", "root") and path != rel:
            errors.append(f"{where} relative link in .github form: {target}")
        elif path == GUIDE and rel != GUIDE:
            errors.append(f"{where} link to TEMPLATE_GUIDE.md")
        elif path not in existing:
            if strict or path not in REQUIRED_FILES:
                errors.append(f"{where} broken link: {target}")
        elif anchor and path.endswith(".md"):
            if anchor not in heading_slugs((root / path).read_text(encoding="utf-8")):
                errors.append(f"{where} broken anchor: {target}")
    for required in spec.links:
        if required not in linked:
            errors.append(f"{rel}:0: missing required link {required}")
    return errors


def check_headings(rel, rows, spec):
    found = [line[3:].strip() for _, line in text_lines(rows) if line.startswith("## ")]
    errors, pos = [], 0
    for wanted in spec.headings:
        try:
            pos = found.index(wanted, pos) + 1
        except ValueError:
            errors.append(f"{rel}:0: missing or out-of-order heading '## {wanted}'")
    return errors


def check_purpose(rel, rows):
    lines = text_lines(rows)
    for i, (_, line) in enumerate(lines):
        if line.startswith("# "):
            rest = [text for _, text in lines[i + 1:] if text.strip()]
            if rest and rest[0].startswith(PURPOSE_PREFIX):
                return []
            break
    return [f"{rel}:0: missing purpose line"]


def check_denylist(rel, rows):
    errors = []
    for term, pattern in DENY_RES:
        hit = next((n for n, line, _, _ in rows if pattern.search(line)), None)
        if hit is not None:
            errors.append(f"{rel}:{hit}: stack-specific term '{term}'")
    return errors


def check_front_matter(rel, lines, required):
    invalid = [f"{rel}:1: invalid front matter"]
    if not lines or lines[0].strip() != "---":
        return invalid
    close = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if close is None:
        return invalid
    keys = {}
    for line in lines[1:close]:
        if not line.strip():
            continue
        m = FRONT_KEY_RE.match(line)
        if not m:
            return invalid
        keys[m.group(1)] = m.group(2).strip().strip("\"'")
    if not all(keys.get(key) for key in required):
        return invalid
    if rel.startswith(".claude/skills/") and keys.get("disable-model-invocation") != "true":
        return [f"{rel}:1: skill must set disable-model-invocation: true (modes run only when typed)"]
    return []


def check_file(root, rel, spec, strict_links=True):
    path = root / rel
    if not path.is_file():
        return [f"{rel}:0: missing file"]
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    rows = parse(text)
    errors = (check_placeholders(rel, rows) + check_comments(rel, rows) + check_code(rel, rows)
              + check_links(root, rel, rows, spec, strict_links) + check_headings(rel, rows, spec))
    errors += [f"{rel}:{n}: ADD marker without colon (the unfinished-work search can't find it)"
               for n, line in text_lines(rows)
               if len(ADD_RE.findall(line)) > len(ADD_SLOT_RE.findall(line))]
    if spec.purpose_line:
        errors += check_purpose(rel, rows)
    if spec.add_slot and not any(ADD_SLOT_RE.search(line) for _, line in text_lines(rows)):
        errors.append(f"{rel}:0: missing ADD slot")
    if len(lines) > spec.max_lines:
        errors.append(f"{rel}:0: exceeds {spec.max_lines} lines ({len(lines)})")
    errors += check_denylist(rel, rows)
    if rel.startswith(".github/ISSUE_TEMPLATE/"):
        errors += check_front_matter(rel, lines, ("name", "about"))
    if rel.startswith(".claude/skills/") and rel.endswith("/SKILL.md"):
        errors += check_front_matter(rel, lines, ("name", "description"))
    return errors


def placeholder_usage(root):
    usage = {name: [] for name in REGISTRY}
    for rel in REQUIRED_FILES:
        path = root / rel
        if rel == GUIDE or not path.is_file():
            continue
        found = set(PLACEHOLDER_RE.findall(path.read_text(encoding="utf-8")))
        for name, files in usage.items():
            if name in found:
                files.append(rel)
    return usage


def check_all(root):
    errors = []
    for rel in REQUIRED_FILES:
        errors += check_file(root, rel, FILES.get(rel, FileSpec()))
    if root.is_dir():
        for path in sorted(root.rglob("*")):
            rel = path.relative_to(root).as_posix()
            if path.is_file() and rel not in REQUIRED_FILES:
                errors.append(f"{rel}:0: unexpected file")
    usage = placeholder_usage(root)
    for name, files in usage.items():
        if not files:
            errors.append(f"(registry):0: registry placeholder {ph(name)} unused")
    guide = root / GUIDE
    if guide.is_file():
        text = guide.read_text(encoding="utf-8")
        errors += [f"{GUIDE}:0: TEMPLATE_GUIDE.md does not list {ph(name)}"
                   for name in REGISTRY if ph(name) not in text]
        rows = [line for line in text.splitlines() if line.startswith("|")]
        for name, files in usage.items():
            # The registry row is the one whose first cell is the placeholder itself.
            cells = [[c.strip() for c in line.strip().strip("|").split("|")] for line in rows]
            row = next((c for c in cells if c[0].strip("`") == ph(name)), None)
            if row is not None:
                listed = {item.strip() for item in row[-1].split(",")}
                errors += [f"{GUIDE}:0: TEMPLATE_GUIDE.md row for {ph(name)} misses {rel}"
                           for rel in files if rel not in listed]
    return errors


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Validate the docs template against its spec.")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--files", nargs="+", metavar="REL")
    mode.add_argument("--usage", action="store_true")
    args = parser.parse_args(argv)

    if args.usage:
        for name, files in placeholder_usage(args.root).items():
            print(f"{ph(name)}: {', '.join(files) or '(unused)'}")
        return 0
    if args.files:
        rels = [rel.replace("\\", "/") for rel in args.files]
        errors = [e for rel in rels
                  for e in check_file(args.root, rel, FILES.get(rel, FileSpec()), strict_links=False)]
    else:
        rels = REQUIRED_FILES
        errors = check_all(args.root)
    for error in errors:
        print(error)
    if errors:
        print(f"{len(errors)} error(s)")
        return 1
    print(f"OK: {len(rels)} file(s) checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
