-- MariaDB dump 10.19  Distrib 10.6.4-MariaDB, for osx10.16 (arm64)
--
-- Host: localhost    Database: tweeter_project
-- ------------------------------------------------------
-- Server version	10.6.4-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `content` varchar(200) COLLATE utf8mb4_bin NOT NULL,
  `created_at` date NOT NULL DEFAULT current_timestamp(),
  `user_id` int(10) unsigned NOT NULL,
  `tweet_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `comment_FK` (`user_id`),
  KEY `comment_FK_1` (`tweet_id`),
  CONSTRAINT `comment_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_FK_1` FOREIGN KEY (`tweet_id`) REFERENCES `tweet` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_CHECK` CHECK (octet_length(`content`) > 0)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (1,'First test comment update','2022-03-03',1,1),(2,'Test comment 2','2022-03-03',2,2),(3,'Test comment 3','2022-03-03',2,2),(7,'First test comment','2022-03-07',1,1);
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment_like`
--

DROP TABLE IF EXISTS `comment_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment_like` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `comment_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `comment_like_UN` (`comment_id`,`user_id`),
  KEY `comment_like_FK` (`user_id`),
  CONSTRAINT `comment_like_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_like_FK_1` FOREIGN KEY (`comment_id`) REFERENCES `comment` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment_like`
--

LOCK TABLES `comment_like` WRITE;
/*!40000 ALTER TABLE `comment_like` DISABLE KEYS */;
INSERT INTO `comment_like` VALUES (1,1,1),(2,2,2),(7,1,3),(3,5,3);
/*!40000 ALTER TABLE `comment_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `follow`
--

