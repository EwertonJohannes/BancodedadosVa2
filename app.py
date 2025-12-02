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
pagina = st.sidebar.radio("Navegação", ["Dashboard ", "Gerenciar Consultas (CRUD)", "Gerenciar Cadastros", "Auditoria (Trigger)"])

# ==============================================================================
# PÁGINA 1: DASHBOARD
# ==============================================================================
if pagina == "Dashboard ":
    st.title("📊 Dashboard de Gestão Clínica")
    
    conn = get_connection()
    if conn: # Só executa se a conexão existir
        
        # === FILTROS INTERATIVOS ===
        st.sidebar.divider()
        st.sidebar.subheader("🔍 Filtros do Dashboard")
        
        # Filtro de período
        col_data1, col_data2 = st.sidebar.columns(2)
        data_inicio = col_data1.date_input("Data Início", value=pd.to_datetime("2015-01-01"))
        data_fim = col_data2.date_input("Data Fim", value=pd.to_datetime("2036-12-29"))
        
        # Filtro de especialidade
        query_especialidades = "SELECT DISTINCT Especialidade FROM Medico ORDER BY Especialidade"
        df_especialidades = pd.read_sql(query_especialidades, conn)
        especialidades_list = ["Todas"] + df_especialidades['Especialidade'].tolist()
        filtro_especialidade = st.sidebar.selectbox("Especialidade", especialidades_list)
        
        # Construir filtro SQL
        filtro_where = f"WHERE DATE(c.Data_Hora) BETWEEN '{data_inicio}' AND '{data_fim}'"
        if filtro_especialidade != "Todas":
            filtro_where += f" AND m.Especialidade = '{filtro_especialidade}'"
        
        # KPI 1: Total de Consultas
        query_total = f"SELECT COUNT(*) as total FROM Consulta c JOIN Medico m ON c.CodMed = m.CodMed {filtro_where}"
        df_total = pd.read_sql(query_total, conn)
        total_consultas = df_total['total'][0]

        # KPI 2: Médicos
        query_medicos = "SELECT COUNT(*) as total FROM Medico"
        df_medicos = pd.read_sql(query_medicos, conn)
        total_medicos = df_medicos['total'][0]
        
        # KPI 3: Pacientes únicos
        query_pacientes = f"SELECT COUNT(DISTINCT c.CpfPaciente) as total FROM Consulta c JOIN Medico m ON c.CodMed = m.CodMed {filtro_where}"
        df_pacientes = pd.read_sql(query_pacientes, conn)
        total_pacientes = df_pacientes['total'][0]
        
        # Evitar divisão por zero
        media = total_consultas / total_medicos if total_medicos > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("📅 Total de Consultas", total_consultas)
        col2.metric("👨‍⚕️ Total de Médicos", total_medicos)
        col3.metric("🏥 Média Consultas/Médico", f"{media:.1f}")

        st.divider()
        
        # === SEÇÃO DE RANKINGS COM GRÁFICOS ===
        col_rank1, col_rank2 = st.columns(2)
        
        with col_rank1:
            st.subheader("🏆 Top 10 Médicos")
            query_rank_med = f"""
            SELECT m.NomeMed, m.Especialidade, COUNT(c.IdConsulta) as TotalConsultas
            FROM Medico m
            JOIN Consulta c ON m.CodMed = c.CodMed
            {filtro_where}
            GROUP BY m.NomeMed, m.Especialidade
            ORDER BY TotalConsultas DESC
            LIMIT 10
            """
            df_rank_med = pd.read_sql(query_rank_med, conn)
            if not df_rank_med.empty:
                fig_rank_med = px.bar(df_rank_med, 
                                     y='NomeMed', 
                                     x='TotalConsultas',
                                     orientation='h',
                                     color='Especialidade',
                                     text='TotalConsultas',
                                     hover_data=['Especialidade'])
                fig_rank_med.update_layout(yaxis={'categoryorder':'total ascending'}, height=400)
                st.plotly_chart(fig_rank_med, use_container_width=True)
            else:
                st.info("Sem dados para o período selecionado")

        with col_rank2:
            st.subheader("👥 Top 10 Pacientes")
            query_rank_pac = f"""
            SELECT p.NomePac, COUNT(c.IdConsulta) as TotalConsultas
            FROM Paciente p
            JOIN Consulta c ON p.CpfPaciente = c.CpfPaciente
            JOIN Medico m ON c.CodMed = m.CodMed
            {filtro_where}
            GROUP BY p.NomePac
            ORDER BY TotalConsultas DESC
            LIMIT 10
            """
            df_rank_pac = pd.read_sql(query_rank_pac, conn)
            if not df_rank_pac.empty:
                fig_rank_pac = px.bar(df_rank_pac,
                                     y='NomePac',
                                     x='TotalConsultas',
                                     orientation='h',
                                     color='TotalConsultas',
                                     text='TotalConsultas',
                                     color_continuous_scale='Blues')
                fig_rank_pac.update_layout(yaxis={'categoryorder':'total ascending'}, height=400)
                st.plotly_chart(fig_rank_pac, use_container_width=True)
            else:
                st.info("Sem dados para o período selecionado")
        
        st.divider()

        # === ESPECIALIDADES COM VISUALIZAÇÃO DUPLA ===
        st.subheader("🩺 Análise de Especialidades")
        
        query_esp = f"""
        SELECT m.Especialidade, COUNT(c.IdConsulta) as Quantidade
        FROM Medico m
        JOIN Consulta c ON m.CodMed = c.CodMed
        {filtro_where}
        GROUP BY m.Especialidade
        ORDER BY Quantidade DESC
        """
        df_esp = pd.read_sql(query_esp, conn)
        
        if not df_esp.empty:
            col_esp1, col_esp2 = st.columns(2)
            
            with col_esp1:
                # Gráfico de Pizza Interativo
                fig_pie = px.pie(df_esp, 
                               values='Quantidade', 
                               names='Especialidade',
                               title='Distribuição por Especialidade',
                               hole=0.4,
                               color_discrete_sequence=px.colors.qualitative.Set3)
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col_esp2:
                # Gráfico de Barras com Cores Graduadas
                fig_bar = px.bar(df_esp, 
                               x='Especialidade', 
                               y='Quantidade',
                               title='Quantidade por Especialidade',
                               text='Quantidade',
                               color='Quantidade',
                               color_continuous_scale='Viridis')
                fig_bar.update_traces(texttemplate='%{text}', textposition='outside')
                fig_bar.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Sem dados suficientes para o gráfico.")

        st.divider()
        
        # === EVOLUÇÃO TEMPORAL INTERATIVA ===
        st.subheader("📈 Evolução de Atendimentos ao Longo do Tempo")
        
        # Seletor de agrupamento
        agrupamento = st.radio("Agrupar por:", ["Dia", "Semana", "Mês"], horizontal=True)
        
        if agrupamento == "Dia":
            query_tempo = f"""
            SELECT DATE(c.Data_Hora) as Data, COUNT(*) as Consultas
            FROM Consulta c
            JOIN Medico m ON c.CodMed = m.CodMed
            {filtro_where}
            GROUP BY DATE(c.Data_Hora)
            ORDER BY Data ASC
            """
        elif agrupamento == "Semana":
            query_tempo = f"""
            SELECT DATE_FORMAT(c.Data_Hora, '%Y-%u') as Data, COUNT(*) as Consultas
            FROM Consulta c
            JOIN Medico m ON c.CodMed = m.CodMed
            {filtro_where}
            GROUP BY DATE_FORMAT(c.Data_Hora, '%Y-%u')
            ORDER BY Data ASC
            """
        else:  # Mês
            query_tempo = f"""
            SELECT DATE_FORMAT(c.Data_Hora, '%Y-%m') as Data, COUNT(*) as Consultas
            FROM Consulta c
            JOIN Medico m ON c.CodMed = m.CodMed
            {filtro_where}
            GROUP BY DATE_FORMAT(c.Data_Hora, '%Y-%m')
            ORDER BY Data ASC
            """
        
        df_tempo = pd.read_sql(query_tempo, conn)
        if not df_tempo.empty:
            fig_line = px.line(df_tempo, 
                             x='Data', 
                             y='Consultas', 
                             markers=True,
                             title=f'Consultas Agrupadas por {agrupamento}')
            fig_line.update_traces(line_color='#FF6B6B', line_width=3, marker_size=8)
            fig_line.update_layout(hovermode='x unified',
                                  xaxis_title="Período",
                                  yaxis_title="Número de Consultas")
            st.plotly_chart(fig_line, use_container_width=True)
            
            # Estatísticas adicionais
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            col_stat1.metric("📊 Média", f"{df_tempo['Consultas'].mean():.1f}")
            col_stat2.metric("🔼 Máximo", df_tempo['Consultas'].max())
            col_stat3.metric("🔽 Mínimo", df_tempo['Consultas'].min())
        else:
            st.info("Sem dados para o período selecionado")

        st.divider()
        
        # === ANÁLISE DE MÉDICOS OCIOSOS ===
        st.subheader("⚠️ Alerta: Médicos Sem Consultas Agendadas")
        
        query_ociosos = f"""
        SELECT m.NomeMed, m.Especialidade, m.Email
        FROM Medico m
        LEFT JOIN (
            SELECT DISTINCT CodMed 
            FROM Consulta c
            WHERE DATE(c.Data_Hora) BETWEEN '{data_inicio}' AND '{data_fim}'
        ) c ON m.CodMed = c.CodMed
        WHERE c.CodMed IS NULL
        """
        df_ociosos = pd.read_sql(query_ociosos, conn)
        
        if not df_ociosos.empty:
            st.warning(f"⚠️ {len(df_ociosos)} médico(s) sem consultas no período selecionado")
            st.dataframe(df_ociosos, use_container_width=True)
        else:
            st.success("✅ Todos os médicos têm consultas agendadas no período!")
        
        conn.close()

