import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sistema Médico", layout="wide")

# --- BARRA LATERAL (LOGIN) ---
st.sidebar.title("🔌 Conexão com Banco")
db_user = st.sidebar.text_input("Usuário (MySQL)", value="root")
db_password = st.sidebar.text_input("Senha (MySQL)", type="password") # Deixe em branco se não tiver senha
st.sidebar.info("Digite sua senha do MySQL acima e pressione Enter.")

# --- 2. FUNÇÃO DE CONEXÃO ---
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=db_user,
            password=db_password,
            database="ConsultasMedicas"
        )
        return conn
    except mysql.connector.Error as err:
        return None

# --- VERIFICAÇÃO INICIAL DE CONEXÃO ---
# Testamos a conexão antes de carregar qualquer página
conn_test = get_connection()
if conn_test is None:
    st.error("🚫 **Desconectado!**")
    st.warning("O sistema não conseguiu conectar ao MySQL.")
    st.markdown("""
    **Como resolver:**
    1. Vá na **barra lateral esquerda**.
    2. Digite a senha correta do seu MySQL (geralmente instalada na aula).
    3. Se não tiver senha, deixe o campo em branco.
    4. Verifique se o banco `ConsultasMedicas` foi criado.
    """)
    st.stop() # PARA O CÓDIGO AQUI para não dar erro lá embaixo
else:
    st.sidebar.success("✅ Conectado!")
    conn_test.close()

# --- 3. MENU DE NAVEGAÇÃO ---
st.sidebar.divider()
pagina = st.sidebar.radio("Navegação", ["Dashboard (Bonificação)", "Gerenciar Consultas (CRUD)", "Auditoria (Trigger)"])

# ==============================================================================
# PÁGINA 1: DASHBOARD
# ==============================================================================
if pagina == "Dashboard (Bonificação)":
    st.title("📊 Dashboard de Gestão Clínica")
    
    conn = get_connection()
    if conn: # Só executa se a conexão existir
        
        # KPI 1: Total de Consultas
        query_total = "SELECT COUNT(*) as total FROM Consulta"
        df_total = pd.read_sql(query_total, conn)
        total_consultas = df_total['total'][0]

        # KPI 2: Médicos
        query_medicos = "SELECT COUNT(*) as total FROM Medico"
        df_medicos = pd.read_sql(query_medicos, conn)
        total_medicos = df_medicos['total'][0]
        
        # Evitar divisão por zero
        media = total_consultas / total_medicos if total_medicos > 0 else 0

        col1, col2 = st.columns(2)
        col1.metric("Total de Consultas Agendadas", total_consultas)
        col2.metric("Média de Pacientes/Médico", f"{media:.1f}")

        st.divider()

        # GRÁFICO 1
        st.subheader("1. Especialidades mais procuradas")
        query_esp = """
        SELECT m.Especialidade, COUNT(c.IdConsulta) as Quantidade
        FROM Medico m
        JOIN Consulta c ON m.CodMed = c.CodMed
        GROUP BY m.Especialidade
        ORDER BY Quantidade DESC
        """
        df_esp = pd.read_sql(query_esp, conn)
        if not df_esp.empty:
            fig_bar = px.bar(df_esp, x='Especialidade', y='Quantidade', color='Especialidade', text_auto=True)
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Sem dados suficientes para o gráfico.")

        # GRÁFICO 2
        st.subheader("2. Evolução de Atendimentos (2023-2026)")
        query_tempo = """
        SELECT DATE(Data_Hora) as Data, COUNT(*) as Consultas
        FROM Consulta
        GROUP BY DATE(Data_Hora)
        ORDER BY Data ASC
        """
        df_tempo = pd.read_sql(query_tempo, conn)
        if not df_tempo.empty:
            fig_line = px.line(df_tempo, x='Data', y='Consultas', markers=True)
            st.plotly_chart(fig_line, use_container_width=True)

        # RELATÓRIO
        st.subheader("3. Alerta: Médicos Ociosos (Left Join)")
        query_ociosos = """
        SELECT m.NomeMed, m.Especialidade, m.Email
        FROM Medico m
        LEFT JOIN Consulta c ON m.CodMed = c.CodMed
        WHERE c.IdConsulta IS NULL
        """
        df_ociosos = pd.read_sql(query_ociosos, conn)
        st.dataframe(df_ociosos, use_container_width=True)
        
        conn.close()

