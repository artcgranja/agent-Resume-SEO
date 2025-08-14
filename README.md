## Agent Resume SEO

Assistente que reescreve e otimiza currículos para SEO/ATS usando um agente (`agno`) com modelo OpenAI. Ele lê arquivos colocados na pasta `file/` (PDF, TXT, MD, CSV, HTML, XML, RTF, PY, JS e DOCX) e gera uma versão otimizada diretamente no console.

### Principais recursos
- **Otimização para ATS e SEO** com prompt especializado em PT‑BR (ver `app/promts/system_promt.py`).
- **Leitura automática** de arquivos na pasta `file/`.
- **Streaming de resposta** no terminal, com exibição de raciocínio (opcional).
- **Persistência** de sessões em Postgres (via `docker-compose.yml`).

## Requisitos
- Python 3.12+
- Conta/Chave da OpenAI (variável `OPENAI_API_KEY`)
- Docker e Docker Compose (opcional, para o Postgres local)

## Instalação (local)
1) Clone o repositório
```bash
git clone https://github.com/artcgranja/agent-Resume-SEO
cd agent-Resume-SEO
```

2) Crie e ative o ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# No Windows: .venv\\Scripts\\activate
```

3) Instale as dependências
```bash
pip install "agno>=0.2.0" "python-docx>=1.1.2" "pdfminer.six>=20231228" \
            "python-multipart>=0.0.9" "pydantic>=2.6.0" "psycopg[binary]>=3.1" \
            "python-dotenv>=1.0.1" "openai>=1.9.0" "sqlalchemy>=2.0.0" "psycopg2-binary>=2.9.10"
```

## Configuração
1) Crie um arquivo `.env` na raiz com sua chave da OpenAI e (opcionalmente) a URL do banco:
```env
OPENAI_API_KEY=sk-...
# Opcional: se não setar, usa o default que aponta para o Docker Compose abaixo
DATABASE_URL=postgresql://resume:resume@localhost:5452/resume_db
```

2) (Opcional) Suba o Postgres com Docker Compose
```bash
docker compose up -d
```
O agente usará a tabela `agent_sessions` (configurado em `app/agents.py`).

## Como usar
1) Coloque seus arquivos de currículo na pasta `file/`. Exemplos:
   - `file/Meu Curriculo.pdf`
   - `file/Resume.txt`

2) Execute o agente
```bash
python main.py
```
O agente imprimirá a resposta no console. Por padrão, o `main.py` envia a mensagem:
```python
"Reescreva o currículo para otimizar meu SEO."
```
e anexa todos os arquivos suportados encontrados em `file/`.

## Personalização
- Mensagem inicial: edite em `main.py` a chamada `seo_agent.print_response(...)` e altere o primeiro argumento (string).
- Extensões suportadas: ajuste `allowed_exts` em `main.py`.
- MIME types: ajuste `ext_to_allowed_mime` em `main.py`. O `agno` valida apenas alguns tipos (por exemplo `application/pdf`, `text/plain`, `text/md`, `text/csv`, `text/html`, `text/xml`, `text/rtf`, `text/javascript`, `text/x-python`). Para tipos fora dessa lista, o código omite o `mime_type` e envia apenas `content` + `name`.
- Prompt do sistema (estratégia de escrita/otimização): configure em `app/promts/system_promt.py`.
- Modelo: em `app/agents.py`, a linha `model=OpenAIChat(id="gpt-4.1-2025-04-14")` pode ser alterada conforme sua conta OpenAI.

## Estrutura do projeto
- `main.py`: ponto de entrada; coleta arquivos em `file/` e chama o agente.
- `app/agents.py`: instancia e configura o `Agent` (modelo, storage, prompt do sistema).
- `app/promts/system_promt.py`: prompt do sistema detalhado para otimização de currículos.
- `docker-compose.yml`: serviço Postgres para persistência das sessões.
- `file/`: coloque aqui os arquivos do currículo.

## Erros comuns e soluções
- ValidationError: "Input should be a valid dictionary or instance of File"
  - Causa: enviar `BufferedReader` para `files`.
  - Solução: já implementado em `main.py` — agora enviamos dicionários compatíveis com `agno.media.File`:
    ```python
    {"content": bytes, "name": "arquivo.pdf", "mime_type": "application/pdf"}
    ```
- Falta de variável `OPENAI_API_KEY`
  - Defina `OPENAI_API_KEY` no `.env` ou ambiente.
- Banco não sobe/conecta
  - Rode `docker compose up -d` e confirme porta `5452` livre.

## Convenção de commits
Use o padrão:
- `[FEAT]`: nova funcionalidade
- `[FIX]`: correção de bug
- `[REFACTOR]`: refatoração sem mudança de funcionalidade
- `[CHORE]`: tarefas gerais, manutenção
- `[DOCS]`: documentação
- `[TEST]`: testes
- `[STYLE]`: formatação
- `[PERF]`: performance

Exemplos:
```text
[FEAT] Adicionando botão de exportação
[FIX] Corrigindo erro de login
[DOCS] Atualizando README com novas instruções
```

## Licença
Defina aqui a licença do projeto (ex.: MIT). Se ainda não houver, adicione um arquivo `LICENSE` posteriormente.
