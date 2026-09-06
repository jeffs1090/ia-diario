# IA Diário — Harness, Claude Code & Subagentes

Página pessoal com notícias, guia de harness, subagentes e prompts aplicados a desenvolvimento PL/SQL.

## Atualização diária

O workflow em `.github/workflows/daily-update.yml` executa todos os dias às 08:00 no horário de Fortaleza, busca feeds RSS/Atom e grava `data/news.json`. Também pode ser executado manualmente em GitHub Actions.

## Publicação

Ative GitHub Pages em Settings → Pages e escolha a fonte GitHub Actions. A página será publicada em:

`https://jeffs1090.github.io/ia-diario/`

## Rodar localmente

```bash
python3 scripts/fetch_news.py
python3 -m http.server 8000
```

Depois acesse `http://localhost:8000`.
