## Agent Resume SEO — Multi‑Agent Chat

Assistente multi‑agente (baseado em `agno`) para otimizar e avaliar currículos com colaboração de agentes especializados e busca na Web. Lê arquivos na pasta `file/` (PDF, TXT, MD, CSV, HTML, XML, RTF, PY, JS, DOCX) e interage no terminal em um loop estilo chat.

### Principais recursos
- **Time de agentes (Team)** em modo collaborate:
  - **SEO Agent**: reescrita/otimização para ATS/SEO.
  - **Evaluate Agent**: avaliação do currículo frente a vagas.
  - **Web Agent**: pesquisa (DuckDuckGo) para contexto de vagas/empresas.
- **Persistência** de sessões no Postgres (tanto dos agentes quanto do time).
- **Arquivos anexados automaticamente** de `file/` via `agno.media.File`.
- **Chat interativo** no terminal com histórico.

## Requisitos
- Python 3.12+
- Chave da OpenAI (`OPENAI_API_KEY`)
- Postgres local (via Docker Compose, opcional)

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
# Windows: .venv\\Scripts\\activate
```

3) Instale as dependências
```bash
pip install "agno>=0.2.0" \
            "python-docx>=1.1.2" "pdfminer.six>=20231228" \
            "python-multipart>=0.0.9" "pydantic>=2.6.0" \
            "psycopg[binary]>=3.1" "python-dotenv>=1.0.1" \
            "openai>=1.9.0" "sqlalchemy>=2.0.0" "psycopg2-binary>=2.9.10"
```
Nota: Se aparecer aviso do `duckduckgo_search` renomeado, instale `ddgs` no seu ambiente virtual.

## Configuração
Crie `.env` na raiz:
```env
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://resume:resume@localhost:5452/resume_db
```

Suba o Postgres com Docker (opcional):
```bash
docker compose up -d
```

## Banco de dados
- Modelos próprios: `resumes` e `evaluate_resumes`.
- Storage do agno: time usa `team_sessions`; agentes usam `agent_sessions`.

Inicialize/sincronize tabelas dos modelos próprios:
```bash
python scripts/init_db.py init
```
Outros comandos úteis:
```bash
python scripts/init_db.py check   # testa conexão
python scripts/init_db.py reset   # drop + create de todas as tabelas dos modelos próprios
```

## Executando o chat
1) Coloque seus arquivos em `file/` (por exemplo, `CV.pdf`).
2) Rode:
```bash
python main.py
```
O app:
- Lê arquivos suportados em `file/` e os envia via `run_with_files(...)`.
- Inicia um loop de chat. Digite suas mensagens após `user:`. Para sair, digite `exit`.

## Arquitetura
- `app/agents/orchestrator.py`: cria um `Team` (modo `collaborate`) com:
  - `SEO Agent` (`app/agents/seo_resume_agent.py`)
  - `Evaluate Agent` (`app/agents/evaluate_resume_agent.py`)
  - `Web Agent` (`app/agents/web_agent.py`)
- `main.py`: coleta arquivos de `file/` e inicia a conversa usando `Orchestrator.run_with_files(...)`.
- `app/tools/*`: ferramentas expostas aos agentes para salvar/listar/editar/recuperar currículos e avaliações.

## Dicas e erros comuns
- "Resume not found": salve primeiro via ferramenta (o agente pode chamar `save_resume`).
- `relation "evaluate_resumes" does not exist`: rode `python scripts/init_db.py init` para criar as tabelas dos modelos.
- Aviso DuckDuckGo: instale `ddgs` no ambiente virtual quando solicitado.
- Erros de schema do storage do agno (colunas como `team_id`): use nomes de tabelas novas (`team_sessions` para Team) ou deixe o agno criar/atualizar automaticamente conforme sua versão. Se já existir uma tabela antiga conflitante, renomeie ou esvazie.

## Convenção de commits
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
Defina aqui a licença do projeto (ex.: MIT). Se ainda não houver, adicione um arquivo `LICENSE`.