# ==============================================================================
# PÁGINA 2: CRUD
# ==============================================================================
elif pagina == "Gerenciar Consultas (CRUD)":
    st.title("📋 Gerenciamento de Consultas")
    conn = get_connection()
    if conn:
        cursor = conn.cursor()

        # BUSCA RÁPIDA
        st.subheader("Busca Rápida de Consultas")
        busca_paciente = st.text_input("Buscar por nome do paciente")
        busca_medico = st.text_input("Buscar por nome do médico")
        busca_clinica = st.text_input("Buscar por nome da clínica")
        filtro_sql = []
        if busca_paciente:
            filtro_sql.append(f"p.NomePac LIKE '%{busca_paciente}%'")
        if busca_medico:
            filtro_sql.append(f"m.NomeMed LIKE '%{busca_medico}%'")
        if busca_clinica:
            filtro_sql.append(f"cl.NomeCli LIKE '%{busca_clinica}%'")
        where_sql = ' AND '.join(filtro_sql)
        if where_sql:
            where_sql = 'WHERE ' + where_sql
        # VIEW
        query_view = f"""
        SELECT c.IdConsulta, cl.NomeCli, m.NomeMed, p.NomePac, c.Data_Hora
        FROM Consulta c
        JOIN Clinica cl ON c.CodCli = cl.CodCli
        JOIN Medico m ON c.CodMed = m.CodMed
        JOIN Paciente p ON c.CpfPaciente = p.CpfPaciente
        {where_sql}
        ORDER BY c.IdConsulta ASC
        """
        df_view = pd.read_sql(query_view, conn)
        st.dataframe(df_view)

        st.divider()

        # CONSULTA POR DATA/MÊS/ANO
        st.subheader("Consultar Agenda")
        
        col_tipo_filtro, col_inputs = st.columns([1, 3])
        
        with col_tipo_filtro:
            tipo_filtro = st.radio("Filtrar por:", ["Dia", "Mês", "Ano"])
        
        where_clause = ""
        descricao_filtro = ""
        
        with col_inputs:
            if tipo_filtro == "Dia":
                data_agenda = st.date_input("Selecione a Data", key="busca_data_agenda_new")
                where_clause = f"DATE(c.Data_Hora) = '{data_agenda}'"
                descricao_filtro = data_agenda.strftime('%d/%m/%Y')
                
            elif tipo_filtro == "Mês":
                col_mes, col_ano = st.columns(2)
                import datetime
                hoje = datetime.date.today()
                mes_sel = col_mes.selectbox("Mês", range(1, 13), index=hoje.month-1)
                ano_sel = col_ano.number_input("Ano", min_value=2000, max_value=2100, value=hoje.year)
                where_clause = f"MONTH(c.Data_Hora) = {mes_sel} AND YEAR(c.Data_Hora) = {ano_sel}"
                descricao_filtro = f"{mes_sel:02d}/{ano_sel}"
                
            elif tipo_filtro == "Ano":
                import datetime
                hoje = datetime.date.today()
                ano_sel = st.number_input("Ano", min_value=2000, max_value=2100, value=hoje.year)
                where_clause = f"YEAR(c.Data_Hora) = {ano_sel}"
                descricao_filtro = f"{ano_sel}"

        if st.button("Buscar Consultas"):
            query_agenda = f"""
            SELECT c.IdConsulta, c.Data_Hora, m.NomeMed as Médico, p.NomePac as Paciente, cl.NomeCli as Clínica
            FROM Consulta c
            JOIN Medico m ON c.CodMed = m.CodMed
            JOIN Paciente p ON c.CpfPaciente = p.CpfPaciente
            JOIN Clinica cl ON c.CodCli = cl.CodCli
            WHERE {where_clause}
            ORDER BY c.Data_Hora ASC
            """
            df_agenda = pd.read_sql(query_agenda, conn)
            
            if not df_agenda.empty:
                st.success(f"📅 {len(df_agenda)} consulta(s) encontrada(s) para {descricao_filtro}")
                st.dataframe(df_agenda, use_container_width=True)
            else:
                st.info(f"Nenhuma consulta agendada para {descricao_filtro}.")


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
                import datetime
                data_consulta = st.date_input("Data da Consulta", datetime.date.today())
                hora_consulta = st.time_input("Hora da Consulta", datetime.datetime.now().time())
                data_hora = datetime.datetime.combine(data_consulta, hora_consulta).strftime("%Y-%m-%d %H:%M:%S")
                submit_nova = st.form_submit_button("Agendar Consulta")
                if submit_nova:
                    try:
                        cod_med = med_selecionado.split(" - ")[0]
                        cpf_pac = pac_selecionado.split(" - ")[0]
                        cod_cli = cli_selecionado.split(" - ")[0]
                        cursor.execute("INSERT INTO Consulta (CodCli, CodMed, CpfPaciente, Data_Hora) VALUES (%s, %s, %s, %s)", 
                                    (cod_cli, cod_med, cpf_pac, data_hora))
                        conn.commit()
                        st.info(f"Linhas afetadas: {cursor.rowcount}")
                        if cursor.rowcount > 0:
                            st.success("Agendado! Atualize a página.")
                        else:
                            st.error("Nenhuma linha foi inserida. Verifique os dados e permissões do banco.")
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
# PÁGINA 3: GERENCIAR CADASTROS (COM GESTÃO DE CONEXÃO CORRIGIDA)
# ==============================================================================
elif pagina == "Gerenciar Cadastros":
    st.title("📋 Gerenciamento de Cadastros")
    
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        
        # Abas para cada entidade
        tab1, tab2, tab3 = st.tabs(["👥 Pacientes", "👨‍⚕️ Médicos", "🏥 Clínicas"])
        
        # ========== ABA PACIENTES ==========
        with tab1:
            st.header("Gerenciar Pacientes")
            
            # Busca de Pacientes
            col_search1, col_search2 = st.columns([3, 1])
            with col_search1:
                busca_paciente = st.text_input("🔍 Buscar paciente por nome ou CPF", key="busca_pac")
            with col_search2:
                st.write("")
                st.write("")
                btn_limpar_pac = st.button("🔄 Limpar Filtro", key="limpar_pac")
            
            # Query base
            query_pacientes = """
            SELECT 
                p.CpfPaciente as CPF,
                p.NomePac as Nome,
                p.DataNascimento as 'Data Nascimento',
                p.Genero as Gênero,
                p.Telefone,
                p.Email,
                COUNT(c.IdConsulta) as 'Total Consultas'
            FROM Paciente p
            LEFT JOIN Consulta c ON p.CpfPaciente = c.CpfPaciente
            """
            
            if busca_paciente and not btn_limpar_pac:
                query_pacientes += f" WHERE p.NomePac LIKE '%{busca_paciente}%' OR p.CpfPaciente LIKE '%{busca_paciente}%'"
            
            query_pacientes += " GROUP BY p.CpfPaciente, p.NomePac, p.DataNascimento, p.Genero, p.Telefone, p.Email ORDER BY p.NomePac ASC"
            
            df_pacientes = pd.read_sql(query_pacientes, conn)
            
            st.subheader(f"📊 Total de Pacientes: {len(df_pacientes)}")
            st.dataframe(df_pacientes, use_container_width=True, hide_index=True)
            
            # Detalhes do Paciente Selecionado
            st.divider()
            st.subheader("🔍 Detalhes do Paciente")
            
            cpf_selecionado = st.selectbox("Selecione um paciente", df_pacientes['CPF'].tolist() if not df_pacientes.empty else [], key="sel_pac_tab1")
            
            if cpf_selecionado:
                # Dados do paciente
                paciente_info = df_pacientes[df_pacientes['CPF'] == cpf_selecionado].iloc[0]
                
                col_info1, col_info2, col_info3 = st.columns(3)
                col_info1.metric("👤 Nome", paciente_info['Nome'])
                col_info2.metric("📅 Data Nascimento", str(paciente_info['Data Nascimento']))
                col_info3.metric("📊 Total de Consultas", int(paciente_info['Total Consultas']))
                
                # Consultas do paciente
                st.subheader("📋 Histórico de Consultas")
                query_consultas_pac = f"""
                SELECT 
                    c.IdConsulta as 'ID',
                    c.Data_Hora as 'Data/Hora',
                    m.NomeMed as 'Médico',
                    m.Especialidade,
                    cl.NomeCli as 'Clínica'
                FROM Consulta c
                JOIN Medico m ON c.CodMed = m.CodMed
                JOIN Clinica cl ON c.CodCli = cl.CodCli
                WHERE c.CpfPaciente = '{cpf_selecionado}'
                ORDER BY c.Data_Hora DESC
                """
                df_consultas_pac = pd.read_sql(query_consultas_pac, conn)
                
                if not df_consultas_pac.empty:
                    st.dataframe(df_consultas_pac, use_container_width=True, hide_index=True)
                else:
                    st.info("Este paciente ainda não tem consultas agendadas.")
        
        # ========== ABA MÉDICOS ==========
        with tab2:
            st.header("Gerenciar Médicos")
            
            # Busca de Médicos
            col_search1, col_search2, col_search3 = st.columns([2, 2, 1])
            with col_search1:
                busca_medico = st.text_input("🔍 Buscar médico por nome", key="busca_med_tab2")
            with col_search2:
                especialidades_disponiveis = pd.read_sql("SELECT DISTINCT Especialidade FROM Medico ORDER BY Especialidade", conn)
                filtro_esp = st.selectbox("Filtrar por especialidade", ["Todas"] + especialidades_disponiveis['Especialidade'].tolist(), key="filtro_esp_tab2")
            with col_search3:
                st.write("")
                st.write("")
                btn_limpar_med = st.button("🔄 Limpar", key="limpar_med_tab2")
            
            # Query base (READ)
            query_medicos = """
            SELECT 
                m.CodMed as 'Código',
                m.NomeMed as 'Nome',
                m.Especialidade,
                m.Email,
                m.Telefone,
                COUNT(c.IdConsulta) as 'Total Consultas',
                COUNT(DISTINCT c.CpfPaciente) as 'Pacientes Atendidos'
            FROM Medico m
            LEFT JOIN Consulta c ON m.CodMed = c.CodMed
            """
            
            filtros = []
            if busca_medico and not btn_limpar_med:
                filtros.append(f"m.NomeMed LIKE '%{busca_medico}%'")
            if filtro_esp != "Todas" and not btn_limpar_med:
                filtros.append(f"m.Especialidade = '{filtro_esp}'")
            
            if filtros:
                query_medicos += " WHERE " + " AND ".join(filtros)
            
            query_medicos += " GROUP BY m.CodMed, m.NomeMed, m.Especialidade, m.Email, m.Telefone ORDER BY m.NomeMed ASC"
            
            df_medicos = pd.read_sql(query_medicos, conn)
            
            st.subheader(f"📊 Total de Médicos: {len(df_medicos)}")
            st.dataframe(df_medicos, use_container_width=True, hide_index=True)
            
            # Detalhes do Médico Selecionado
            st.divider()
            st.subheader("🔍 Detalhes do Médico")
            
            cod_med_selecionado = st.selectbox("Selecione um médico", df_medicos['Código'].tolist() if not df_medicos.empty else [], key="sel_med_tab2")
            
            if cod_med_selecionado:
                medico_info = df_medicos[df_medicos['Código'] == cod_med_selecionado].iloc[0]
                
                col_info1, col_info2, col_info3, col_info4 = st.columns(4)
                col_info1.metric("👨‍⚕️ Nome", medico_info['Nome'])
                col_info2.metric("🩺 Especialidade", medico_info['Especialidade'])
                col_info3.metric("📊 Total Consultas", int(medico_info['Total Consultas']))
                col_info4.metric("👥 Pacientes", int(medico_info['Pacientes Atendidos']))
                
                # Consultas do médico
                st.subheader("📋 Agenda de Consultas")
                query_consultas_med = f"""
                SELECT 
                    c.IdConsulta as 'ID',
                    c.Data_Hora as 'Data/Hora',
                    p.NomePac as 'Paciente',
                    p.CpfPaciente as 'CPF',
                    cl.NomeCli as 'Clínica'
                FROM Consulta c
                JOIN Paciente p ON c.CpfPaciente = p.CpfPaciente
                JOIN Clinica cl ON c.CodCli = cl.CodCli
                WHERE c.CodMed = '{cod_med_selecionado}'
                ORDER BY c.Data_Hora DESC
                """
                df_consultas_med = pd.read_sql(query_consultas_med, conn)
                
                if not df_consultas_med.empty:
                    st.dataframe(df_consultas_med, use_container_width=True, hide_index=True)
                    
                    # Gráfico de consultas por mês
                    df_consultas_med['Mes'] = pd.to_datetime(df_consultas_med['Data/Hora']).dt.to_period('M').astype(str)
                    df_agrupado = df_consultas_med.groupby('Mes').size().reset_index(name='Quantidade')
                    
                    fig = px.bar(df_agrupado, x='Mes', y='Quantidade', 
                               title=f"Consultas de {medico_info['Nome']} por Mês",
                               labels={'Mes': 'Mês', 'Quantidade': 'Número de Consultas'})
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Este médico ainda não tem consultas agendadas.")
        
            st.divider()

            # ==========================================================
            # C (CREATE) - Cadastrar Novo Médico
            # ==========================================================
            st.subheader("➕ Cadastrar Novo Médico")

            with st.form("form_add_medico_tab2"):
                st.caption("Código (CHAR 7, ex: MED0020), Nome e Especialidade são obrigatórios.")
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    cod_med = st.text_input("Código do Médico", max_chars=7, key="med_cod_create_tab2")
                    nome_med = st.text_input("Nome Completo", key="med_nome_create_tab2")
                    especialidade = st.text_input("Especialidade", key="med_esp_create_tab2")
                with col_f2:
                    genero = st.selectbox("Gênero", ["F", "M", "Outro"], key="med_gen_create_tab2")
                    telefone = st.text_input("Telefone", key="med_tel_create_tab2")
                    email = st.text_input("E-mail", key="med_email_create_tab2")
                
                submit_med = st.form_submit_button("Cadastrar Médico (CREATE)")

            if submit_med:
                cursor = conn.cursor()
                if cod_med and nome_med and especialidade:
                    try:
                        genero_db = genero[0].upper() if genero != "Outro" else "" 
                        query = "INSERT INTO Medico (CodMed, NomeMed, Genero, Telefone, Email, Especialidade) VALUES (%s, %s, %s, %s, %s, %s)"
                        cursor.execute(query, (cod_med, nome_med, genero_db, telefone, email, especialidade))
                        conn.commit()
                        st.success(f"Médico **{nome_med}** cadastrado com sucesso!")
                    except mysql.connector.Error as e:
                        st.error("❌ Erro ao cadastrar Médico: Código ou Email podem já existir.")
                    finally:
                        cursor.close()
                else:
                    st.error("Preencha todos os campos obrigatórios!")
            
            st.divider()

            # ==========================================================
            # U (UPDATE) - Atualizar Dados do Médico
            # ==========================================================
            st.subheader("🔄 Atualizar Dados do Médico")
            
            df_medicos_upd = pd.read_sql("SELECT CodMed, NomeMed FROM Medico", conn)
            lista_medicos = {row['CodMed']: row['NomeMed'] for index, row in df_medicos_upd.iterrows()}
            
            medico_selecionado = st.selectbox("Selecione o Médico para Atualizar", options=list(lista_medicos.keys()), format_func=lambda x: f"{x} - {lista_medicos[x]}", key="upd_med_sel_tab2")

            if medico_selecionado:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM Medico WHERE CodMed = %s", (medico_selecionado,))
                dados_atuais = cursor.fetchone()
                cursor.close()

                if dados_atuais:
                    with st.form("form_update_medico_tab2"):
                        st.markdown(f"**Atualizando:** {dados_atuais['NomeMed']} (Teste de **ON UPDATE CASCADE**)")
                        novo_email = st.text_input("Novo E-mail", value=dados_atuais['Email'] or "", key="email_upd_tab2")
                        novo_tel = st.text_input("Novo Telefone", value=dados_atuais['Telefone'] or "", key="tel_upd_tab2")
                        nova_esp = st.text_input("Nova Especialidade", value=dados_atuais['Especialidade'] or "", key="esp_upd_tab2")
                        
                        submit_update = st.form_submit_button("Atualizar Dados (UPDATE)")

                    if submit_update:
                        cursor = conn.cursor()
                        try:
                            query = "UPDATE Medico SET Email = %s, Telefone = %s, Especialidade = %s WHERE CodMed = %s"
                            cursor.execute(query, (novo_email, novo_tel, nova_esp, medico_selecionado))
                            conn.commit()
                            st.success(f"Médico **{dados_atuais['NomeMed']}** atualizado com sucesso!")
                        except mysql.connector.Error as e:
                            st.error(f"❌ Erro ao atualizar dados: {e}")
                        finally:
                            cursor.close()
            
            st.divider()

            # ==========================================================
            # D (DELETE) - Remover Médico
            # ==========================================================
            st.subheader("🗑️ Remover Médico")
            
            df_medicos_del = pd.read_sql("SELECT CodMed, NomeMed FROM Medico", conn)
            lista_medicos_del = {row['CodMed']: row['NomeMed'] for index, row in df_medicos_del.iterrows()}
            
            medico_deletar = st.selectbox("Selecione o Médico para Deletar", options=list(lista_medicos_del.keys()), format_func=lambda x: f"{x} - {lista_medicos_del[x]}", key='del_med_tab2')

            delete_button = st.button("CONFIRMAR EXCLUSÃO (DELETE)", type="primary", key="del_medico_btn")
            if delete_button and medico_deletar:
                cursor = conn.cursor()
                try:
                    st.warning("A exclusão testará o **ON DELETE RESTRICT** (Violação de FK).")
                    cursor.execute("DELETE FROM Medico WHERE CodMed = %s", (medico_deletar,))
                    conn.commit()
                    st.success(f"✅ Médico {medico_deletar} removido com sucesso!")
                except mysql.connector.IntegrityError as e:
                    st.error("❌ ERRO: Violação de Integridade Referencial (FK).")
                    st.warning("Este médico possui consultas agendadas. Remova-as primeiro!")
                except mysql.connector.Error as e:
                    st.error(f"❌ Erro ao deletar Médico: {e}")
                finally:
                    cursor.close()

        # ========== ABA CLÍNICAS ==========
        with tab3:
            st.header("Gerenciar Clínicas")
            
            # Busca de Clínicas
            col_search1, col_search2 = st.columns([3, 1])
            with col_search1:
                busca_clinica = st.text_input("🔍 Buscar clínica por nome", key="busca_cli_tab3")
            with col_search2:
                st.write("")
                st.write("")
                btn_limpar_cli = st.button("🔄 Limpar", key="limpar_cli_tab3")
            
            # Query base (READ)
            query_clinicas = """
            SELECT 
                cl.CodCli as 'Código',
                cl.NomeCli as 'Nome',
                cl.Endereco as 'Endereço',
                cl.Telefone,
                COUNT(c.IdConsulta) as 'Total Consultas'
            FROM Clinica cl
            LEFT JOIN Consulta c ON cl.CodCli = c.CodCli
            """
            
            if busca_clinica and not btn_limpar_cli:
                query_clinicas += f" WHERE cl.NomeCli LIKE '%{busca_clinica}%'"
            
            query_clinicas += " GROUP BY cl.CodCli, cl.NomeCli, cl.Endereco, cl.Telefone ORDER BY cl.NomeCli ASC"
            
            df_clinicas = pd.read_sql(query_clinicas, conn)
            
            st.subheader(f"📊 Total de Clínicas: {len(df_clinicas)}")
            st.dataframe(df_clinicas, use_container_width=True, hide_index=True)
            
            # Detalhes da Clínica Selecionada
            st.divider()
            st.subheader("🔍 Detalhes da Clínica")
            
            cod_cli_selecionado = st.selectbox("Selecione uma clínica", df_clinicas['Código'].tolist() if not df_clinicas.empty else [], key="sel_cli_tab3")
            
            if cod_cli_selecionado:
                clinica_info = df_clinicas[df_clinicas['Código'] == cod_cli_selecionado].iloc[0]
                
                col_info1, col_info2, col_info3 = st.columns(3)
                col_info1.metric("🏥 Nome", clinica_info['Nome'])
                col_info2.metric("📍 Endereço", clinica_info['Endereço'])
                col_info3.metric("📊 Total Consultas", int(clinica_info['Total Consultas']))
                
                # Consultas da clínica
                st.subheader("📋 Consultas Realizadas")
                query_consultas_cli = f"""
                SELECT 
                    c.IdConsulta as 'ID',
                    c.Data_Hora as 'Data/Hora',
                    p.NomePac as 'Paciente',
                    m.NomeMed as 'Médico',
                    m.Especialidade
                FROM Consulta c
                JOIN Paciente p ON c.CpfPaciente = p.CpfPaciente
                JOIN Medico m ON c.CodMed = m.CodMed
                WHERE c.CodCli = '{cod_cli_selecionado}'
                ORDER BY c.Data_Hora DESC
                """
                df_consultas_cli = pd.read_sql(query_consultas_cli, conn)
                
                if not df_consultas_cli.empty:
                    st.dataframe(df_consultas_cli, use_container_width=True, hide_index=True)
                    
                    # Distribuição por especialidade
                    df_esp_dist = df_consultas_cli.groupby('Especialidade').size().reset_index(name='Quantidade')
                    
                    col_chart1, col_chart2 = st.columns(2)
                    
                    with col_chart1:
                        fig_pie = px.pie(df_esp_dist, values='Quantidade', names='Especialidade',
                                       title=f"Distribuição de Especialidades na {clinica_info['Nome']}")
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    with col_chart2:
                        fig_bar = px.bar(df_esp_dist, x='Especialidade', y='Quantidade',
                                       title="Consultas por Especialidade",
                                       color='Quantidade')
                        st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("Esta clínica ainda não tem consultas agendadas.")
        
            st.divider()

            # ==========================================================
            # C (CREATE) - Cadastrar Nova Clínica
            # ==========================================================
            st.subheader("➕ Cadastrar Nova Clínica")
            
            with st.form("form_add_clinica_tab3"):
                st.caption("Código (CHAR 7, ex: 0000009) e Nome são obrigatórios.")
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    cod_cli = st.text_input("Código da Clínica", max_chars=7, key="cli_cod_create_tab3")
                    nome_cli = st.text_input("Nome da Clínica", key="cli_nome_create_tab3")
                    endereco = st.text_input("Endereço", key="cli_end_create_tab3")
                with col_f2:
                    telefone = st.text_input("Telefone", key="cli_tel_create_tab3")
                    email = st.text_input("E-mail", key="cli_email_create_tab3")
                
                submit_cli = st.form_submit_button("Cadastrar Clínica (CREATE)")

            if submit_cli:
                cursor = conn.cursor()
                if cod_cli and nome_cli:
                    try:
                        query = "INSERT INTO Clinica (CodCli, NomeCli, Endereco, Telefone, Email) VALUES (%s, %s, %s, %s, %s)"
                        cursor.execute(query, (cod_cli, nome_cli, endereco, telefone, email))
                        conn.commit()
                        st.success(f"Clínica **{nome_cli}** cadastrada com sucesso!")
                    except mysql.connector.Error as e:
                        st.error("❌ Erro ao cadastrar Clínica: Código ou Nome podem já existir.")
                    finally:
                        cursor.close()
                else:
                    st.error("Preencha todos os campos obrigatórios!")
            
            st.divider()

            # ==========================================================
            # U (UPDATE) - Atualizar Dados da Clínica
            # ==========================================================
            st.subheader("🔄 Atualizar Dados da Clínica")
            
            df_clinicas_upd = pd.read_sql("SELECT CodCli, NomeCli FROM Clinica", conn)
            lista_clinicas = {row['CodCli']: row['NomeCli'] for index, row in df_clinicas_upd.iterrows()}
            
            clinica_selecionada = st.selectbox("Selecione a Clínica para Atualizar", options=list(lista_clinicas.keys()), format_func=lambda x: f"{x} - {lista_clinicas[x]}", key="upd_cli_sel_tab3")

            if clinica_selecionada:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM Clinica WHERE CodCli = %s", (clinica_selecionada,))
                dados_atuais = cursor.fetchone()
                cursor.close()

                if dados_atuais:
                    with st.form("form_update_clinica_tab3"):
                        st.markdown(f"**Atualizando:** {dados_atuais['NomeCli']} (Teste de **ON UPDATE CASCADE**)")
                        novo_endereco = st.text_input("Novo Endereço", value=dados_atuais['Endereco'] or "", key="end_upd_tab3")
                        novo_tel = st.text_input("Novo Telefone", value=dados_atuais['Telefone'] or "", key="tel_upd_tab3")
                        novo_email = st.text_input("Novo E-mail", value=dados_atuais['Email'] or "", key="email_upd_tab3")
                        
                        submit_update = st.form_submit_button("Atualizar Dados (UPDATE)")

                    if submit_update:
                        cursor = conn.cursor()
                        try:
                            query = "UPDATE Clinica SET Endereco = %s, Telefone = %s, Email = %s WHERE CodCli = %s"
                            cursor.execute(query, (novo_endereco, novo_tel, novo_email, clinica_selecionada))
                            conn.commit()
                            st.success(f"Clínica **{dados_atuais['NomeCli']}** atualizada com sucesso!")
                        except mysql.connector.Error as e:
                            st.error(f"❌ Erro ao atualizar dados: {e}")
                        finally:
                            cursor.close()
            
            st.divider()

            # ==========================================================
            # D (DELETE) - Remover Clínica
            # ==========================================================
            st.subheader("🗑️ Remover Clínica")
            
            df_clinicas_del = pd.read_sql("SELECT CodCli, NomeCli FROM Clinica", conn)
            lista_clinicas_del = {row['CodCli']: row['NomeCli'] for index, row in df_clinicas_del.iterrows()}
            
            clinica_deletar = st.selectbox("Selecione a Clínica para Deletar", options=list(lista_clinicas_del.keys()), format_func=lambda x: f"{x} - {lista_clinicas_del[x]}", key='del_cli_tab3')

            delete_button = st.button("CONFIRMAR EXCLUSÃO (DELETE)", type="primary", key="del_clinica_btn")

            if delete_button and clinica_deletar:
                cursor = conn.cursor()
                try:
                    st.warning("A exclusão testará o **ON DELETE RESTRICT** (Violação de FK).")
                    cursor.execute("DELETE FROM Clinica WHERE CodCli = %s", (clinica_deletar,))
                    conn.commit()
                    st.success(f"✅ Clínica {clinica_deletar} removida com sucesso!")
                except mysql.connector.IntegrityError as e:
                    st.error("❌ ERRO: Violação de Integridade Referencial (FK).")
                    st.warning("Esta clínica possui consultas agendadas. Remova-as primeiro!")
                except mysql.connector.Error as e:
                    st.error(f"❌ Erro ao deletar Clínica: {e}")
                finally:
                    cursor.close()

        conn.close()