DROP TABLE IF EXISTS `follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `follow` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `follower_id` int(10) unsigned NOT NULL,
  `followed_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `follow_UN` (`follower_id`,`followed_id`),
  KEY `follow_FK_1` (`followed_id`),
  CONSTRAINT `follow_FK` FOREIGN KEY (`follower_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `follow_FK_1` FOREIGN KEY (`followed_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `follow`
--

LOCK TABLES `follow` WRITE;
/*!40000 ALTER TABLE `follow` DISABLE KEYS */;
INSERT INTO `follow` VALUES (2,2,1),(6,5,7),(14,7,1),(3,7,2),(11,7,5);
/*!40000 ALTER TABLE `follow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tweet`
--

DROP TABLE IF EXISTS `tweet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweet` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `content` varchar(200) COLLATE utf8mb4_bin NOT NULL,
  `created_at` date NOT NULL DEFAULT current_timestamp(),
  `user_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tweet_FK` (`user_id`),
  CONSTRAINT `tweet_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tweet_CHECK` CHECK (octet_length(`content`) > 0)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tweet`
--

LOCK TABLES `tweet` WRITE;
/*!40000 ALTER TABLE `tweet` DISABLE KEYS */;
INSERT INTO `tweet` VALUES (1,'Tweet1','2022-03-02',1),(2,'Tweet2','2022-03-02',2),(3,'Tweet3','2022-03-02',2),(7,'Test from Postman','2022-03-03',7),(11,'Another test from Postman','2022-03-03',7),(14,'Another test from Postman','2022-03-07',5),(15,'Test','2022-03-07',19),(16,'Testing again','2022-03-07',19),(17,'Posting a new tweet','2022-03-07',19),(18,'Another test posting','2022-03-07',19),(19,'New test','2022-03-07',19),(20,'Test post by user14','2022-03-07',19),(21,'Test post','2022-03-07',5);
/*!40000 ALTER TABLE `tweet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tweet_like`
--

DROP TABLE IF EXISTS `tweet_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweet_like` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `tweet_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tweet_like_UN` (`user_id`,`tweet_id`),
  KEY `tweet_like_FK_1` (`tweet_id`),
  CONSTRAINT `tweet_like_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tweet_like_FK_1` FOREIGN KEY (`tweet_id`) REFERENCES `tweet` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tweet_like`
--

LOCK TABLES `tweet_like` WRITE;
/*!40000 ALTER TABLE `tweet_like` DISABLE KEYS */;
INSERT INTO `tweet_like` VALUES (1,1,1),(2,1,2),(3,2,3),(12,5,16),(10,19,1),(11,19,2),(35,19,3),(32,19,7);
/*!40000 ALTER TABLE `tweet_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `username` varchar(30) COLLATE utf8mb4_bin NOT NULL,
  `password` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `bio` varchar(200) COLLATE utf8mb4_bin NOT NULL,
  `birthdate` date NOT NULL,
  `image_url` varchar(500) COLLATE utf8mb4_bin NOT NULL DEFAULT 'https://www.reshot.com/preview-assets/icons/E7JU2GQ3FT/avatar-E7JU2GQ3FT.svg',
  `banner_url` varchar(500) COLLATE utf8mb4_bin NOT NULL DEFAULT 'https://res.cloudinary.com/twenty20/private_images/t_standard-fit/v1611255558/photosp/51960aad-06e3-411c-927f-f270ebd9f766/51960aad-06e3-411c-927f-f270ebd9f766.jpg',
  `salt` varchar(15) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_email` (`email`),
  UNIQUE KEY `user_username` (`username`),
  CONSTRAINT `user_CHECK` CHECK (octet_length(`password`) > 3)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'user1@users.com','user1','pass1','Engineer','1988-04-07','https://www.reshot.com/preview-assets/icons/E7JU2GQ3FT/avatar-E7JU2GQ3FT.svg','https://res.cloudinary.com/twenty20/private_images/t_standard-fit/v1611255558/photosp/51960aad-06e3-411c-927f-f270ebd9f766/51960aad-06e3-411c-927f-f270ebd9f766.jpg',''),(2,'user2@users.com','user2','pass2','Doctor','1990-05-06','https://www.reshot.com/preview-assets/icons/E7JU2GQ3FT/avatar-E7JU2GQ3FT.svg','https://res.cloudinary.com/twenty20/private_images/t_standard-fit/v1611255558/photosp/51960aad-06e3-411c-927f-f270ebd9f766/51960aad-06e3-411c-927f-f270ebd9f766.jpg',''),(5,'user4@users.com','user4','pass4','Teacher','1985-11-02','https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1287&q=80','','mAbAhLOHFwV0iA'),(7,'user7@users.com','user7','pass7','Scientist','1985-11-05','https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1287&q=80','','Ha3_yo0RGYAe_A'),(8,'user8@users.com','user8','newpass','Test','1985-11-05','https://res.cloudinary.com/twenty20/private_images/t_standard-fit/v1611255558/photosp/51960aad-06e3-411c-927f-f270ebd9f766/51960aad-06e3-411c-927f-f270ebd9f766.jpg','','xczn7J_aqkm90A'),(9,'user9@users.com','user9','newpass','Developer','1985-11-05','https://res.cloudinary.com/twenty20/private_images/t_standard-fit/v1611255558/photosp/51960aad-06e3-411c-927f-f270ebd9f766/51960aad-06e3-411c-927f-f270ebd9f766.jpg','','dNLpXUHjABBPHQ'),(12,'user11@users.com','user11','pass10','Scientist','1985-11-05','https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1287&q=80','','qxaQ6Tze56VbHw'),(17,'user12@users.com','user12','pass12','Scientist','1985-11-05','https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1287&q=80','','ICcUDC7yyP_gYA'),(18,'user13@users.com','user13','pass13','Teacher','1992-05-04','https://www.reshot.com/preview-assets/icons/E7JU2GQ3FT/avatar-E7JU2GQ3FT.svg','https://res.cloudinary.com/twenty20/private_images/t_standard-fit/v1611255558/photosp/51960aad-06e3-411c-927f-f270ebd9f766/51960aad-06e3-411c-927f-f270ebd9f766.jpg','UYaGl8oX4TAykg'),(19,'user14@users.com','user14','pass14','Web Dev','1995-11-09','https://res.cloudinary.com/twenty20/private_images/t_standard-fit/v1611255558/photosp/51960aad-06e3-411c-927f-f270ebd9f766/51960aad-06e3-411c-927f-f270ebd9f766.jpg','https://res.cloudinary.com/twenty20/private_images/t_standard-fit/v1611255558/photosp/51960aad-06e3-411c-927f-f270ebd9f766/51960aad-06e3-411c-927f-f270ebd9f766.jpg','z0V9nB1hyv2qOw'),(21,'user15@users.com','user15@users.com','pass15','Scientist','1985-11-05','https://www.reshot.com/preview-assets/icons/E7JU2GQ3FT/avatar-E7JU2GQ3FT.svg','https://res.cloudinary.com/twenty20/private_images/t_standard-fit/v1611255558/photosp/51960aad-06e3-411c-927f-f270ebd9f766/51960aad-06e3-411c-927f-f270ebd9f766.jpg','Lc_K_vxy1lGKXQ');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_session`
--

DROP TABLE IF EXISTS `user_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_session` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `login_token` varchar(300) COLLATE utf8mb4_bin NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_session_UN` (`login_token`),
  KEY `user_session_FK` (`user_id`),
  CONSTRAINT `user_session_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_session`
--

LOCK TABLES `user_session` WRITE;
/*!40000 ALTER TABLE `user_session` DISABLE KEYS */;
INSERT INTO `user_session` VALUES (1,'czpO11YaFF44IayZU0lP1j1l5E1uK0wQi5pifPfqSqnAsdTAcPX7sdMPd7PKejy22R0',5),(4,'DlZBcqq6bbVgYBXMa1oiTadUSND6FkHwLHmiSAp6y_TF3uBm7HCxy5Mmvw6fizg91gk',8),(5,'YjX7s3Gxonv4QmmcRqtpV5W6WuXZjfYYGfu3_w9kNFqiDNY02rTJVWvgUB7BgANZSTg',5),(6,'ii-qu-ofwIwI-gSXa4sqgwrKkph3C7Qc_TeqVVx8BDMDHdnSq7-_bbPueQtM6_0PW_8',9),(7,'XwRBpQQVQCEwN39LgmfVe36anLetz8H4MncTXg87dpJHPjOqLEZi5Wq3cMozpeo20zo',5),(8,'X7JvK84nKKRwcM8Rj3ntAcYc7VlsaU7K4_0rbL_USmZPyc-R48lTfhTRugzCio5D3JA',5),(9,'Vp-g5K3ollTma7N-4aZIw0EHUVq8z5vmv4hakV0m3EuVAKk_EmpzwGl-B84VCYVlUyA',5),(12,'SKyu4N7L30EbDWYT9ZwXsRq_f8gh6MQY-I6uwa5JfEIQ4qqO5MpUTZAoe3O9kQcyjc0',7),(13,'f7IaZ2D0wAY2idAAVplQM05SuqMocP2q0kwrBmQ3JBCY07sSVAijrDgMU0_g6L3cfmg',12),(14,'G4XzVw51XFdcfUcs5d4HhUM9UILm7LziMg-4r6q7jG0VMt3XMs_rA_Cpf6iXW5oAW_w',7),(15,'pipzwqqGpySrUiq9egtR1XNmG15NXgHCQ4CIuRseCozKT19whXjanx0TBiK97kBCAKU',1),(16,'Ew75kf-Yp7eppzEjOmj_Vxirg8ck1yva88Mjs_vES0QDlAuBqifdE7g8__Aoxk2rTSE',1),(17,'qrGdl3oVoIn3m5wj71XhRaT2Bzs4CKW2puMICijmbM0VluBwyccHBm_zocoDpLKErew',1),(19,'viObx0Hklk-gBKXGKgVW2-lR09DsbmL0HSfYgv4pRLKuLvWlKD3HdaqX2Q7UDwcIM7E',1),(21,'THHIhsWL22VTeErekxQnwn7iTHLsmY3aEOYIAXsYCGh26-I29klxk8Z13SNbcQK4hU8',1),(22,'0ryOxnRyr-Js7CziohXh3Tlg9BB1hSFqSbRZ-n4e5851o1PNH8jlpe6ECsIt31CS-VA',17),(25,'zgnSdf4NtDLhxJru-1rADQ3Ljf7CFmwwsGAkjQIAaRspjm2ZpJPwlST5OgtyHKk01Ok',17),(26,'3jI6trWMA-FZhSOTKKfgaO8WVHqeNgxWzudNW2f-70vye5QQ7ZTbiTk6HoYvBdICT8M',17),(28,'WzApG_chGzXFuDj7iV8wZlCboZlBc2fbu__oWAZWaG0FPS0ms3P_IOg23psgAJhOFFU',18),(30,'l5XBhDuWhmXdxoW1FP3T0Oppvp1s32OX5AMF0vlq1LaUs9tJaAaK2VS9E0oeZ-9ojpQ',19),(35,'NTeKZEdVYoXXzCQSqlAsemEnMYAT64H_OATGOvzOn0uu8LuplD7NBd7E34Knhc3lXIY',19),(36,'JT9lQdgyJpcawDJr1_givy02Y3JkMxQgSLoW8awt9JYRiKEGSoHYvt25Uz6LsEz_wbQ',21);
/*!40000 ALTER TABLE `user_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'tweeter_project'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-03-08  0:01:17
