# 🚀 Desafio Estágio Python - b2bflow

Repositório desenvolvido para o processo seletivo da vaga de **Estágio em Desenvolvimento Python** na **b2bflow**.

O objetivo principal do projeto é realizar a integração entre um banco de dados relacional (**Supabase**) e uma API de mensageria (**Z-API**) para automação de disparos de mensagens customizadas via WhatsApp.

A versão atual foi evoluída para suportar **disparos em massa flexíveis**, processando dinamicamente todos os contatos ativos presentes na base de dados, sem travas ou limites rígidos de paginação.

---

# 🛠️ Tecnologias Utilizadas

- **Python 3.x** - Linguagem base do projeto.
- **Supabase (PostgreSQL)** - Banco de dados para persistência dos contatos.
- **Z-API** - Gateway para envio de mensagens via WhatsApp.
- **Requests** - Biblioteca para consumo de APIs REST.
- **python-dotenv** - Gerenciamento de variáveis de ambiente.

---

# 💾 Modelagem e Setup da Tabela (Supabase)

A tabela `contatos` foi estruturada para armazenar os dados necessários para personalização das mensagens.

Execute o script abaixo no **SQL Editor** do Supabase.

```sql
-- Garante que a tabela comece limpa para os testes
drop table if exists contatos;

-- Criação da tabela
create table contatos (
    id bigint generated always as identity primary key,
    nome text not null,
    telefone text not null
);

-- Inserção de contatos fictícios
insert into contatos (nome, telefone) values
('Carlos Eduardo Silva', '5511999991111'),
('Ana Beatriz Souza', '5521988882222'),
('Marcos Antônio Pereira', '5531977773333'),
('Juliana Maria Oliveira', '5541966664444'),
('Lucas Rafael Santos', '5561955555555'),
('Fernanda Costa Lima', '5581944446666'),
('Rodrigo Alves Almeida', '5571933337777');
```

---

# ⚙️ Instalação e Execução Local

## 1. Clone o repositório

```bash
git clone https://github.com/linskrs/meu-desafio-b2bflow.git
cd meu-desafio-b2bflow
```

---

## 2. Crie o ambiente virtual

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> **Caso o PowerShell bloqueie a execução de scripts:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

### Linux / macOS / Git Bash

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 4. Configure as variáveis de ambiente

Crie um arquivo chamado `.env` na raiz do projeto (utilize o `.env.example` como modelo):

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_service_role

ZAPI_INSTANCE_ID=sua_instancia
ZAPI_TOKEN=seu_token
ZAPI_CLIENT_TOKEN=seu_client_token
```

> 🔒 **Importante:** o arquivo `.env` contém credenciais sensíveis e está listado no `.gitignore`, portanto nunca será enviado ao GitHub.

---

## 5. Execute a aplicação

```bash
python main.py
```

---

# 📋 Arquitetura do Sistema

## 🔹 Integração HTTP

A comunicação com o Supabase e com a Z-API é realizada diretamente através da biblioteca **Requests**, utilizando chamadas HTTP REST.

Essa abordagem elimina dependências desnecessárias de SDKs, oferecendo maior controle, simplicidade e facilidade de manutenção.

---

## 🔹 Disparo Dinâmico

O sistema percorre automaticamente todos os registros retornados pelo banco de dados e monta a mensagem utilizando o template exigido pelo desafio:

```text
Olá, {nome} tudo bem com você?
```

Cada contato recebe sua própria mensagem personalizada.

---

## 🔹 Logging

Toda a aplicação utiliza a biblioteca padrão **logging** para registrar:

- Inicialização do sistema;
- Leitura do banco;
- Envio de mensagens;
- Sucesso nas requisições;
- Falhas;
- Erros de comunicação.

Os logs possuem timestamp e níveis de severidade (`INFO`, `WARNING` e `ERROR`).

---

## 🔹 Tratamento de Exceções

O projeto trata exceções relacionadas a:

- Timeout;
- Falhas de conexão;
- Erros HTTP;
- `requests.exceptions.RequestException`.

---

## 🔹 Modo Simulação

Caso as credenciais da Z-API não estejam configuradas no arquivo `.env`, o sistema entra automaticamente em **Modo Simulação**.

Nesse modo:

- Nenhuma mensagem é enviada;
- O payload é exibido no terminal;
- O fluxo continua normalmente;
- Permite testes sem consumir a API da Z-API.

---

# 📂 Estrutura do Projeto

```text
.
├── main.py
├── .env.example
├── requirements.txt
├── README.md
└── logs/
```

---

# ✅ Funcionalidades

- Integração com Supabase.
- Integração com Z-API.
- Leitura dinâmica de todos os contatos.
- Disparo personalizado via WhatsApp.
- Logging estruturado.
- Tratamento de exceções.
- Modo simulação para testes.
- Configuração através de variáveis de ambiente.

---

# 👨‍💻 Autor

**Liniker Silva**