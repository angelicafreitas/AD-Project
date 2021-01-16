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
INSERT INTO `dim_gun_type` VALUES (1,'223 Rem [AR-15]'),(2,'410 gauge'),(3,'Shotgun'),(4,'12 gauge'),(5,'32 Auto'),(6,'38 Spl'),(7,'44 Mag'),(8,'10mm'),(9,'Handgun'),(10,'40 SW'),(11,'Rifle'),(12,'380 Auto'),(13,'25 Auto'),(14,'Other'),(15,'28 gauge'),(16,'9mm'),(17,'357 Mag'),(18,'7.62 [AK-47]'),(19,'22 LR'),(20,'30-06 Spr'),(21,'300 Win'),(22,'16 gauge'),(23,'Unknown'),(24,'20 gauge'),(25,'45 Auto'),(26,'30-30 Win'),(27,'308 Win');
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

-- Dump completed on 2021-01-16 13:19:01