# ==============================================================================
# PÁGINA 4: AUDITORIA
# ==============================================================================
elif pagina == "Auditoria (Trigger)":
    st.title("🕵️ Auditoria e Recuperação de Consultas")
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        
        # === LOG DE CANCELAMENTOS ===
        st.header("📋 Histórico de Cancelamentos")
        
        # Filtros para o log
        col_filtro1, col_filtro2 = st.columns(2)
        with col_filtro1:
            filtrar_por_data = st.checkbox("Filtrar por período")
            if filtrar_por_data:
                data_inicio_log = st.date_input("Data Início do Log", value=pd.to_datetime("2015-01-01"), key="log_inicio")
                data_fim_log = st.date_input("Data Fim do Log", value=pd.to_datetime("2036-12-29"), key="log_fim")
        
        # Query do log - usando SELECT * para pegar todas as colunas como estão
        if filtrar_por_data:
            query_log = f"""
            SELECT * FROM Log_Cancelamento 
            WHERE DATE(DataCancelamento) BETWEEN '{data_inicio_log}' AND '{data_fim_log}'
            ORDER BY DataCancelamento DESC
            """
        else:
            query_log = """
            SELECT * FROM Log_Cancelamento 
            ORDER BY DataCancelamento DESC
            """
        
        df_log = pd.read_sql(query_log, conn)
        
        if not df_log.empty:
            st.success(f"📊 Total de {len(df_log)} consulta(s) cancelada(s) registrada(s)")
            st.dataframe(df_log, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma consulta cancelada no período selecionado.")
        
        st.divider()
        
        # === CONSULTAS RECUPERADAS ===
        st.header("🔄 Consultas Recuperadas")
        st.info("💡 Apenas consultas que foram canceladas e depois recuperadas através desta ferramenta")
        
        # Para identificar consultas recuperadas, vamos verificar:
        # 1. Consultas muito recentes (criadas há menos de 1 hora - provavelmente são recuperações)
        # 2. Ou criar uma tabela de controle (mais robusto)
        
        # Por enquanto, vamos mostrar consultas criadas recentemente após haver cancelamentos no log
        if not df_log.empty:
            query_recentes = """
            SELECT 
                c.IdConsulta,
                c.Data_Hora as DataConsulta,
                p.NomePac as Paciente,
                m.NomeMed as Medico,
                cl.NomeCli as Clinica,
                TIMESTAMPDIFF(MINUTE, NOW(), c.Data_Hora) as MinutosAteFuturo
            FROM Consulta c
            JOIN Paciente p ON c.CpfPaciente = p.CpfPaciente
            JOIN Medico m ON c.CodMed = m.CodMed
            JOIN Clinica cl ON c.CodCli = cl.CodCli
            WHERE c.IdConsulta > (SELECT COALESCE(MAX(IdConsultaDeletada), 0) FROM Log_Cancelamento)
            ORDER BY c.IdConsulta DESC
            LIMIT 10
            """
            
            try:
                df_recuperadas = pd.read_sql(query_recentes, conn)
                
                if not df_recuperadas.empty:
                    st.success(f"🔄 {len(df_recuperadas)} consulta(s) recuperada(s) identificada(s)")
                    
                    # Remover coluna de minutos para exibição
                    df_display = df_recuperadas[['IdConsulta', 'DataConsulta', 'Paciente', 'Medico', 'Clinica']]
                    st.dataframe(df_display, use_container_width=True, hide_index=True)
                    
                    st.caption("📌 Consultas com ID maior que o último cancelamento registrado")
                else:
                    st.info("Nenhuma consulta recuperada identificada ainda.")
            except Exception as e:
                st.warning("⚠️ Não foi possível identificar consultas recuperadas automaticamente.")
                st.caption("Dica: Consultas recuperadas terão IDs maiores que as canceladas.")
        else:
            st.info("Sem histórico de cancelamentos. Recupere uma consulta para vê-la aqui!")
        
        st.divider()
        
        # === RECUPERAÇÃO DE CONSULTAS ===
        st.header("🔄 Recuperar Consulta Cancelada")
        st.info("💡 Você pode restaurar uma consulta cancelada desde que os dados ainda estejam disponíveis no log.")
        
        if not df_log.empty:
            # Seleção da consulta a recuperar
            col_recuperar1, col_recuperar2 = st.columns([2, 1])
            
            with col_recuperar1:
                # Criar lista de opções formatadas usando os nomes reais das colunas
                opcoes_recuperacao = []
                
                # Detectar nomes das colunas dinamicamente
                col_names = df_log.columns.tolist()
                
                for idx, row in df_log.iterrows():
                    # Usar o primeiro campo como ID (geralmente é o ID ou índice)
                    id_col = col_names[0]
                    opcao = f"ID {row[id_col]} - "
                    
                    # Adicionar data se existir
                    for col in col_names:
                        if 'data' in col.lower() and 'cancelamento' not in col.lower():
                            opcao += f"{row[col]} - "
                            break
                    
                    # Adicionar CPF se existir
                    for col in col_names:
                        if 'cpf' in col.lower():
                            opcao += f"CPF: {row[col]}"
                            break
                    
                    opcoes_recuperacao.append(opcao)
                
                consulta_selecionada = st.selectbox(
                    "Selecione a consulta para recuperar",
                    opcoes_recuperacao if opcoes_recuperacao else ["Nenhuma consulta disponível"]
                )
            
            if consulta_selecionada != "Nenhuma consulta disponível":
                # Extrair ID da consulta selecionada
                id_recuperar = int(consulta_selecionada.split(" - ")[0].replace("ID ", ""))
                
                # Buscar detalhes da consulta no log usando o nome da primeira coluna
                col_id = df_log.columns[0]
                log_info = df_log[df_log[col_id] == id_recuperar].iloc[0]
                
                st.subheader("📋 Detalhes da Consulta Cancelada")
                
                # Encontrar as colunas dinamicamente
                col_names = df_log.columns.tolist()
                
                # Exibir métricas com os dados disponíveis
                cols_metricas = st.columns(len(col_names))
                for i, col_name in enumerate(col_names):
                    cols_metricas[i].metric(col_name, str(log_info[col_name]))
                
                # Buscar informações adicionais
                st.subheader("📝 Inserir Dados para Recuperação")
                
                # Formulário para entrada manual de dados
                with st.form("form_recuperacao", clear_on_submit=False):
                    st.write("Preencha os dados da consulta que deseja recuperar:")
                    
                    # Buscar listas de opções
                    medicos_disp = pd.read_sql("SELECT CodMed, NomeMed, Especialidade FROM Medico ORDER BY NomeMed", conn)
                    pacientes_disp = pd.read_sql("SELECT CpfPaciente, NomePac FROM Paciente ORDER BY NomePac", conn)
                    clinicas_disp = pd.read_sql("SELECT CodCli, NomeCli FROM Clinica ORDER BY NomeCli", conn)
                    
                    col_form1, col_form2 = st.columns(2)
                    
                    with col_form1:
                        if not pacientes_disp.empty:
                            pac_opcoes = [f"{row['CpfPaciente']} - {row['NomePac']}" for _, row in pacientes_disp.iterrows()]
                            pac_selecionado = st.selectbox("👤 Selecione o Paciente", pac_opcoes)
                            cpf_valor = pac_selecionado.split(" - ")[0]
                        else:
                            cpf_valor = st.text_input("👤 CPF do Paciente", max_chars=11)
                        
                        if not clinicas_disp.empty:
                            cli_opcoes = [f"{row['CodCli']} - {row['NomeCli']}" for _, row in clinicas_disp.iterrows()]
                            cli_selecionado = st.selectbox("🏥 Selecione a Clínica", cli_opcoes)
                            cli_valor = cli_selecionado.split(" - ")[0]
                        else:
                            cli_valor = st.text_input("🏥 Código da Clínica")
                    
                    with col_form2:
                        if not medicos_disp.empty:
                            med_opcoes = [f"{row['CodMed']} - {row['NomeMed']} ({row['Especialidade']})" for _, row in medicos_disp.iterrows()]
                            med_selecionado = st.selectbox("👨‍⚕️ Selecione o Médico", med_opcoes)
                            med_valor = med_selecionado.split(" - ")[0]
                        else:
                            med_valor = st.text_input("👨‍⚕️ Código do Médico")
                        
                        import datetime
                        data_consulta_rec = st.date_input("📅 Data da Consulta", value=datetime.date.today())
                        hora_consulta_rec = st.time_input("🕐 Hora da Consulta", value=datetime.time(10, 0))
                    
                    data_hora_original = datetime.datetime.combine(data_consulta_rec, hora_consulta_rec).strftime("%Y-%m-%d %H:%M:%S")
                    
                    submit_form_rec = st.form_submit_button("✅ Confirmar Dados", type="primary", use_container_width=True)
                
                # Exibir resumo após confirmação
                if submit_form_rec:
                    st.success("✅ Dados confirmados! Role para baixo para recuperar a consulta.")
                
                st.divider()
                
                # Verificações antes de recuperar
                st.subheader("✅ Verificações de Integridade")
                
                verificacoes_ok = True
                
                # Só fazer verificações se conseguimos buscar os dados
                if cpf_valor and med_valor and cli_valor:
                    # Verificar se o paciente existe
                    query_check_pac = f"SELECT NomePac FROM Paciente WHERE CpfPaciente = '{cpf_valor}'"
                    df_check_pac = pd.read_sql(query_check_pac, conn)
                    
                    if df_check_pac.empty:
                        st.error(f"❌ Paciente com CPF {cpf_valor} não existe mais no sistema")
                        verificacoes_ok = False
                    
                    # Verificar se o médico existe
                    query_check_med = f"SELECT NomeMed FROM Medico WHERE CodMed = '{med_valor}'"
                    df_check_med = pd.read_sql(query_check_med, conn)
                    
                    if df_check_med.empty:
                        st.error(f"❌ Médico com código {med_valor} não existe mais no sistema")
                        verificacoes_ok = False
                    
                    # Verificar se a clínica existe
                    query_check_cli = f"SELECT NomeCli FROM Clinica WHERE CodCli = '{cli_valor}'"
                    df_check_cli = pd.read_sql(query_check_cli, conn)
                    
                    if df_check_cli.empty:
                        st.error(f"❌ Clínica com código {cli_valor} não existe mais no sistema")
                        verificacoes_ok = False
                    
                    # VERIFICAÇÃO DE DUPLICAÇÃO
                    if data_hora_original and verificacoes_ok:
                        query_check_duplicada = f"""
                        SELECT IdConsulta, Data_Hora 
                        FROM Consulta 
                        WHERE CpfPaciente = '{cpf_valor}' 
                        AND CodMed = '{med_valor}' 
                        AND CodCli = '{cli_valor}'
                        AND Data_Hora = '{data_hora_original}'
                        """
                        df_check_dup = pd.read_sql(query_check_duplicada, conn)
                        
                        if not df_check_dup.empty:
                            st.error(f"❌ JÁ EXISTE consulta idêntica (ID: {df_check_dup['IdConsulta'][0]} em {df_check_dup['Data_Hora'][0]})")
                            st.info("💡 Esta consulta já foi recuperada anteriormente ou nunca foi deletada.")
                            verificacoes_ok = False
                    
                    # Mostrar sucesso apenas se tudo estiver OK
                    if verificacoes_ok:
                        st.success("✅ Todos os dados validados! Pode recuperar a consulta.")
                else:
                    st.error("❌ Não foi possível obter os dados necessários para recuperação")
                    verificacoes_ok = False
                
                # Verificar conflito de horário
                # Inicializar data_hora_recuperacao
                data_hora_recuperacao = None
                
                if med_valor and data_hora_original:
                    try:
                        query_check_horario = f"""
                        SELECT COUNT(*) as conflito 
                        FROM Consulta 
                        WHERE CodMed = '{med_valor}' 
                        AND Data_Hora = '{data_hora_original}'
                        """
                        df_check_horario = pd.read_sql(query_check_horario, conn)
                        
                        if df_check_horario['conflito'][0] > 0:
                            st.warning("⚠️ O médico já tem consulta agendada neste horário. Escolha um novo horário:")
                            nova_data = st.date_input("Nova Data", value=pd.to_datetime(data_hora_original).date(), key="nova_data_rec")
                            nova_hora = st.time_input("Nova Hora", value=pd.to_datetime(data_hora_original).time(), key="nova_hora_rec")
                            import datetime
                            data_hora_recuperacao = datetime.datetime.combine(nova_data, nova_hora).strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            st.success(f"✅ Horário disponível: {data_hora_original}")
                            data_hora_recuperacao = str(data_hora_original)
                    except Exception as e:
                        st.warning(f"⚠️ Não foi possível verificar conflito de horário. Você pode definir manualmente:")
                        import datetime
                        nova_data = st.date_input("Data da Consulta", value=datetime.date.today(), key="manual_data_rec")
                        nova_hora = st.time_input("Hora da Consulta", value=datetime.datetime.now().time(), key="manual_hora_rec")
                        data_hora_recuperacao = datetime.datetime.combine(nova_data, nova_hora).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    st.warning("⚠️ Defina manualmente a data e hora da consulta:")
                    import datetime
                    nova_data = st.date_input("Data da Consulta", value=datetime.date.today(), key="manual_data_rec2")
                    nova_hora = st.time_input("Hora da Consulta", value=datetime.datetime.now().time(), key="manual_hora_rec2")
                    data_hora_recuperacao = datetime.datetime.combine(nova_data, nova_hora).strftime("%Y-%m-%d %H:%M:%S")
                
                st.divider()
                
                # Botão de recuperação
                col_btn1, col_btn2 = st.columns([1, 3])
                
                with col_btn1:
                    if verificacoes_ok and cpf_valor and med_valor and cli_valor and data_hora_recuperacao:
                        if st.button("🔄 RECUPERAR CONSULTA", type="primary", use_container_width=True):
                            try:
                                # Inserir a consulta novamente (sem especificar ID, será auto-incrementado)
                                query_recuperar = """
                                INSERT INTO Consulta (CodCli, CodMed, CpfPaciente, Data_Hora) 
                                VALUES (%s, %s, %s, %s)
                                """
                                cursor.execute(query_recuperar, (
                                    cli_valor,
                                    med_valor,
                                    cpf_valor,
                                    data_hora_recuperacao
                                ))
                                conn.commit()
                                
                                if cursor.rowcount > 0:
                                    # Obter o ID gerado
                                    novo_id_gerado = cursor.lastrowid
                                    st.success(f"✅ Consulta recuperada com sucesso! Novo ID: {novo_id_gerado}")
                                    st.balloons()
                                    
                                    # Opcionalmente, remover do log
                                    remover_log = st.checkbox("Remover esta entrada do log de cancelamentos?")
                                    if remover_log:
                                        cursor.execute(f"DELETE FROM Log_Cancelamento WHERE {col_id} = {id_recuperar}")
                                        conn.commit()
                                        st.info("Registro removido do log de cancelamentos.")
                                else:
                                    st.error("Erro ao recuperar consulta.")
                                    
                            except mysql.connector.Error as e:
                                st.error(f"Erro ao recuperar consulta: {e}")
                    else:
                        st.button("🔄 RECUPERAR CONSULTA", disabled=True, use_container_width=True)
                        st.warning("⚠️ Corrija os problemas acima antes de recuperar")
        else:
            st.info("Não há consultas canceladas para recuperar no momento.")
        
        conn.close()