# ==============================================================================
# PÁGINA 2: CRUD
# ==============================================================================
elif pagina == "Gerenciar Consultas (CRUD)":
    st.title("📋 Gerenciamento de Consultas")
    conn = get_connection()
    if conn:
        cursor = conn.cursor()

        # VIEW
        query_view = """
        SELECT c.IdConsulta, cl.NomeCli, m.NomeMed, p.NomePac, c.Data_Hora
        FROM Consulta c
        JOIN Clinica cl ON c.CodCli = cl.CodCli
        JOIN Medico m ON c.CodMed = m.CodMed
        JOIN Paciente p ON c.CpfPaciente = p.CpfPaciente
        ORDER BY c.Data_Hora DESC
        """
        df_view = pd.read_sql(query_view, conn)
        st.dataframe(df_view)

        st.divider()

        # INSERT
        st.subheader("Nova Consulta")
        medicos = pd.read_sql("SELECT CodMed, NomeMed FROM Medico", conn)
        pacientes = pd.read_sql("SELECT CpfPaciente, NomePac FROM Paciente", conn)
        clinicas = pd.read_sql("SELECT CodCli, NomeCli FROM Clinica", conn)

        with st.form("form_add"):
            if not medicos.empty and not pacientes.empty and not clinicas.empty:
                med_selecionado = st.selectbox("Médico", medicos['CodMed'] + " - " + medicos['NomeMed'])
                pac_selecionado = st.selectbox("Paciente", pacientes['CpfPaciente'] + " - " + pacientes['NomePac'])
                cli_selecionado = st.selectbox("Clínica", clinicas['CodCli'] + " - " + clinicas['NomeCli'])
                data_hora = st.text_input("Data e Hora (AAAA-MM-DD HH:MM:SS)", "2025-11-28 10:00:00")
                
                if st.form_submit_button("Agendar Consulta"):
                    try:
                        cod_med = med_selecionado.split(" - ")[0]
                        cpf_pac = pac_selecionado.split(" - ")[0]
                        cod_cli = cli_selecionado.split(" - ")[0]
                        cursor.execute("INSERT INTO Consulta (CodCli, CodMed, CpfPaciente, Data_Hora) VALUES (%s, %s, %s, %s)", 
                                    (cod_cli, cod_med, cpf_pac, data_hora))
                        conn.commit()
                        st.success("Agendado! Atualize a página.")
                    except mysql.connector.Error as e:
                        st.error(f"Erro ao inserir: {e}")
            else:
                st.warning("Faltam dados de Médicos, Pacientes ou Clínicas no banco.")
                st.form_submit_button("Agendar (Bloqueado)")

        # DELETE
        st.divider()
        st.subheader("Cancelar Consulta")
        id_delete = st.number_input("ID da Consulta", min_value=1, step=1)
        if st.button("Remover Consulta"):
            try:
                cursor.execute("DELETE FROM Consulta WHERE IdConsulta = %s", (id_delete,))
                conn.commit()
                if cursor.rowcount > 0:
                    st.warning(f"Consulta {id_delete} removida!")
                else:
                    st.error("ID não encontrado.")
            except mysql.connector.Error as e:
                st.error(f"Erro ao remover (Integridade): {e}")

        conn.close()

# ==============================================================================
# PÁGINA 3: AUDITORIA
# ==============================================================================
elif pagina == "Auditoria (Trigger)":
    st.title("🕵️ Log de Cancelamentos")
    conn = get_connection()
    if conn:
        df_log = pd.read_sql("SELECT * FROM Log_Cancelamento ORDER BY DataCancelamento DESC", conn)
        st.dataframe(df_log, use_container_width=True)
        conn.close()