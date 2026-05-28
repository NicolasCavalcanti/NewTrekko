#!/usr/bin/env python3
"""Update all HTML files to replace emoji/text avatars with real img tags."""

import re
import os
import glob

BASE = "/home/user/NewTrekko"

AUTHOR_SLUGS = {
    "Rafael Dias":      "rafael-dias",
    "Marcos Rodrigues": "marcos-rodrigues",
    "Letícia Campos":   "leticia-campos",
    "Leticia Campos":   "leticia-campos",
}

# ─── 1. Update author profile pages ─────────────────────────────────────────

AUTHOR_PROFILES = [
    {
        "path":    f"{BASE}/autores/rafael-dias/index.html",
        "slug":    "rafael-dias",
        "name":    "Rafael Dias",
        "initials":"RD",
    },
    {
        "path":    f"{BASE}/autores/marcos-rodrigues/index.html",
        "slug":    "marcos-rodrigues",
        "name":    "Marcos Rodrigues",
        "initials":"MR",
    },
    {
        "path":    f"{BASE}/autores/leticia-campos/index.html",
        "slug":    "leticia-campos",
        "name":    "Letícia Campos",
        "initials":"LC",
    },
]


def update_author_profile(info: dict) -> None:
    path = info["path"]
    with open(path, encoding="utf-8") as f:
        html = f.read()

    slug = info["slug"]
    name = info["name"]
    initials = info["initials"]

    # 1a. Replace <div class="avatar" …>INITIALS</div>
    html = html.replace(
        f'<div class="avatar" aria-hidden="true">{initials}</div>',
        f'<img src="/images/autores/{slug}-avatar.jpg" alt="Foto de {name}" '
        f'class="avatar" width="96" height="96" loading="eager" decoding="async">',
    )

    # 1b. Update CSS .avatar — remove flex/text props, add object-fit
    html = re.sub(
        r'(\.avatar\s*\{[^}]*?)(display:\s*flex;[^}]*?align-items:\s*center;[^}]*?justify-content:\s*center;[^}]*?font-size:\s*2rem;[^}]*?font-weight:\s*700;)',
        r'\1object-fit: cover;',
        html,
        flags=re.DOTALL,
    )
    # Simpler targeted replacement for minified CSS
    html = re.sub(
        r'(\.avatar\{[^}]*?)display:flex;align-items:center;justify-content:center;font-size:2rem;font-weight:700;',
        r'\1object-fit:cover;',
        html,
    )
    # Non-minified variant
    html = re.sub(
        r'(\.avatar\s*\{[^}]*?)display:\s*flex;\s*align-items:\s*center;\s*justify-content:\s*center;\s*font-size:\s*2rem;\s*font-weight:\s*700;',
        r'\1object-fit: cover;',
        html,
        flags=re.DOTALL,
    )

    # 1c. Add "image" to Schema.org Person (if not already present)
    if '"image"' not in html:
        image_prop = f'    "image": "https://trekko.com.br/images/autores/{slug}-avatar.jpg",\n'
        # Insert after the "url" line
        html = re.sub(
            r'("url"\s*:\s*"https://trekko\.com\.br/autores/[^"]+"\s*,)',
            r'\1\n' + image_prop.rstrip('\n'),
            html,
        )

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Updated author profile: {path}")


# ─── 2. Update blog articles ──────────────────────────────────────────────────

def get_author_from_html(html: str) -> str | None:
    """Extract author name from the author-box section."""
    m = re.search(
        r'<div class="author-avatar">.*?</div>\s*<div class="author-info">\s*<h4>([^<]+)</h4>',
        html,
        re.DOTALL,
    )
    if m:
        return m.group(1).strip()
    # Fallback: any h4 inside author-box
    m2 = re.search(r'class="author-box".*?<h4>([^<]+)</h4>', html, re.DOTALL)
    if m2:
        return m2.group(1).strip()
    return None


def update_blog_article(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        html = f.read()

    if '<div class="author-avatar">' not in html:
        return

    author_name = get_author_from_html(html)
    if not author_name:
        print(f"  WARN: could not detect author in {path}")
        return

    slug = AUTHOR_SLUGS.get(author_name)
    if not slug:
        print(f"  WARN: unknown author '{author_name}' in {path}")
        return

    # 2a. Replace emoji div with img (handles any emoji content)
    html = re.sub(
        r'<div class="author-avatar">[^<]*</div>',
        f'<img src="/images/autores/{slug}-avatar.jpg" '
        f'alt="Foto de {author_name}" class="author-avatar" '
        f'width="56" height="56" loading="lazy" decoding="async">',
        html,
    )

    # 2b. Fix CSS .author-avatar — replace emoji-specific props with img-friendly ones
    # Minified form
    html = re.sub(
        r'(\.author-avatar\{[^}]*?)display:flex;align-items:center;justify-content:center;font-size:1\.5rem;',
        r'\1object-fit:cover;',
        html,
    )
    # Non-minified
    html = re.sub(
        r'(\.author-avatar\s*\{[^}]*?)display:\s*flex;\s*align-items:\s*center;\s*justify-content:\s*center;\s*font-size:\s*1\.5rem;',
        r'\1object-fit: cover;',
        html,
        flags=re.DOTALL,
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Updated blog article: {os.path.basename(os.path.dirname(path))}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=== Updating author profile pages ===")
    for info in AUTHOR_PROFILES:
        update_author_profile(info)

    print("\n=== Updating blog articles ===")
    articles = glob.glob(f"{BASE}/blog/*/index.html")
    articles.sort()
    for article in articles:
        update_blog_article(article)

    print("\nDone.")


if __name__ == "__main__":
    main()
