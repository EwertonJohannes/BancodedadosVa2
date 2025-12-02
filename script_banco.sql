-- 1. Criação do Banco de Dados
CREATE DATABASE IF NOT EXISTS ConsultasMedicas;
USE ConsultasMedicas;

-- 2. Criação das Tabelas
-- Tabela Clínica
CREATE TABLE IF NOT EXISTS Clinica (
    CodCli CHAR(7) PRIMARY KEY, -- CHAR mantém os zeros à esquerda (ex: 0000001)
    NomeCli VARCHAR(100) NOT NULL,
    Endereco VARCHAR(150),
    Telefone VARCHAR(20),
    Email VARCHAR(100)
);

-- Tabela Médico
CREATE TABLE IF NOT EXISTS Medico (
    CodMed CHAR(7) PRIMARY KEY,
    NomeMed VARCHAR(100) NOT NULL,
    Genero CHAR(1), -- M ou F
    Telefone VARCHAR(20),
    Email VARCHAR(100),
    Especialidade VARCHAR(50)
);

-- Tabela Paciente
CREATE TABLE IF NOT EXISTS Paciente (
    CpfPaciente CHAR(11) PRIMARY KEY, -- CPF sem pontos/traços para facilitar busca
    NomePac VARCHAR(100) NOT NULL,
    DataNascimento DATE,
    Genero CHAR(1),
    Telefone VARCHAR(20),
    Email VARCHAR(100)
);

