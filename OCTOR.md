# Laya na Octor

Fork Apache-2.0 de [NandhaKishorM/laya](https://github.com/NandhaKishorM/laya) — motor System One (decisões tipadas, sem gerar texto).

## Produção (sp1-sd-octor-1)

| | |
|---|---|
| App dir | `/home/ubuntu/octor/apps/laya/` |
| Compose | `docker-compose.yml` (no host como `docker-compose.yml`) |
| Imagem | `ghcr.io/0ctor/laya` |
| Container | `octor-laya` |
| Interno | `http://octor-laya:8000/v1/systemone` |
| VPN | `http://10.8.0.1:8343/health` |
| Device | CPU (`LAYA_DEVICE=cpu`) |
| Checkpoint | `multilingual` (PT-BR) |

Deploy: push em `main` → deploy-hook `0ctor/laya` (`kind: single`).

## Consumidores

- **web-ticket** — prioridade automática na criação (`LAYA_URL`)
- **platform-hosting** — engine `laya` na aba IA (sidecar por site)

## Smoke

```bash
curl -fsS http://10.8.0.1:8343/health
curl -fsS http://10.8.0.1:8343/v1/systemone \
  -H 'content-type: application/json' \
  -d '{"state":{"body":"Sistema fora do ar, clientes sem acesso"},"questions":{"priority":{"type":"choice","instructions":"Prioridade do ticket","criteria":{"URGENT":"fora do ar, dados, segurança","HIGH":"bloqueio parcial","MEDIUM":"dúvida operacional","LOW":"melhoria, cosmético"}}}}'
```

## Volume

No host, o cache HF precisa ser UID 10001 (usuário `laya` na imagem):

```bash
sudo mkdir -p /home/ubuntu/octor/volumes/laya/hf-cache
sudo chown -R 10001:10001 /home/ubuntu/octor/volumes/laya
```
