CREATE DATABASE  IF NOT EXISTS `consultasmedicas` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `consultasmedicas`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: consultasmedicas
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `clinica`
--

DROP TABLE IF EXISTS `clinica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clinica` (
  `CodCli` char(7) NOT NULL,
  `NomeCli` varchar(100) NOT NULL,
  `Endereco` varchar(150) DEFAULT NULL,
  `Telefone` varchar(20) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`CodCli`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clinica`
--

LOCK TABLES `clinica` WRITE;
/*!40000 ALTER TABLE `clinica` DISABLE KEYS */;
INSERT INTO `clinica` VALUES ('0000001','Saúde Plus','Av. Rosa e Silva, 406','(81) 4002-3633','saudeplus@mail.com'),('0000002','Visão Recife','Av. Agamenon Magalhães, 810','(81) 3042-1112','visaorecife@mail.com'),('0000003','Vida Kids','Rua das Crianças, 100','(81) 3333-4444','vidakids@mail.com'),('0000004','OrtoCenter','Av. Boa Viagem, 500','(81) 3465-7777','ortocenter@mail.com'),('0000005','DermoEstética','Rua do Sol, 200','(81) 3222-1111','dermo@mail.com');
/*!40000 ALTER TABLE `clinica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consulta`
--

DROP TABLE IF EXISTS `consulta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consulta` (
  `IdConsulta` int NOT NULL AUTO_INCREMENT,
  `CodCli` char(7) DEFAULT NULL,
  `CodMed` char(7) DEFAULT NULL,
  `CpfPaciente` char(11) DEFAULT NULL,
  `Data_Hora` datetime DEFAULT NULL,
  PRIMARY KEY (`IdConsulta`),
  KEY `CodCli` (`CodCli`),
  KEY `CodMed` (`CodMed`),
  KEY `CpfPaciente` (`CpfPaciente`),
  CONSTRAINT `consulta_ibfk_1` FOREIGN KEY (`CodCli`) REFERENCES `clinica` (`CodCli`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `consulta_ibfk_2` FOREIGN KEY (`CodMed`) REFERENCES `medico` (`CodMed`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `consulta_ibfk_3` FOREIGN KEY (`CpfPaciente`) REFERENCES `paciente` (`CpfPaciente`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consulta`
--

LOCK TABLES `consulta` WRITE;
/*!40000 ALTER TABLE `consulta` DISABLE KEYS */;
INSERT INTO `consulta` VALUES (1,'0000001','MED0001','11111111111','2023-05-10 08:00:00'),(2,'0000001','MED0001','33333333333','2023-06-15 09:30:00'),(3,'0000002','MED0005','44444444444','2023-07-20 14:00:00'),(4,'0000003','MED0004','12121212121','2023-08-05 10:00:00'),(5,'0000001','MED0003','17171717171','2023-09-12 11:00:00'),(6,'0000005','MED0002','55555555555','2023-10-30 15:00:00'),(7,'0000004','MED0008','66666666666','2023-11-11 16:00:00'),(8,'0000001','MED0001','11111111111','2023-12-01 08:30:00'),(9,'0000003','MED0006','14141414141','2023-12-15 09:00:00'),(10,'0000001','MED0001','19191919191','2023-12-20 10:30:00'),(11,'0000001','MED0001','11111111111','2024-01-10 08:00:00'),(12,'0000002','MED0007','22222222222','2024-02-15 14:00:00'),(13,'0000003','MED0004','20202020202','2024-02-20 09:00:00'),(14,'0000005','MED0002','77777777777','2024-03-05 16:30:00'),(15,'0000001','MED0003','18181818181','2024-03-10 11:00:00'),(16,'0000001','MED0003','18181818181','2024-03-15 11:00:00'),(17,'0000001','MED0003','18181818181','2024-03-20 11:00:00'),(18,'0000004','MED0008','16161616161','2024-04-01 15:00:00'),(19,'0000002','MED0005','88888888888','2024-05-12 10:00:00'),(20,'0000002','MED0007','99999999999','2024-06-15 14:30:00'),(21,'0000003','MED0006','13131313131','2024-07-20 09:15:00'),(22,'0000001','MED0001','10101010101','2024-08-05 17:00:00'),(23,'0000005','MED0002','21212121212','2024-08-10 13:00:00'),(24,'0000001','MED0001','11111111111','2024-09-01 08:00:00'),(25,'0000004','MED0008','15151515151','2024-09-15 16:00:00'),(26,'0000003','MED0004','14141414141','2024-10-02 10:00:00'),(27,'0000001','MED0003','17171717171','2024-10-15 11:30:00'),(28,'0000002','MED0005','44444444444','2024-11-01 14:00:00'),(29,'0000002','MED0005','66666666666','2024-11-05 14:30:00'),(30,'0000001','MED0001','19191919191','2024-11-20 09:00:00'),(31,'0000005','MED0002','55555555555','2024-12-01 15:15:00'),(32,'0000003','MED0006','12121212121','2024-12-10 08:45:00'),(33,'0000004','MED0008','16161616161','2024-12-15 16:00:00'),(34,'0000001','MED0003','18181818181','2024-12-20 11:00:00'),(35,'0000002','MED0007','22222222222','2024-12-28 13:00:00'),(36,'0000001','MED0001','11111111111','2025-01-15 08:00:00'),(37,'0000002','MED0005','88888888888','2025-02-10 14:00:00'),(38,'0000003','MED0004','20202020202','2025-03-05 09:30:00'),(39,'0000005','MED0002','77777777777','2025-04-12 16:00:00'),(40,'0000001','MED0003','18181818181','2025-05-20 11:00:00'),(41,'0000004','MED0008','66666666666','2025-06-15 15:00:00'),(42,'0000002','MED0007','99999999999','2025-07-20 14:30:00'),(43,'0000003','MED0006','13131313131','2025-08-10 09:00:00'),(44,'0000001','MED0001','10101010101','2025-09-05 17:00:00'),(45,'0000005','MED0002','21212121212','2025-10-15 13:00:00'),(46,'0000001','MED0003','17171717171','2025-11-01 11:30:00'),(47,'0000002','MED0005','44444444444','2025-11-20 14:00:00'),(48,'0000003','MED0004','14141414141','2025-12-05 10:00:00'),(49,'0000004','MED0008','15151515151','2025-12-15 16:30:00'),(50,'0000001','MED0001','19191919191','2025-12-22 09:00:00'),(51,'0000001','MED0001','11111111111','2026-01-10 08:00:00'),(52,'0000002','MED0007','22222222222','2026-02-15 14:00:00'),(53,'0000005','MED0002','55555555555','2026-03-20 15:00:00'),(54,'0000003','MED0006','12121212121','2026-04-10 08:30:00'),(55,'0000001','MED0003','18181818181','2026-05-15 11:00:00'),(56,'0000003','MED0008','13131313131','2025-11-28 10:00:00');
/*!40000 ALTER TABLE `consulta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_cancelamento`
--

DROP TABLE IF EXISTS `log_cancelamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_cancelamento` (
  `IdLog` int NOT NULL AUTO_INCREMENT,
  `Usuario` varchar(50) DEFAULT NULL,
  `DataCancelamento` datetime DEFAULT NULL,
  `IdConsultaDeletada` int DEFAULT NULL,
  `Motivo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`IdLog`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_cancelamento`
--

LOCK TABLES `log_cancelamento` WRITE;
/*!40000 ALTER TABLE `log_cancelamento` DISABLE KEYS */;
/*!40000 ALTER TABLE `log_cancelamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medico`
--

DROP TABLE IF EXISTS `medico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medico` (
  `CodMed` char(7) NOT NULL,
  `NomeMed` varchar(100) NOT NULL,
  `Genero` char(1) DEFAULT NULL,
  `Telefone` varchar(20) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Especialidade` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`CodMed`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medico`
--

LOCK TABLES `medico` WRITE;
/*!40000 ALTER TABLE `medico` DISABLE KEYS */;
INSERT INTO `medico` VALUES ('MED0001','Dr. Roberto Silva','M','98888-1111','roberto@mail.com','Cardiologia'),('MED0002','Dra. Ana Clara','F','97777-2222','anaclara@mail.com','Dermatologia'),('MED0003','Dr. Jorge Mendes','M','96666-3333','jorge@mail.com','Cardiologia'),('MED0004','Dra. Patricia Lima','F','95555-4444','patricia@mail.com','Pediatria'),('MED0005','Dr. Lucas Carvalho','M','98256-5703','lucas@mail.com','Oftalmologia'),('MED0006','Dra. Marcela Gomes','F','98273-3245','marcela@mail.com','Pediatria'),('MED0007','Dr. Alexandre Alencar','M','99482-4758','alexandre@mail.com','Oftalmologia'),('MED0008','Dra. Carla Dias','F','91111-2222','carla@mail.com','Ortopedia'),('MED0009','Dr. Gregory House','M','90000-0000','house@mail.com','Diagnóstico'),('MED0010','Dra. Grey','F','91111-1111','grey@mail.com','Cirurgia Geral');
/*!40000 ALTER TABLE `medico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paciente`
--

DROP TABLE IF EXISTS `paciente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paciente` (
  `CpfPaciente` char(11) NOT NULL,
  `NomePac` varchar(100) NOT NULL,
  `DataNascimento` date DEFAULT NULL,
  `Genero` char(1) DEFAULT NULL,
  `Telefone` varchar(20) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`CpfPaciente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paciente`
--

LOCK TABLES `paciente` WRITE;
/*!40000 ALTER TABLE `paciente` DISABLE KEYS */;
INSERT INTO `paciente` VALUES ('10101010101','Fausto Silva','1965-02-02','M','9999-0010','fausto@mail.com'),('11111111111','Sr. João Silva','1950-05-20','M','9999-0001','joao@mail.com'),('12121212121','Menino Ney','2015-02-05','M','9999-0011','ney@mail.com'),('13131313131','Menina Maisa','2010-05-22','F','9999-0012','maisa@mail.com'),('14141414141','Bebê George','2023-01-01','M','9999-0013','geo@mail.com'),('15151515151','Larissa Manoela','2005-12-28','F','9999-0014','lari@mail.com'),('16161616161','MC Cabelinho','2000-01-20','M','9999-0015','mc@mail.com'),('17171717171','Cliente Fiel','1995-05-05','M','9999-0016','fiel@mail.com'),('18181818181','Hipocondríaco Junior','1998-08-08','M','9999-0017','hipo@mail.com'),('19191919191','Dona Florinda','1962-02-14','F','9999-0018','flor@mail.com'),('20202020202','Chaves do 8','2016-06-20','M','9999-0019','chaves@mail.com'),('21212121212','Chiquinha','2016-10-10','F','9999-0020','chiq@mail.com'),('22222222222','Sra. Maria José','1955-10-10','F','9999-0002','maria@mail.com'),('33333333333','Sr. Pedro Paulo','1960-01-30','M','9999-0003','pedro@mail.com'),('44444444444','Carlos Santana','1985-06-15','M','9999-0004','carlos@mail.com'),('55555555555','Fernanda Lima','1990-12-25','F','9999-0005','nanda@mail.com'),('66666666666','Roberto Justus','1982-03-12','M','9999-0006','justus@mail.com'),('77777777777','Ana Paula Padrão','1988-07-07','F','9999-0007','ana@mail.com'),('88888888888','Tiago Leifert','1980-09-09','M','9999-0008','tiago@mail.com'),('99999999999','Ivete Sangalo','1975-05-27','F','9999-0009','ivete@mail.com');
/*!40000 ALTER TABLE `paciente` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-27 14:28:07
