# AGENTS.md

Context for AI coding assistants (Claude Code, Codex, Cursor, Copilot, Gemini CLI) working in this repository.

**Laya** is a fast, local, on-device decision engine. These rules mirror [CONTRIBUTING.md](CONTRIBUTING.md); the assistant-facing summary lives here because coding agents read this file automatically.

## Do NOT

- Introduce a dependency on a hosted service or external API. Features must run in the user's own process or on their own hardware; a feature that only works against a hosted backend belongs in a separate integration, not here.
- Change the public API without updating `tests/test_hooks_api.py` in the same pull request — that suite is the API contract.
- Skip the CI gates before declaring a change done:

  ```bash
  ruff check laya/ --select=E9,F63,F7,F82,F401,F811 --line-length=120
  python -m compileall -q laya/ tests/
  ```

- Reformat files wholesale, reorder imports, or "modernize" surrounding code. Match the style of the file being edited; a diff full of formatting noise gets a change rejected.
- Commit secrets, tokens, or large binary files.
- Open pull requests in a language other than English. The project is triaged in English.
- Invent conventions. Use conventional commit prefixes matching the history (`feat(agent):`, `fix(router):`, `perf(common):`, `docs(hooks):`, `test(batch):`), and keep one logical change per commit.

## Where to look

| Editing | Read | Check |
|---|---|---|
| `laya/` core | — | plain script suites: `python tests/test_router.py`, `tests/test_criteria.py`, `tests/test_hooks.py`, `tests/test_hooks_api.py` |
| server path | `tests/test_serve.py` | `python -m pytest tests/test_serve.py` (skips when the `serve` extra is missing) |
| ONNX path | `tests/test_onnx.py` | `python -m pytest tests/test_onnx.py` (skips when the `onnx` extra is missing) |
| fast/local paths | `tests/test_fast.py`, `tests/test_local_e2e.py`, `tests/test_mcp_local_e2e.py` | need CUDA or checkpoints under `~/laya_models`; skipped otherwise |
| docs, docstrings in `laya/` | `docs/`, `docs/.nav.yml` for page order | `pip install -r requirements-docs.txt`, then `zensical build --strict --clean` with no `griffe:` lines in the output |

Optional extras are declared in `pyproject.toml` (`serve`, `fast`, `onnx`, `langchain`, `langgraph`); install only what the change needs.

## Pull requests

- Rebase onto the latest `main` so the diff is only your change.
- Keep it focused; split unrelated work into another PR.
- If a change moves numbers, report the before and after. The maintainer verifies decisions against real checkpoints, and measured deltas (probability changes, latency, memory) are what gets a change merged.
- Leave one runnable check behind for non-trivial logic; an assert-based script is enough.

## Padrões da org (obrigatórios)

