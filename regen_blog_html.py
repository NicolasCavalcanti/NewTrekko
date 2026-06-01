#!/usr/bin/env python3
"""
Regenerate blog post article content from data/blog.json.
Converts markdown-style content to HTML and injects into existing HTML shells.
"""
import json, os, re

BLOG_DIR = "blog"

with open("data/blog.json", encoding="utf-8") as f:
    posts = json.load(f)

def md_to_html(text):
    """Convert simple markdown to HTML for blog articles."""
    lines = text.split("\n")
    html_lines = []
    in_ul = False
    in_table = False
    buffer = []

    def flush_p():
        nonlocal buffer
        if buffer:
            para = " ".join(buffer).strip()
            if para:
                html_lines.append(f"    <p>{para}</p>")
            buffer = []

    def flush_table():
        nonlocal in_table
        in_table = False

    for line in lines:
        stripped = line.strip()

        # Table row
        if stripped.startswith("|") and stripped.endswith("|"):
            if buffer:
                flush_p()
            if not in_table:
                in_table = True
                html_lines.append('    <div class="table-wrap"><table><tbody>')
            # Skip separator rows
            if re.match(r'^\|[-| :]+\|$', stripped):
                continue
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            row = "".join(f"<td>{c}</td>" for c in cells)
            html_lines.append(f"      <tr>{row}</tr>")
            continue
        else:
            if in_table:
                html_lines.append("    </tbody></table></div>")
                in_table = False

        # Headings
        if stripped.startswith("## "):
            if buffer:
                flush_p()
            if in_ul:
                html_lines.append("    </ul>")
                in_ul = False
            heading = stripped[3:].strip()
            heading = apply_inline(heading)
            html_lines.append(f"    <h2>{heading}</h2>")
            continue

        if stripped.startswith("### "):
            if buffer:
                flush_p()
            if in_ul:
                html_lines.append("    </ul>")
                in_ul = False
            heading = stripped[4:].strip()
            heading = apply_inline(heading)
            html_lines.append(f"    <h3>{heading}</h3>")
            continue

        # List items
        if stripped.startswith("- ") or stripped.startswith("* "):
            if buffer:
                flush_p()
            if not in_ul:
                html_lines.append("    <ul>")
                in_ul = True
            item = stripped[2:].strip()
            item = apply_inline(item)
            html_lines.append(f"      <li>{item}</li>")
            continue

        # Numbered list
        num_match = re.match(r'^(\d+)\.\s+(.+)$', stripped)
        if num_match:
            if buffer:
                flush_p()
            if in_ul:
                html_lines.append("    </ul>")
                in_ul = False
            item = apply_inline(num_match.group(2))
            html_lines.append(f"      <li>{item}</li>")
            # Start ol if not already (simple: just use li outside ul)
            continue

        # Empty line
        if not stripped:
            if buffer:
                flush_p()
            if in_ul:
                html_lines.append("    </ul>")
                in_ul = False
            continue

        # Normal text — accumulate into paragraph
        if in_ul:
            html_lines.append("    </ul>")
            in_ul = False
        buffer.append(apply_inline(stripped))

    if buffer:
        flush_p()
    if in_ul:
        html_lines.append("    </ul>")
    if in_table:
        html_lines.append("    </tbody></table></div>")

    return "\n".join(html_lines)


def apply_inline(text):
    """Apply inline markdown: bold, links, code."""
    # [text](/url) -> <a href="/url">text</a>
    text = re.sub(r'\[([^\]]+)\]\((/[^)]+)\)', r'<a href="\2">\1</a>', text)
    # **text** -> <strong>text</strong>
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # `code` -> <code>code</code>
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # emoji/special chars passthrough
    return text


def inject_article(html_path, new_article_html):
    """Replace the <article class="post-body">...</article> section."""
    with open(html_path, encoding="utf-8") as f:
        content = f.read()

    # Find article start and end
    start_tag = '<article class="post-body">'
    end_tag = "</article>"

    start_idx = content.find(start_tag)
    if start_idx == -1:
        print(f"  WARNING: no <article> found in {html_path}")
        return False

    end_idx = content.find(end_tag, start_idx)
    if end_idx == -1:
        print(f"  WARNING: no </article> found in {html_path}")
        return False

    new_section = f"{start_tag}\n{new_article_html}\n  {end_tag}"
    new_content = content[:start_idx] + new_section + content[end_idx + len(end_tag):]

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


def count_h2(html_path):
    with open(html_path, encoding="utf-8") as f:
        content = f.read()
    return len(re.findall(r'<h2', content))


def count_internal_links(html_path):
    with open(html_path, encoding="utf-8") as f:
        content = f.read()
    return len(re.findall(r'href="/(blog|trilha)/', content))


ok = 0
fail = 0
for post in posts:
    slug = post["slug"]
    html_path = os.path.join(BLOG_DIR, slug, "index.html")

    if not os.path.exists(html_path):
        print(f"SKIP {slug} — HTML not found")
        continue

    article_html = md_to_html(post["content"])
    success = inject_article(html_path, article_html)

    if success:
        h2 = count_h2(html_path)
        links = count_internal_links(html_path)
        words = len(post["content"].split())
        status = "✓" if (h2 >= 5 and links >= 3 and words >= 800) else f"⚠ h2={h2} links={links} words={words}"
        print(f"  {status} {slug}")
        if h2 >= 5 and links >= 3 and words >= 800:
            ok += 1
        else:
            fail += 1
    else:
        fail += 1

print(f"\nDone: {ok} posts fully OK, {fail} need attention")
