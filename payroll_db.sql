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
  `fund_amount` decimal(15,2) DEFAULT NULL,
  PRIMARY KEY (`fund_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fund`
--

LOCK TABLES `fund` WRITE;
/*!40000 ALTER TABLE `fund` DISABLE KEYS */;
INSERT INTO `fund` VALUES (1,2000000000.00);
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
  `fund_id` int DEFAULT NULL,
  `admin_id` varchar(50) DEFAULT NULL,
  `old_amount` decimal(15,2) DEFAULT NULL,
  `new_amount` decimal(15,2) DEFAULT NULL,
  `transaction_date` datetime DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `fk_trans_fund_idx` (`fund_id`),
  KEY `fk_trans_admin_idx` (`admin_id`),
  CONSTRAINT `fk_trans_fund` FOREIGN KEY (`fund_id`) REFERENCES `fund` (`fund_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fundtransaction`
--

LOCK TABLES `fundtransaction` WRITE;
/*!40000 ALTER TABLE `fundtransaction` DISABLE KEYS */;
INSERT INTO `fundtransaction` VALUES (1,1,'1',2000000000.00,1970000000.00,'2025-11-30 15:00:00');
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
  `leave_date` date DEFAULT NULL,
  PRIMARY KEY (`leave_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leave`
--

LOCK TABLES `leave` WRITE;
/*!40000 ALTER TABLE `leave` DISABLE KEYS */;
INSERT INTO `leave` VALUES (1,'2025-12-25');
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
  `leave_id` int DEFAULT NULL,
  `staff_id` varchar(50) DEFAULT NULL,
  `reason` longtext,
  `status` enum('Pending','Approved','Rejected') DEFAULT NULL,
  PRIMARY KEY (`detail_id`),
  KEY `fk_detail_id_idx` (`leave_id`),
  KEY `fk_detail_staff_idx` (`staff_id`),
  CONSTRAINT `fk_detail_id` FOREIGN KEY (`leave_id`) REFERENCES `leave` (`leave_id`),
  CONSTRAINT `fk_detail_staff` FOREIGN KEY (`staff_id`) REFERENCES `staffprofile` (`staff_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leavedetail`
--

LOCK TABLES `leavedetail` WRITE;
/*!40000 ALTER TABLE `leavedetail` DISABLE KEYS */;
INSERT INTO `leavedetail` VALUES (1,1,'2','Xin nghỉ đi chơi Noel','Pending');
/*!40000 ALTER TABLE `leavedetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `person` (
  `id` varchar(50) NOT NULL,
  `username` varchar(150) DEFAULT NULL,
  `password` varchar(150) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `role` enum('Admin','Staff') DEFAULT NULL,
  `gender` enum('Male','Female','Other') DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person`
--

LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
INSERT INTO `person` VALUES ('1','admin_boss','123456','2020-01-01','Admin','Male','1990-05-20'),('2','staff_alice','123456','2024-06-01','Staff','Female','2000-01-15'),('3','staff_bob','123456','2024-07-01','Staff','Male','1995-11-05');
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
  `rank` varchar(100) DEFAULT NULL,
  `amount` decimal(15,2) DEFAULT NULL,
  `multiplier` float DEFAULT NULL,
  PRIMARY KEY (`salary_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salary`
--

LOCK TABLES `salary` WRITE;
/*!40000 ALTER TABLE `salary` DISABLE KEYS */;
INSERT INTO `salary` VALUES (1,'Intern',5000000.00,1),(2,'Senior Dev',20000000.00,1.5);
INSERT INTO `salary` VALUES ('1','Senior3',4000.00,1.6),('2','Senior2',10000.00,1.5),('L001','Junior 3',2000.00,1),('L002','Junior 2',2000.00,1);
/*!40000 ALTER TABLE `salary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salarychangehistory`
--

DROP TABLE IF EXISTS `salarychangehistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salarychangehistory` (
  `history_id` int NOT NULL AUTO_INCREMENT,
  `admin_id` varchar(36) DEFAULT NULL,
  `salary_id` varchar(20) DEFAULT NULL,
  `old_amount` decimal(15,2) DEFAULT NULL,
  `new_amount` decimal(15,2) DEFAULT NULL,
  `old_multiplier` float DEFAULT NULL,
  `new_multiplier` float DEFAULT NULL,
  `change_date` datetime DEFAULT NULL,
  PRIMARY KEY (`history_id`),
  KEY `fk_history_admin_idx` (`admin_id`),
  KEY `fk_history_staff_idx` (`staff_id`),
  KEY `fk_history_salary_idx` (`salary_id`),
  CONSTRAINT `fk_history_admin` FOREIGN KEY (`admin_id`) REFERENCES `person` (`id`),
  CONSTRAINT `fk_history_salary` FOREIGN KEY (`salary_id`) REFERENCES `salary` (`salary_id`),
  CONSTRAINT `fk_history_staff` FOREIGN KEY (`staff_id`) REFERENCES `staffprofile` (`staff_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salarychangehistory`
--

LOCK TABLES `salarychangehistory` WRITE;
/*!40000 ALTER TABLE `salarychangehistory` DISABLE KEYS */;
INSERT INTO `salarychangehistory` VALUES (1,'1','2',2,5000000.00,20000000.00,1,1.5,'2025-12-01 09:00:00');
INSERT INTO `salarychangehistory` VALUES (2,NULL,'2',20000000.00,10000.00,1.5,1.5,'Senior Dev','Senior 2','2025-11-20 10:42:12'),(5,NULL,'2',10000.00,10000.00,1.5,1.5,'Senior2','Senior2','2025-11-20 11:40:14'),(6,NULL,'1',3000.00,4000.00,1.6,1.6,'Senior 3','Senior 3','2025-11-23 21:10:34'),(7,NULL,'1',4000.00,4000.00,1.6,1.6,'Senior 3','Senior3','2025-11-23 21:11:15');
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
  `staff_id` varchar(50) DEFAULT NULL,
  `admin_id` varchar(50) DEFAULT NULL,
  `total_amount` decimal(15,2) DEFAULT NULL,
  `payment_date` datetime DEFAULT NULL,
  `salary_id` int DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `fk_payment_admin_idx` (`admin_id`),
  KEY `fk_payment_staff_idx` (`staff_id`),
  KEY `fk_payment_salary_idx` (`salary_id`),
  CONSTRAINT `fk_payment_admin` FOREIGN KEY (`admin_id`) REFERENCES `person` (`id`),
  CONSTRAINT `fk_payment_salary` FOREIGN KEY (`salary_id`) REFERENCES `salary` (`salary_id`),
  CONSTRAINT `fk_payment_staff` FOREIGN KEY (`staff_id`) REFERENCES `staffprofile` (`staff_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salarypayment`
--

LOCK TABLES `salarypayment` WRITE;
/*!40000 ALTER TABLE `salarypayment` DISABLE KEYS */;
INSERT INTO `salarypayment` VALUES (1,'3','1',30000000.00,'2025-11-30 15:00:00',2);
INSERT INTO `salarypayment` VALUES (1,'2','2',4800.00,'2025-11-15 00:00:00','1'),(2,'3','2',15000.00,'2025-11-15 00:00:00','2'),(3,'3','2',15000.00,'2025-10-15 00:00:00','2'),(4,'2','2',4800.00,'2025-03-15 00:00:00','1');
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
  `admin_id` varchar(50) DEFAULT NULL,
  `staff_id` varchar(50) DEFAULT NULL,
  `action` varchar(100) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`manage_id`),
  KEY `fk_manage_admin_idx` (`admin_id`),
  KEY `fk_manage_staff_idx` (`staff_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staffmanagement`
--

LOCK TABLES `staffmanagement` WRITE;
/*!40000 ALTER TABLE `staffmanagement` DISABLE KEYS */;
INSERT INTO `staffmanagement` VALUES (1,'1','2','thêm','2024-06-01 08:00:00'),(2,'1','3','thêm','2024-07-01 08:00:00');
/*!40000 ALTER TABLE `staffmanagement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staffprofile`
--

DROP TABLE IF EXISTS `staffprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staffprofile` (
  `staff_id` varchar(36) NOT NULL,
  `salary_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`staff_id`),
  KEY `fk_staff_salary_idx` (`salary_id`),
  CONSTRAINT `fk_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `person` (`id`),
  CONSTRAINT `fk_staff_salary` FOREIGN KEY (`salary_id`) REFERENCES `salary` (`salary_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staffprofile`
--

LOCK TABLES `staffprofile` WRITE;
/*!40000 ALTER TABLE `staffprofile` DISABLE KEYS */;
INSERT INTO `staffprofile` VALUES ('2',1),('3',2);
INSERT INTO `staffprofile` VALUES ('2','1'),('3','2');
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
