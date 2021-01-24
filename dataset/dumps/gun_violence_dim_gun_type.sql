-- MySQL dump 10.13  Distrib 8.0.18, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: gun_violence
-- ------------------------------------------------------
-- Server version	8.0.18

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
-- Table structure for table `dim_gun_type`
--

DROP TABLE IF EXISTS `dim_gun_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_gun_type` (
  `dim_gun_type_id` int(11) NOT NULL,
  `class_type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`dim_gun_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dim_gun_type`
--

LOCK TABLES `dim_gun_type` WRITE;
/*!40000 ALTER TABLE `dim_gun_type` DISABLE KEYS */;
INSERT INTO `dim_gun_type` VALUES (1,'25 Auto'),(2,'223 Rem [AR-15]'),(3,'12 gauge'),(4,'308 Win'),(5,'7.62 [AK-47]'),(6,'Unknown'),(7,'357 Mag'),(8,'Handgun'),(9,'410 gauge'),(10,'32 Auto'),(11,'16 gauge'),(12,'40 SW'),(13,'Rifle'),(14,'Shotgun'),(15,'380 Auto'),(16,'30-06 Spr'),(17,'44 Mag'),(18,'300 Win'),(19,'20 gauge'),(20,'28 gauge'),(21,'22 LR'),(22,'38 Spl'),(23,'45 Auto'),(24,'10mm'),(25,'9mm'),(26,'Other'),(27,'30-30 Win');
/*!40000 ALTER TABLE `dim_gun_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-24  9:32:04