-- Tabela Consulta
CREATE TABLE IF NOT EXISTS Consulta (
    IdConsulta INT AUTO_INCREMENT PRIMARY KEY, -- Identificador único para facilitar o CRUD (Delete/Update) no sistema Web
    CodCli CHAR(7),
    CodMed CHAR(7),
    CpfPaciente CHAR(11),
    Data_Hora DATETIME,
    
    -- Definição das Chaves Estrangeiras (FK) com CASCADE 
    -- 1. CLINICA: Configurada para CAUSAR ERRO ao deletar (Violação de Integridade)
    FOREIGN KEY (CodCli) REFERENCES Clinica(CodCli) ON UPDATE CASCADE ON DELETE RESTRICT,
    -- 2. MEDICO: Configurada para ATUALIZAR EM CASCATA (Se mudar o ID do médico, muda na consulta)
    FOREIGN KEY (CodMed) REFERENCES Medico(CodMed) ON UPDATE CASCADE ON DELETE RESTRICT,
    -- 3. PACIENTE: Configurada para APAGAR EM CASCATA (Perigoso, mas bom para mostrar o Delete Cascade)
    -- Se você apagar o Paciente "Teste", as consultas dele somem sozinhas.
    FOREIGN KEY (CpfPaciente) REFERENCES Paciente(CpfPaciente) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- 3. População dos Dados 
-- ==========================================================
-- 1. POPULANDO CLÍNICAS (5 Unidades)
-- ==========================================================
INSERT INTO Clinica (CodCli, NomeCli, Endereco, Telefone, Email) VALUES
('0000001', 'Saúde Plus', 'Av. Rosa e Silva, 406', '(81) 4002-3633', 'saudeplus@mail.com'),
('0000002', 'Visão Recife', 'Av. Agamenon Magalhães, 810', '(81) 3042-1112', 'visaorecife@mail.com'),
('0000003', 'Vida Kids', 'Rua das Crianças, 100', '(81) 3333-4444', 'vidakids@mail.com'),
('0000004', 'OrtoCenter', 'Av. Boa Viagem, 500', '(81) 3465-7777', 'ortocenter@mail.com'),
('0000005', 'DermoEstética', 'Rua do Sol, 200', '(81) 3222-1111', 'dermo@mail.com');
INSERT INTO Clinica (CodCli, NomeCli, Endereco, Telefone, Email) VALUES
('0000006', 'Clínica Mente Sã', 'Rua da Harmonia, 300', '(81) 3268-0000', 'mentesa@mail.com'),
('0000007', 'Laboratório Precision', 'Av. Caxangá, 1500', '(81) 3455-9999', 'labprecision@mail.com'),
('0000008', 'Centro Geriátrico Viver Bem', 'Rua do Futuro, 88', '(81) 3030-5050', 'viverbem@mail.com');

-- ==========================================================
-- 2. POPULANDO MÉDICOS (10 Médicos - Várias Especialidades)
-- ==========================================================
INSERT INTO Medico (CodMed, NomeMed, Genero, Telefone, Email, Especialidade) VALUES
('MED0001', 'Dr. Roberto Silva', 'M', '98888-1111', 'roberto@mail.com', 'Cardiologia'),
('MED0002', 'Dra. Ana Clara', 'F', '97777-2222', 'anaclara@mail.com', 'Dermatologia'),
('MED0003', 'Dr. Jorge Mendes', 'M', '96666-3333', 'jorge@mail.com', 'Cardiologia'),
('MED0004', 'Dra. Patricia Lima', 'F', '95555-4444', 'patricia@mail.com', 'Pediatria'),
('MED0005', 'Dr. Lucas Carvalho', 'M', '98256-5703', 'lucas@mail.com', 'Oftalmologia'),
('MED0006', 'Dra. Marcela Gomes', 'F', '98273-3245', 'marcela@mail.com', 'Pediatria'),
('MED0007', 'Dr. Alexandre Alencar', 'M', '99482-4758', 'alexandre@mail.com', 'Oftalmologia'),
('MED0008', 'Dra. Carla Dias', 'F', '91111-2222', 'carla@mail.com', 'Ortopedia'),
-- MÉDICOS "FANTASMAS" (Para testar o LEFT JOIN - Sem consultas)
('MED0009', 'Dr. Gregory House', 'M', '90000-0000', 'house@mail.com', 'Diagnóstico'),
('MED0010', 'Dra. Grey', 'F', '91111-1111', 'grey@mail.com', 'Cirurgia Geral');

-- ==========================================================
-- 3. POPULANDO PACIENTES (20 Pessoas - Idades Variadas)
-- ==========================================================
INSERT INTO Paciente (CpfPaciente, NomePac, DataNascimento, Genero, Telefone, Email) VALUES
-- Idosos (Para média de idade alta)
('11111111111', 'Sr. João Silva', '1950-05-20', 'M', '9999-0001', 'joao@mail.com'),
('22222222222', 'Sra. Maria José', '1955-10-10', 'F', '9999-0002', 'maria@mail.com'),
('33333333333', 'Sr. Pedro Paulo', '1960-01-30', 'M', '9999-0003', 'pedro@mail.com'),
-- Adultos (1980-1990)
('44444444444', 'Carlos Santana', '1985-06-15', 'M', '9999-0004', 'carlos@mail.com'),
('55555555555', 'Fernanda Lima', '1990-12-25', 'F', '9999-0005', 'nanda@mail.com'),
('66666666666', 'Roberto Justus', '1982-03-12', 'M', '9999-0006', 'justus@mail.com'),
('77777777777', 'Ana Paula Padrão', '1988-07-07', 'F', '9999-0007', 'ana@mail.com'),
('88888888888', 'Tiago Leifert', '1980-09-09', 'M', '9999-0008', 'tiago@mail.com'),
('99999999999', 'Ivete Sangalo', '1975-05-27', 'F', '9999-0009', 'ivete@mail.com'),
('10101010101', 'Fausto Silva', '1965-02-02', 'M', '9999-0010', 'fausto@mail.com'),
-- Jovens e Crianças (Para Pediatria)
('12121212121', 'Menino Ney', '2015-02-05', 'M', '9999-0011', 'ney@mail.com'),
('13131313131', 'Menina Maisa', '2010-05-22', 'F', '9999-0012', 'maisa@mail.com'),
('14141414141', 'Bebê George', '2023-01-01', 'M', '9999-0013', 'geo@mail.com'),
('15151515151', 'Larissa Manoela', '2005-12-28', 'F', '9999-0014', 'lari@mail.com'),
('16161616161', 'MC Cabelinho', '2000-01-20', 'M', '9999-0015', 'mc@mail.com'),
-- Recorrentes (Vão ter muitas consultas)
('17171717171', 'Cliente Fiel', '1995-05-05', 'M', '9999-0016', 'fiel@mail.com'),
('18181818181', 'Hipocondríaco Junior', '1998-08-08', 'M', '9999-0017', 'hipo@mail.com'),
('19191919191', 'Dona Florinda', '1962-02-14', 'F', '9999-0018', 'flor@mail.com'),
('20202020202', 'Chaves do 8', '2016-06-20', 'M', '9999-0019', 'chaves@mail.com'),
('21212121212', 'Chiquinha', '2016-10-10', 'F', '9999-0020', 'chiq@mail.com');

-- ==========================================================
-- 4. POPULANDO CONSULTAS (Distribuídas 2023-2026)
-- ==========================================================
INSERT INTO Consulta (CodCli, CodMed, CpfPaciente, Data_Hora) VALUES
-- ANO 2023 
('0000001', 'MED0001', '11111111111', '2023-05-10 08:00:00'),
('0000001', 'MED0001', '33333333333', '2023-06-15 09:30:00'),
('0000002', 'MED0005', '44444444444', '2023-07-20 14:00:00'),
('0000003', 'MED0004', '12121212121', '2023-08-05 10:00:00'),
('0000001', 'MED0003', '17171717171', '2023-09-12 11:00:00'),
('0000005', 'MED0002', '55555555555', '2023-10-30 15:00:00'),
('0000004', 'MED0008', '66666666666', '2023-11-11 16:00:00'),
('0000001', 'MED0001', '11111111111', '2023-12-01 08:30:00'), 
('0000003', 'MED0006', '14141414141', '2023-12-15 09:00:00'),
('0000001', 'MED0001', '19191919191', '2023-12-20 10:30:00'),

-- ANO 2024 
('0000001', 'MED0001', '11111111111', '2024-01-10 08:00:00'),
('0000002', 'MED0007', '22222222222', '2024-02-15 14:00:00'),
('0000003', 'MED0004', '20202020202', '2024-02-20 09:00:00'),
('0000005', 'MED0002', '77777777777', '2024-03-05 16:30:00'),
('0000001', 'MED0003', '18181818181', '2024-03-10 11:00:00'), 
('0000001', 'MED0003', '18181818181', '2024-03-15 11:00:00'), 
('0000001', 'MED0003', '18181818181', '2024-03-20 11:00:00'), 
('0000004', 'MED0008', '16161616161', '2024-04-01 15:00:00'),
('0000002', 'MED0005', '88888888888', '2024-05-12 10:00:00'),
('0000002', 'MED0007', '99999999999', '2024-06-15 14:30:00'),
('0000003', 'MED0006', '13131313131', '2024-07-20 09:15:00'),
('0000001', 'MED0001', '10101010101', '2024-08-05 17:00:00'),
('0000005', 'MED0002', '21212121212', '2024-08-10 13:00:00'),
('0000001', 'MED0001', '11111111111', '2024-09-01 08:00:00'), 
('0000004', 'MED0008', '15151515151', '2024-09-15 16:00:00'),
('0000003', 'MED0004', '14141414141', '2024-10-02 10:00:00'),
('0000001', 'MED0003', '17171717171', '2024-10-15 11:30:00'),
('0000002', 'MED0005', '44444444444', '2024-11-01 14:00:00'),
('0000002', 'MED0005', '66666666666', '2024-11-05 14:30:00'),
('0000001', 'MED0001', '19191919191', '2024-11-20 09:00:00'),
('0000005', 'MED0002', '55555555555', '2024-12-01 15:15:00'),
('0000003', 'MED0006', '12121212121', '2024-12-10 08:45:00'),
('0000004', 'MED0008', '16161616161', '2024-12-15 16:00:00'),
('0000001', 'MED0003', '18181818181', '2024-12-20 11:00:00'), 
('0000002', 'MED0007', '22222222222', '2024-12-28 13:00:00'),

-- ANO 2025 
('0000001', 'MED0001', '11111111111', '2025-01-15 08:00:00'),
('0000002', 'MED0005', '88888888888', '2025-02-10 14:00:00'),
('0000003', 'MED0004', '20202020202', '2025-03-05 09:30:00'),
('0000005', 'MED0002', '77777777777', '2025-04-12 16:00:00'),
('0000001', 'MED0003', '18181818181', '2025-05-20 11:00:00'),
('0000004', 'MED0008', '66666666666', '2025-06-15 15:00:00'),
('0000002', 'MED0007', '99999999999', '2025-07-20 14:30:00'),
('0000003', 'MED0006', '13131313131', '2025-08-10 09:00:00'),
('0000001', 'MED0001', '10101010101', '2025-09-05 17:00:00'),
('0000005', 'MED0002', '21212121212', '2025-10-15 13:00:00'),
('0000001', 'MED0003', '17171717171', '2025-11-01 11:30:00'),
('0000002', 'MED0005', '44444444444', '2025-11-20 14:00:00'),
('0000003', 'MED0004', '14141414141', '2025-12-05 10:00:00'),
('0000004', 'MED0008', '15151515151', '2025-12-15 16:30:00'),
('0000001', 'MED0001', '19191919191', '2025-12-22 09:00:00'),

-- ANO 2026 
('0000001', 'MED0001', '11111111111', '2026-01-10 08:00:00'),
('0000002', 'MED0007', '22222222222', '2026-02-15 14:00:00'),
('0000005', 'MED0002', '55555555555', '2026-03-20 15:00:00'),
('0000003', 'MED0006', '12121212121', '2026-04-10 08:30:00'),
('0000001', 'MED0003', '18181818181', '2026-05-15 11:00:00');
USE ConsultasMedicas;

-- ==========================================================
-- NOVOS MÉDICOS 
-- ==========================================================
INSERT INTO Medico (CodMed, NomeMed, Genero, Telefone, Email, Especialidade) VALUES
('MED0011', 'Dra. Julia Roberts', 'F', '98877-6655', 'julia@mail.com', 'Psiquiatria'),
('MED0012', 'Dr. Will Smith', 'M', '91111-0000', 'will@mail.com', 'Dermatologia'),
('MED0013', 'Dr. Drauzio Varella', 'M', '92222-1111', 'drauzio@mail.com', 'Infectologia'),
('MED0014', 'Dra. Nise da Silveira', 'F', '93333-2222', 'nise@mail.com', 'Psiquiatria'),
('MED0015', 'Dr. House MD', 'M', '94444-3333', 'house@mail.com', 'Diagnóstico'), 

('MED0016', 'Dr. Estranho', 'M', '95555-4444', 'strange@mail.com', 'Neurologia'), 
('MED0017', 'Dra. Meredith Grey', 'F', '96666-5555', 'meredith@mail.com', 'Cirurgia Geral'),
('MED0018', 'Dr. Dolittle', 'M', '97777-6666', 'dolittle@mail.com', 'Veterinária');

-- ==========================================================
--  NOVOS PACIENTES 
-- ==========================================================
INSERT INTO Paciente (CpfPaciente, NomePac, DataNascimento, Genero, Telefone, Email) VALUES
('30303030303', 'Vovó Palmirinha', '1931-06-29', 'F', '9999-0030', 'vovo@mail.com'),
('40404040404', 'Silvio Santos', '1930-12-12', 'M', '9999-0040', 'silvio@mail.com'),
('50505050505', 'Tony Stark', '1970-05-29', 'M', '9999-0050', 'tony@mail.com'),
('60606060606', 'Natasha Romanoff', '1984-11-22', 'F', '9999-0060', 'nat@mail.com'),
('70707070707', 'Peter Parker', '2001-08-10', 'M', '9999-0070', 'spidey@mail.com'),
('80808080808', 'Wanda Maximoff', '1989-02-10', 'F', '9999-0080', 'wanda@mail.com'),
('90909090909', 'Bruce Banner', '1969-12-18', 'M', '9999-0090', 'hulk@mail.com'),
('01010101010', 'Eleven Stranger', '2011-02-19', 'F', '9999-0099', 'eleven@mail.com');

-- ==========================================================
-- NOVAS CONSULTAS 
-- ==========================================================
INSERT INTO Consulta (CodCli, CodMed, CpfPaciente, Data_Hora) VALUES
-- 2022 
('0000006', 'MED0011', '80808080808', '2022-06-15 14:00:00'), 
('0000006', 'MED0011', '80808080808', '2022-07-15 14:00:00'), 
('0000006', 'MED0011', '80808080808', '2022-08-15 14:00:00'), 
('0000001', 'MED0001', '50505050505', '2022-12-20 10:00:00'), 

-- 2024 (Reforçando o ano atual com a nova Clínica Geriátrica)
('0000008', 'MED0001', '30303030303', '2024-05-10 08:00:00'), 
('0000008', 'MED0013', '40404040404', '2024-06-12 09:30:00'), 
('0000008', 'MED0003', '30303030303', '2024-07-20 11:00:00'), 
('0000006', 'MED0014', '90909090909', '2024-08-05 16:00:00'), 
('0000007', 'MED0015', '50505050505', '2024-09-01 07:00:00'), 
('0000007', 'MED0015', '60606060606', '2024-09-01 07:30:00'), 
('0000002', 'MED0012', '70707070707', '2024-10-12 14:00:00'),

-- 2025 (Futuro Próximo - Consultas Agendadas)
('0000006', 'MED0011', '80808080808', '2025-01-10 14:00:00'), 
('0000008', 'MED0001', '30303030303', '2025-03-15 08:30:00'), 
('0000003', 'MED0004', '01010101010', '2025-04-20 10:00:00'), 
('0000003', 'MED0006', '20202020202', '2025-05-05 09:00:00'), 
('0000007', 'MED0015', '11111111111', '2025-06-10 07:00:00'), 
('0000004', 'MED0008', '70707070707', '2025-07-15 15:30:00'),


('0000008', 'MED0003', '40404040404', '2026-06-01 10:00:00'),
('0000006', 'MED0014', '90909090909', '2026-12-25 18:00:00'), 
('0000001', 'MED0001', '17171717171', '2027-01-15 08:00:00'), 
('0000002', 'MED0005', '18181818181', '2027-02-20 14:00:00'); 



CREATE TABLE IF NOT EXISTS Log_Cancelamento (
    IdLog INT AUTO_INCREMENT PRIMARY KEY,
    Usuario VARCHAR(50),
    DataCancelamento DATETIME,
    IdConsultaDeletada INT,
    Motivo VARCHAR(100)
);

-- Criar o Trigger
DELIMITER $$
CREATE TRIGGER trg_Auditoria_Cancelamento
AFTER DELETE ON Consulta
FOR EACH ROW
BEGIN
    INSERT INTO Log_Cancelamento (Usuario, DataCancelamento, IdConsultaDeletada, Motivo)
    VALUES (USER(), NOW(), OLD.IdConsulta, 'Consulta Removida pelo Sistema');
END$$
DELIMITER ;

-- GATILHO (TRIGGER) 2: PREVENÇÃO DE DATA RETROATIVA
DELIMITER $$
CREATE TRIGGER trg_Validar_Data_Consulta
BEFORE INSERT ON Consulta
FOR EACH ROW
BEGIN
    IF NEW.Data_Hora <= NOW() THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'ERRO DE INTEGRIDADE: Não é permitido agendar consultas para datas/horas passadas. Verifique a Data_Hora.';
    END IF;
END$$
DELIMITER ;