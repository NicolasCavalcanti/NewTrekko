#!/usr/bin/env python3
"""Update blog post HTML files: add category level to visual breadcrumb and JSON-LD schema."""
import json, os, re

BLOG_DIR = "blog"
BASE_URL = "https://trekko.com.br"

CATEGORY_LABELS = {
    "equipamentos":           "Equipamentos",
    "conservacao-ambiental":  "Conservação Ambiental",
    "planejamento-seguranca": "Planejamento e Segurança",
    "guias-praticos":         "Guias Práticos",
    "trilhas-destinos":       "Trilhas e Destinos",
}

with open("data/blog.json", encoding="utf-8") as f:
    posts = json.load(f)

slug_to_category = {p["slug"]: p["category"] for p in posts}
slug_to_title = {p["slug"]: p["title"] for p in posts}

ok = fail = 0

for slug, category in slug_to_category.items():
    html_path = os.path.join(BLOG_DIR, slug, "index.html")
    if not os.path.exists(html_path):
        print(f"SKIP {slug} — not found")
        continue

    with open(html_path, encoding="utf-8") as f:
        content = f.read()

    cat_label = CATEGORY_LABELS.get(category, category)
    cat_url = f"/blog/{category}"
    post_title = slug_to_title.get(slug, slug)
    post_url = f"{BASE_URL}/blog/{slug}"

    # --- Update visual breadcrumb ---
    # Match: <nav class="breadcrumb"...>...<li>...<a href="/blog">Blog</a>...</li>...<li>...<span...>Title</span>...</li>...(optional extra)</ol>
    # Replace the nav block with a 4-level version
    old_nav_pat = r'<nav class="breadcrumb"[^>]*>.*?</nav>'
    new_nav = (
        f'<nav class="breadcrumb" aria-label="Navegação estrutural">\n'
        f'<div class="container"><ol>\n'
        f'  <li><a href="/">Trekko</a></li>\n'
        f'  <li><a href="/blog">Blog</a></li>\n'
        f'  <li><a href="{cat_url}">{cat_label}</a></li>\n'
        f'  <li><span aria-current="page">{post_title}</span></li>\n'
        f'</ol></div>\n'
        f'</nav>'
    )
    content_new, n = re.subn(old_nav_pat, new_nav, content, flags=re.DOTALL)
    if n == 0:
        print(f"  WARN no breadcrumb nav found: {slug}")
        fail += 1
        continue

    # --- Update JSON-LD BreadcrumbList ---
    # Find existing BreadcrumbList and replace itemListElement
    def replace_breadcrumb_jsonld(m):
        old_json_str = m.group(0)
        # Find the script tag containing BreadcrumbList
        try:
            # Extract JSON from script tag
            json_match = re.search(r'\{.*\}', old_json_str, re.DOTALL)
            if not json_match:
                return old_json_str
            data = json.loads(json_match.group(0))
            graph = data.get("@graph", [])
            for node in graph:
                if node.get("@type") == "BreadcrumbList":
                    node["itemListElement"] = [
                        {"@type": "ListItem", "position": 1, "name": "Trekko", "item": BASE_URL},
                        {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE_URL}/blog"},
                        {"@type": "ListItem", "position": 3, "name": cat_label, "item": f"{BASE_URL}{cat_url}"},
                        {"@type": "ListItem", "position": 4, "name": post_title, "item": post_url},
                    ]
                    break
            new_json = json.dumps(data, ensure_ascii=False, indent=" ")
            return old_json_str[:old_json_str.index('{')] + new_json + old_json_str[old_json_str.rindex('}')+1:]
        except Exception as e:
            print(f"  WARN JSON-LD update failed for {slug}: {e}")
            return old_json_str

    script_pat = r'<script type="application/ld\+json">.*?</script>'
    content_new = re.sub(script_pat, replace_breadcrumb_jsonld, content_new, flags=re.DOTALL)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content_new)

    print(f"  ✓ {slug} [{cat_label}]")
    ok += 1

print(f"\nDone: {ok} updated, {fail} failed")
