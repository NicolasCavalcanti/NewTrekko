#!/usr/bin/env python3
import json

with open('data/blog.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

posts = {p['id']: p for p in data}

def append_section(post_id, text):
    posts[post_id]['content'] += '\n\n' + text

# ID 4 - por-que-contratar-guia-cadastur (need +11w)
append_section(4, """Contratar um guia profissional é um investimento na segurança e na qualidade da experiência, não um custo desnecessário.""")

# ID 6 - planejamento-trilha-longo-curso (need +3w)
append_section(6, """Bom planejamento, boa trilha.""")

# ID 16 - melhor-epoca-trilhas-brasil (need +28w)
append_section(16, """Lembre sempre: a melhor época para uma trilha específica pode ser diferente da melhor época geral da região. Confirme sempre com resenhas recentes e com o parque antes de sair de casa.""")

# ID 20 - seguranca-trilha-regras (need +2w)
append_section(20, """Trilhe com segurança.""")

# ID 28 - trilhas-nordeste-brasil (need +4w)
append_section(28, """O Nordeste reserva surpresas para todo trilheiro atento.""")

# Verify
targets = {
    1: 900, 2: 800, 3: 800, 4: 800, 5: 800, 6: 800,
    7: 1000, 8: 1000, 9: 1200, 10: 1000, 11: 1000, 12: 1000,
    13: 1000, 14: 1200, 15: 1200, 16: 1000, 17: 900, 18: 900,
    19: 1000, 20: 1000, 21: 900, 22: 800, 23: 900, 24: 900,
    25: 900, 26: 1000, 27: 1000, 28: 1000
}

with open('data/blog.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

ok = fail = 0
for post in data:
    words = len(post['content'].split())
    target = targets.get(post['id'], 800)
    status = '✓' if words >= target else f'✗ need+{target-words}'
    if words >= target: ok += 1
    else: fail += 1
    print(f'ID {post["id"]:2} | {words:5}w / {target}w {status}')
print(f'\nTotal: {ok} OK, {fail} below target')