<!-- octor-ecosystem:start -->
> Vale para **qualquer** assistente e IDE (**Cursor**, **OpenCode**, **Codex**, **VS Code**/Copilot, Claude, ChatGPT, etc.) e para humanos.
> **Fonte portátil (igual para todo o time):** este `AGENTS.md` — o bloco abaixo. Pastas de IDE (`.cursor/`, `.opencode/`, `.codex/`, …) são **opcionais** e **não** podem contradizer nem substituir este bloco.
> Detalhe canônico: portal [`0ctor/backstage`](https://github.com/0ctor/backstage) (`agents-ecosystem-block.md` + docs).

1. **Git Flow:** proibido editar/push em `main`. `feature/*` ← `dev` → PR→`dev` → PR `dev`→`main` (deploy **só** em `main`). **Hotfix absoluto** (bug que precisa ir já a `main`): `fix/*` ← `main` → PR→`main` + PR/cherry-pick do mesmo fix em `dev` — proibido acelerar via `dev`+promote. Apagar branch após merge (local; remota via setting GitHub **`delete_branch_on_merge`** em todos os repos — script [ensure_delete_branch_on_merge.py](https://github.com/0ctor/backstage/blob/main/scripts/ensure_delete_branch_on_merge.py)). **Proibido** usar `git stash` como depósito de WIP/funcionalidade — código escrito vive em `feature/*`/`fix/*` com commit (troca de tarefa: commit ou worktree). Doc: [git-flow.md](https://github.com/0ctor/backstage/blob/main/git-flow.md).
2. **Schema (ADR-005):** DDL/migrations **somente** em [`platform-database`](https://github.com/0ctor/platform-database). Proibido `Schema::` / `dbforge` / pastas `migrations/` de schema em outros apps.
3. **Auth / SSO:** sempre [`web-auth`](https://github.com/0ctor/web-auth) (`auth.octor.com.br`). Não reinventar portal de login.
4. **Segredos:** só `.env` / Vault — nunca commit. GitHub Actions: **Variables** para não-sensível (URLs, portas); **Secrets** para credenciais.
5. **Loki:** backend `LOKI_PUSH_*` + `LOKI_JOB` no `.env` da API; frontend via `POST /v1/errors/report` (ou `/v2/...`) na API — **proibido** senha Loki em `NEXT_PUBLIC_*`.
6. **Constraints:** sem hostname/IP de produção hardcoded no código de app; sem gates absolutos de PRD no código (usar env / feature flag / config de deploy — não `if (host===…)`); **sem** rotas HTTP `OPTIONS` (CORS no gateway); soft delete `deleted_at` + `deleted_by`.
7. **Deploy:** push/`main` → `platform-deploy-hook` → GHCR `ghcr.io/0ctor/<app>:<sha>` → compose em [`sp1-sd-octor-1`](https://github.com/0ctor/sp1-sd-octor-1) (`apps/<serviço>/`).
8. **Testes (mínimo):** unitários obrigatórios; CI `lint → typecheck → test → build` em **`dev` e `main`**. APIs: integração; apps de usuário: E2E/smoke (SSO + fluxo principal + anti–tela branca). Metas: coverage ≥ 80%; mutation ≥ 80% quando configurado. Canônico: [testing-strategy.md](https://github.com/0ctor/backstage/blob/main/testing-strategy.md).
9. **Agente:** username **Alfred** (nunca “Mordomo Octor”).
10. **Stack:** respeitar a do repo — não trocar framework sem decisão explícita.
11. **Mapa cross-app:** [`catalog.yaml`](https://github.com/0ctor/backstage/blob/main/catalog.yaml) / [catalog-rede](https://github.com/0ctor/backstage/blob/main/catalog-rede.json). Mudança de contrato / portas / API / arquitetura → atualizar o Backstage ([docs-sync.md](https://github.com/0ctor/backstage/blob/main/docs-sync.md)). UX → sync [`platform-help`](https://github.com/0ctor/platform-help). App novo: [novo-app-octor.md](https://github.com/0ctor/backstage/blob/main/novo-app-octor.md).
12. **Dependentes de dados:** ao mudar schema/contrato/semântica de tabelas, avaliar e atualizar [`web-migration`](https://github.com/0ctor/web-migration), [`web-export`](https://github.com/0ctor/web-export) e demais consumidores do mesmo dado (ex. `web-database`, `platform-legacy`, apps do domínio) — ou registrar explicitamente “sem impacto”. Detalhe: [cross-app-data-dependents-sync](https://github.com/0ctor/backstage/blob/main/.cursor/rules/cross-app-data-dependents-sync.mdc).
13. **Datas / fusos:** instantes de auditoria (`created_at`/`updated_at`/`deleted_at`) em **UTC** no backend; API com ISO `Z`/offset (naive legado = UTC). UI no fuso do operador; se mostrar UTC, sufixo ` UTC`. Proibido `timeZone="UTC"` no next-intl sem rótulo e `Local::now()`/`date()` do servidor para auditoria. Agenda/slots/vencimentos = civil (helpers separados). Canônico: [timezone-datetime.md](https://github.com/0ctor/backstage/blob/main/timezone-datetime.md).
14. **Skills / agentes (org):** política = este bloco. Procedimentos repetíveis = [`agent-skills/`](https://github.com/0ctor/backstage/tree/main/agent-skills) (`octor-pr-audit`, `octor-github-resolution`, `octor-promote-check`) — instalar com [`install-agent-skills.py`](https://github.com/0ctor/backstage/blob/main/scripts/install-agent-skills.py). Preferência pessoal de IDE **não** entra no canônico. Doc: [agent-skills.md](https://github.com/0ctor/backstage/blob/main/agent-skills.md).
<!-- octor-ecosystem:end -->

