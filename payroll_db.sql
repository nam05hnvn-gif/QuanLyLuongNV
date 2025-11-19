CREATE DATABASE  IF NOT EXISTS `payroll_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `payroll_db`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: payroll_db
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
-- Table structure for table `fund`
--

DROP TABLE IF EXISTS `fund`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fund` (
  `fund_id` int NOT NULL,
  `fund_name` varchar(100) NOT NULL,
  `fund_amount` decimal(15,2) NOT NULL,
  PRIMARY KEY (`fund_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fund`
--

LOCK TABLES `fund` WRITE;
/*!40000 ALTER TABLE `fund` DISABLE KEYS */;
INSERT INTO `fund` VALUES (999,'Main Fund',5000000000.00);
/*!40000 ALTER TABLE `fund` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fundtransaction`
--

DROP TABLE IF EXISTS `fundtransaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fundtransaction` (
  `transaction_id` int NOT NULL,
  `fund_id` int NOT NULL,
  `admin_id` int NOT NULL,
  `old_fund` decimal(15,2) NOT NULL,
  `new_fund` decimal(15,2) NOT NULL,
  `transaction_date` datetime NOT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `fk_trans_fund_idx` (`fund_id`),
  KEY `fk_trans_admin_idx` (`admin_id`),
  CONSTRAINT `fk_trans_admin` FOREIGN KEY (`admin_id`) REFERENCES `person` (`id`),
  CONSTRAINT `fk_trans_fund` FOREIGN KEY (`fund_id`) REFERENCES `fund` (`fund_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fundtransaction`
--

LOCK TABLES `fundtransaction` WRITE;
/*!40000 ALTER TABLE `fundtransaction` DISABLE KEYS */;
INSERT INTO `fundtransaction` VALUES (9001,999,1,5000000000.00,4970000000.00,'2025-11-19 03:49:44');
/*!40000 ALTER TABLE `fundtransaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leave`
--

DROP TABLE IF EXISTS `leave`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leave` (
  `leave_id` int NOT NULL,
  `leave_date` date NOT NULL,
  PRIMARY KEY (`leave_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leave`
--

LOCK TABLES `leave` WRITE;
/*!40000 ALTER TABLE `leave` DISABLE KEYS */;
INSERT INTO `leave` VALUES (500,'2025-11-20');
/*!40000 ALTER TABLE `leave` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leavedetail`
--

DROP TABLE IF EXISTS `leavedetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leavedetail` (
  `detail_id` int NOT NULL,
  `leave_id` int NOT NULL,
  `staff_id` int NOT NULL,
  `reason` longtext,
  `status` enum('pending','approved','rejected') NOT NULL,
  PRIMARY KEY (`detail_id`),
  KEY `fk_leave_leave_idx` (`leave_id`),
  KEY `fk_leave_staff_idx` (`staff_id`),
  CONSTRAINT `fk_leave_leave` FOREIGN KEY (`leave_id`) REFERENCES `leave` (`leave_id`),
  CONSTRAINT `fk_leave_staff` FOREIGN KEY (`staff_id`) REFERENCES `person` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leavedetail`
--

LOCK TABLES `leavedetail` WRITE;
/*!40000 ALTER TABLE `leavedetail` DISABLE KEYS */;
INSERT INTO `leavedetail` VALUES (1,500,3,'Sick leave','approved');
/*!40000 ALTER TABLE `leavedetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `person` (
  `id` int NOT NULL,
  `username` varchar(150) NOT NULL,
  `password` varchar(128) NOT NULL,
  `start_date` date NOT NULL,
  `role` enum('admin','staff') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person`
--

LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
INSERT INTO `person` VALUES (1,'admin_boss','123456','2023-01-01','admin'),(2,'staff_alex','123456','2023-06-15','staff'),(3,'staff_sarah','123456','2023-07-01','staff');
/*!40000 ALTER TABLE `person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salary`
--

DROP TABLE IF EXISTS `salary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salary` (
  `salary_id` int NOT NULL,
  `salary_rank` varchar(100) NOT NULL,
  `amount` decimal(15,2) NOT NULL,
  `multiplier` float DEFAULT NULL,
  PRIMARY KEY (`salary_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salary`
--

LOCK TABLES `salary` WRITE;
/*!40000 ALTER TABLE `salary` DISABLE KEYS */;
INSERT INTO `salary` VALUES (101,'Junior',10000000.00,1),(102,'Senior',20000000.00,1.5);
/*!40000 ALTER TABLE `salary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salarychangehistory`
--

DROP TABLE IF EXISTS `salarychangehistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salarychangehistory` (
  `history_id` int NOT NULL,
  `staff_id` int NOT NULL,
  `admin_id` int NOT NULL,
  `salary_id` int NOT NULL,
  `old_amount` decimal(15,2) DEFAULT NULL,
  `new_amount` decimal(15,2) NOT NULL,
  `old_multiplier` float DEFAULT NULL,
  `new_multiplier` float DEFAULT NULL,
  `change_date` datetime NOT NULL,
  PRIMARY KEY (`history_id`),
  KEY `fk_schistory_staff_idx` (`staff_id`),
  KEY `fk_schistory_admin_idx` (`admin_id`),
  KEY `fk_schistory_salary_idx` (`salary_id`),
  CONSTRAINT `fk_schistory_admin` FOREIGN KEY (`admin_id`) REFERENCES `person` (`id`),
  CONSTRAINT `fk_schistory_salary` FOREIGN KEY (`salary_id`) REFERENCES `salary` (`salary_id`),
  CONSTRAINT `fk_schistory_staff` FOREIGN KEY (`staff_id`) REFERENCES `person` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salarychangehistory`
--

LOCK TABLES `salarychangehistory` WRITE;
/*!40000 ALTER TABLE `salarychangehistory` DISABLE KEYS */;
/*!40000 ALTER TABLE `salarychangehistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salarypayment`
--

DROP TABLE IF EXISTS `salarypayment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salarypayment` (
  `payment_id` int NOT NULL,
  `staff_id` int NOT NULL,
  `admin_id` int NOT NULL,
  `salary_id` int NOT NULL,
  `total_amount` decimal(15,2) NOT NULL,
  `payment_date` datetime NOT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `fk_pay_staff_idx` (`staff_id`),
  KEY `fk_pay_admin_idx` (`admin_id`),
  KEY `fk_pay_salary_idx` (`salary_id`),
  CONSTRAINT `fk_pay_admin` FOREIGN KEY (`admin_id`) REFERENCES `person` (`id`),
  CONSTRAINT `fk_pay_salary` FOREIGN KEY (`salary_id`) REFERENCES `salary` (`salary_id`),
  CONSTRAINT `fk_pay_staff` FOREIGN KEY (`staff_id`) REFERENCES `person` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salarypayment`
--

LOCK TABLES `salarypayment` WRITE;
/*!40000 ALTER TABLE `salarypayment` DISABLE KEYS */;
INSERT INTO `salarypayment` VALUES (8001,2,1,102,30000000.00,'2025-11-19 03:49:44');
/*!40000 ALTER TABLE `salarypayment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staffmanagement`
--

DROP TABLE IF EXISTS `staffmanagement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staffmanagement` (
  `manage_id` int NOT NULL,
  `admin_id` int NOT NULL,
  `staff_id` int NOT NULL,
  `action` varchar(50) NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`manage_id`),
  KEY `fk_manage_admin_idx` (`admin_id`),
  KEY `fk_manage_staff_idx` (`staff_id`),
  CONSTRAINT `fk_manage_admin` FOREIGN KEY (`admin_id`) REFERENCES `person` (`id`),
  CONSTRAINT `fk_manage_staff` FOREIGN KEY (`staff_id`) REFERENCES `person` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staffmanagement`
--

LOCK TABLES `staffmanagement` WRITE;
/*!40000 ALTER TABLE `staffmanagement` DISABLE KEYS */;
/*!40000 ALTER TABLE `staffmanagement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staffprofile`
--

DROP TABLE IF EXISTS `staffprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staffprofile` (
  `staff_id` int NOT NULL,
  `salary_id` int NOT NULL,
  `gender` enum('male','female') DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  PRIMARY KEY (`staff_id`),
  KEY `fk_staff_salary_idx` (`salary_id`),
  CONSTRAINT `fk_staff_person` FOREIGN KEY (`staff_id`) REFERENCES `person` (`id`),
  CONSTRAINT `fk_staff_salary` FOREIGN KEY (`salary_id`) REFERENCES `salary` (`salary_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staffprofile`
--

LOCK TABLES `staffprofile` WRITE;
/*!40000 ALTER TABLE `staffprofile` DISABLE KEYS */;
INSERT INTO `staffprofile` VALUES (2,102,'male','1995-05-20'),(3,101,'female','1998-11-10');
/*!40000 ALTER TABLE `staffprofile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-19  4:00:20
