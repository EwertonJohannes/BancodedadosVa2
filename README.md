# Sistema de Gestão de Consultas Médicas 🏥

Este projeto é um sistema Web desenvolvido em Python (Streamlit) conectado a um banco de dados MySQL. Ele realiza operações de CRUD (Consultas, Médicos, Pacientes) e apresenta um Dashboard gerencial com gráficos analíticos.

## 📋 Pré-requisitos

Para rodar este projeto, você precisa ter instalado:
* [Python](https://www.python.org/downloads/) (versão 3.8 ou superior)
* [MySQL Server e Workbench](https://dev.mysql.com/downloads/installer/)
* VS Code (Recomendado)

## 🚀 Instalação e Configuração

### 1. Configurar o Banco de Dados
1. Abra o **MySQL Workbench**.
2. Vá em `File > Open SQL Script` e selecione o arquivo `script_banco.sql` que está neste repositório.
3. Execute todo o script (Raio Grande ⚡) para criar o banco `ConsultasMedicas` e popular as tabelas.

### 2. Instalar as Dependências (Python)
Abra o terminal na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

### 3. Executar o Sistema
No terminal, execute:

```bash
streamlit run app.py
```

O sistema abrirá automaticamente no seu navegador em `http://localhost:8501`.

## 🔐 Configuração de Acesso

Na primeira execução:
1. Na **barra lateral esquerda**, digite o usuário MySQL (padrão: `root`)
2. Digite sua senha do MySQL
3. Se não tiver senha configurada, deixe o campo em branco
4. O sistema validará a conexão automaticamente

## 📌 Funcionalidades

### 1️⃣ Dashboard (Bonificação)
- **KPIs**: Total de consultas e média de pacientes por médico
- **Gráfico de Barras**: Especialidades médicas mais procuradas
- **Gráfico de Linha**: Evolução temporal dos atendimentos
- **Relatório**: Médicos ociosos (sem consultas agendadas) usando LEFT JOIN

### 2️⃣ Gerenciar Consultas (CRUD)
- **Listar**: Visualização de todas as consultas com informações de clínica, médico e paciente
- **Inserir**: Agendamento de novas consultas
- **Deletar**: Cancelamento de consultas pelo ID

### 3️⃣ Auditoria (Trigger)
- Visualização do log de cancelamentos
- Registra automaticamente data e ID das consultas removidas através de trigger no banco

## 🗂️ Estrutura do Projeto

```
BancodedadosVa2/
│
├── app.py                  # Aplicação principal Streamlit
├── requirements.txt        # Dependências Python
├── script_banco.sql        # Script de criação do banco de dados
└── README.md              # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**: Linguagem de programação
- **Streamlit**: Framework para interface web
- **MySQL**: Banco de dados relacional
- **Pandas**: Manipulação de dados
- **Plotly**: Visualização de gráficos interativos
- **mysql-connector-python**: Conexão Python-MySQL

## 📊 Modelo do Banco de Dados

O sistema utiliza as seguintes tabelas principais:
- **Clinica**: Informações das clínicas
- **Medico**: Cadastro de médicos e especialidades
- **Paciente**: Dados dos pacientes
- **Consulta**: Agendamentos e relacionamentos
- **Log_Cancelamento**: Auditoria de exclusões (populada via trigger)

## ⚠️ Troubleshooting

### Erro de Conexão com MySQL
- Verifique se o MySQL Server está rodando
- Confirme se o banco `ConsultasMedicas` foi criado
- Valide usuário e senha na barra lateral

### Erro ao instalar dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Porta já em uso (Streamlit)
```bash
streamlit run app.py --server.port 8502
```

## 👨‍💻 Autor

Desenvolvido como projeto acadêmico de Banco de Dados.


