-- MySQL dump 10.13  Distrib 5.6.10, for osx10.6 (x86_64)
--
-- Host: sql.mit.edu    Database: mjhu+eyebrowse_prod
-- ------------------------------------------------------
-- Server version	5.1.56-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_userprofile`
--

DROP TABLE IF EXISTS `accounts_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `activation_key` varchar(40) NOT NULL,
  `pic_url` varchar(1000) NOT NULL,
  `use_tour` tinyint(1) NOT NULL,
  `anon_email` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_userprofile`
--

LOCK TABLES `accounts_userprofile` WRITE;
/*!40000 ALTER TABLE `accounts_userprofile` DISABLE KEYS */;
INSERT INTO `accounts_userprofile` VALUES (1,1,'','/static/common/img/placeholder.png',1,0),(2,2,'','/static/common/img/placeholder.png',1,0),(3,3,'','/static/common/img/placeholder.png',1,0);
/*!40000 ALTER TABLE `accounts_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_userprofile_follows`
--

DROP TABLE IF EXISTS `accounts_userprofile_follows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_userprofile_follows` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_userprofile_id` int(11) NOT NULL,
  `to_userprofile_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `from_userprofile_id` (`from_userprofile_id`,`to_userprofile_id`),
  KEY `accounts_userprofile_follows_1a986d56` (`from_userprofile_id`),
  KEY `accounts_userprofile_follows_f151dec5` (`to_userprofile_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_userprofile_follows`
--

LOCK TABLES `accounts_userprofile_follows` WRITE;
/*!40000 ALTER TABLE `accounts_userprofile_follows` DISABLE KEYS */;
INSERT INTO `accounts_userprofile_follows` VALUES (1,1,2),(2,2,1),(3,3,2),(4,3,1);
/*!40000 ALTER TABLE `accounts_userprofile_follows` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_blacklistitem`
--

DROP TABLE IF EXISTS `api_blacklistitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_blacklistitem` (
  `filterlistitem_ptr_id` int(11) NOT NULL,
  `type` varchar(40) NOT NULL,
  PRIMARY KEY (`filterlistitem_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_blacklistitem`
--

LOCK TABLES `api_blacklistitem` WRITE;
/*!40000 ALTER TABLE `api_blacklistitem` DISABLE KEYS */;
INSERT INTO `api_blacklistitem` VALUES (1,'blacklist'),(2,'blacklist'),(3,'blacklist'),(4,'blacklist'),(5,'blacklist'),(38,'blacklist'),(8,'blacklist'),(9,'blacklist'),(10,'blacklist'),(11,'blacklist'),(12,'blacklist'),(13,'blacklist'),(14,'blacklist'),(15,'blacklist'),(16,'blacklist'),(17,'blacklist'),(37,'blacklist'),(21,'blacklist'),(22,'blacklist'),(23,'blacklist'),(27,'blacklist'),(39,'blacklist');
/*!40000 ALTER TABLE `api_blacklistitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_eyehistory`
--

DROP TABLE IF EXISTS `api_eyehistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_eyehistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `src` varchar(40) NOT NULL,
  `url` varchar(2000) NOT NULL,
  `favIconUrl` varchar(2000) NOT NULL,
  `title` varchar(40) NOT NULL,
  `start_event` varchar(40) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_event` varchar(40) NOT NULL,
  `end_time` datetime NOT NULL,
  `total_time` int(11) NOT NULL,
  `humanize_time` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_eyehistory_e90f3816` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=162 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_eyehistory`
--

LOCK TABLES `api_eyehistory` WRITE;
/*!40000 ALTER TABLE `api_eyehistory` DISABLE KEYS */;
INSERT INTO `api_eyehistory` VALUES (1,1,'chrome','https://github.com/','https://github.com/favicon.ico','GitHub','focus','2013-03-07 22:35:44','blur','2013-03-07 22:36:25',40669,'a few seconds'),(2,1,'chrome','https://github.com/','https://github.com/favicon.ico','GitHub','focus','2013-03-07 22:36:25','blur','2013-03-07 22:36:39',14041,'a few seconds'),(3,1,'chrome','https://github.com/','https://github.com/favicon.ico','GitHub','focus','2013-03-07 22:36:39','blur','2013-03-07 22:36:41',1540,'a few seconds'),(4,1,'chrome','https://github.com/','https://github.com/favicon.ico','GitHub','update','2013-03-07 22:36:41','blur','2013-03-07 22:37:57',76107,'a minute'),(5,1,'chrome','https://github.com/','https://github.com/favicon.ico','GitHub','focus','2013-03-07 22:37:57','blur','2013-03-07 22:39:18',81536,'a minute'),(6,1,'chrome','https://github.com/','https://github.com/favicon.ico','GitHub','focus','2013-03-07 22:39:18','blur','2013-03-07 22:44:18',299572,'5 minutes'),(7,1,'chrome','https://app.asana.com/0/1322635282600/1322635282600','','Joshua’s joshblum Tasks - Asana','update','2013-03-07 22:44:24','blur','2013-03-07 22:44:44',20308,'a few seconds'),(8,1,'chrome','https://app.asana.com/0/1322635282600/1322635282600','https://app.asana.com/-/static/luna/browser/images/favicon.ico','Joshua’s joshblum Tasks - Asana','focus','2013-03-07 22:44:44','blur','2013-03-07 22:44:51',6713,'a few seconds'),(9,1,'chrome','https://github.com/','https://github.com/favicon.ico','GitHub','focus','2013-03-07 22:44:51','blur','2013-03-07 22:48:10',199403,'3 minutes'),(10,2,'chrome','http://stackoverflow.com/questions/7475223/mysql-config-not-found-when-installing-mysqldb-python-interface','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','linux - mysql_config not found when inst','update','2013-03-07 22:59:14','blur','2013-03-07 22:59:41',26499,'a few seconds'),(11,2,'chrome','http://stackoverflow.com/','','Stack Overflow','focus','2013-03-07 22:59:41','blur','2013-03-07 22:59:50',9269,'a few seconds'),(12,1,'chrome','http://www.heroku.com/','https://nav.heroku.com/images/logos/favicon.ico','Heroku | Cloud Application Platform','update','2013-03-07 23:02:13','blur','2013-03-07 23:02:23',10312,'a few seconds'),(13,2,'chrome','http://stackoverflow.com/questions','','Newest Questions - Stack Overflow','update','2013-03-07 22:59:50','blur','2013-03-07 23:02:32',161806,'3 minutes'),(14,2,'chrome','http://stackoverflow.com/questions','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','Newest Questions - Stack Overflow','focus','2013-03-07 23:02:32','blur','2013-03-07 23:02:34',2365,'a few seconds'),(15,1,'chrome','https://dashboard.heroku.com/apps','https://dqegdwgdd0yjs.cloudfront.net/assets/favicon-4b8fc5ed8423fc1d06847636fb10eee1.ico','Heroku | Apps','update','2013-03-07 23:02:23','blur','2013-03-07 23:03:40',76844,'a minute'),(16,2,'chrome','http://stackoverflow.com/questions','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','Newest Questions - Stack Overflow','focus','2013-03-07 23:02:34','blur','2013-03-07 23:03:49',74267,'a minute'),(17,2,'chrome','http://stackoverflow.com/questions','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','Newest Questions - Stack Overflow','focus','2013-03-07 23:03:49','blur','2013-03-07 23:04:59',70934,'a minute'),(18,1,'chrome','https://dashboard.heroku.com/apps','https://dqegdwgdd0yjs.cloudfront.net/assets/favicon-4b8fc5ed8423fc1d06847636fb10eee1.ico','Heroku | Apps','focus','2013-03-07 23:03:40','blur','2013-03-07 23:19:53',972874,'16 minutes'),(19,1,'chrome','https://dashboard.heroku.com/apps','https://dqegdwgdd0yjs.cloudfront.net/assets/favicon-4b8fc5ed8423fc1d06847636fb10eee1.ico','Heroku | Apps','focus','2013-03-07 23:19:53','blur','2013-03-07 23:21:02',68907,'a minute'),(20,3,'chrome','http://stackoverflow.com/questions/907042/possible-to-assign-to-multiple-variables-from-an-array','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','javascript - Possible to assign to multi','update','2013-03-07 23:22:19','blur','2013-03-07 23:22:37',18391,'a few seconds'),(21,2,'chrome','http://stackoverflow.com/questions','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','Newest Questions - Stack Overflow','focus','2013-03-07 23:04:59','blur','2013-03-07 23:25:36',1236354,'21 minutes'),(22,3,'chrome','https://github.com/joshblum/eyebrowse-server','https://github.com/favicon.ico','joshblum/eyebrowse-server · GitHub','update','2013-03-07 23:22:37','blur','2013-03-07 23:26:38',241255,'4 minutes'),(23,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','update','2013-03-07 23:26:38','blur','2013-03-07 23:29:10',151855,'3 minutes'),(24,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','update','2013-03-07 23:29:10','blur','2013-03-07 23:29:13',2964,'a few seconds'),(25,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','update','2013-03-07 23:29:13','blur','2013-03-07 23:29:22',8752,'a few seconds'),(26,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/?','','eyebrowse | Profile','update','2013-03-07 23:29:22','blur','2013-03-07 23:29:47',25545,'a few seconds'),(27,3,'chrome','http://eyebrowse.herokuapp.com/users/joshblum','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','update','2013-03-07 23:29:47','blur','2013-03-07 23:31:32',104216,'2 minutes'),(28,3,'chrome','http://eyebrowse.herokuapp.com/users/joshblum','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','update','2013-03-07 23:29:47','blur','2013-03-07 23:31:32',104216,'2 minutes'),(29,3,'chrome','http://eyebrowse.herokuapp.com/users/joshblum','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','focus','2013-03-07 23:31:32','blur','2013-03-07 23:31:33',1502,'a few seconds'),(30,3,'chrome','http://eyebrowse.herokuapp.com/users/joshblum','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','focus','2013-03-07 23:31:33','blur','2013-03-07 23:31:46',13078,'a few seconds'),(31,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','update','2013-03-07 23:31:46','blur','2013-03-07 23:31:57',10387,'a few seconds'),(32,2,'chrome','http://stackoverflow.com/questions/3186051/find-and-remove-iframe','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','jquery - Find and remove IFrame - Stack ','focus','2013-03-07 23:25:36','blur','2013-03-07 23:32:08',392137,'7 minutes'),(33,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/?filter=search','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','update','2013-03-07 23:31:57','blur','2013-03-07 23:32:26',29382,'a few seconds'),(34,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','update','2013-03-07 23:32:26','blur','2013-03-07 23:32:36',9696,'a few seconds'),(35,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/?filter=firehose','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','update','2013-03-07 23:32:36','blur','2013-03-07 23:33:17',40852,'a few seconds'),(36,2,'chrome','http://stackoverflow.com/questions/3186051/find-and-remove-iframe','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','jquery - Find and remove IFrame - Stack ','focus','2013-03-07 23:32:08','blur','2013-03-07 23:33:54',105948,'2 minutes'),(37,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','update','2013-03-07 23:33:17','blur','2013-03-07 23:34:13',56005,'a minute'),(38,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','focus','2013-03-07 23:34:13','blur','2013-03-07 23:34:19',6836,'a few seconds'),(39,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','update','2013-03-07 23:34:19','blur','2013-03-07 23:34:24',4840,'a few seconds'),(40,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/?filter=firehose','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','update','2013-03-07 23:34:24','blur','2013-03-07 23:34:38',14111,'a few seconds'),(41,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','update','2013-03-07 23:34:38','blur','2013-03-07 23:35:10',32096,'a few seconds'),(42,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','focus','2013-03-07 23:35:10','blur','2013-03-07 23:35:25',14396,'a few seconds'),(43,1,'chrome','http://stackoverflow.com/questions/2049109/how-to-import-sql-into-sqlite3','','sqlite - how to import .sql into sqlite3','update','2013-03-07 23:21:02','blur','2013-03-07 23:35:23',861534,'14 minutes'),(44,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','focus','2013-03-07 23:35:25','blur','2013-03-07 23:35:53',27925,'a few seconds'),(45,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','focus','2013-03-07 23:35:53','blur','2013-03-07 23:36:45',52336,'a minute'),(46,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','focus','2013-03-07 23:36:45','blur','2013-03-07 23:36:58',12752,'a few seconds'),(47,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/edit','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Edit Profile','update','2013-03-07 23:36:58','blur','2013-03-07 23:37:00',2143,'a few seconds'),(48,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/edit#whitelist','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Edit Profile','update','2013-03-07 23:37:00','blur','2013-03-07 23:38:55',114648,'2 minutes'),(49,3,'chrome','https://github.com/','https://github.com/favicon.ico','GitHub','update','2013-03-07 23:38:55','blur','2013-03-07 23:39:16',21766,'a few seconds'),(50,3,'chrome','https://github.com/','https://github.com/favicon.ico','GitHub','focus','2013-03-07 23:39:16','blur','2013-03-07 23:41:02',105627,'2 minutes'),(51,3,'chrome','https://github.com/joshblum/eyebrowse-server','https://github.com/favicon.ico','joshblum/eyebrowse-server · GitHub','focus','2013-03-07 23:41:02','blur','2013-03-07 23:41:04',1888,'a few seconds'),(52,3,'chrome','http://stackoverflow.com/questions/907042/possible-to-assign-to-multiple-variables-from-an-array','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','javascript - Possible to assign to multi','focus','2013-03-07 23:41:04','blur','2013-03-07 23:41:07',2641,'a few seconds'),(53,3,'chrome','http://stackoverflow.com/questions/907042/possible-to-assign-to-multiple-variables-from-an-array','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','javascript - Possible to assign to multi','focus','2013-03-07 23:41:04','blur','2013-03-07 23:41:07',2641,'a few seconds'),(54,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/edit#whitelist','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Edit Profile','focus','2013-03-07 23:41:07','blur','2013-03-07 23:41:08',1054,'a few seconds'),(55,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/edit#whitelist','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Edit Profile','focus','2013-03-07 23:41:08','blur','2013-03-07 23:41:32',24241,'a few seconds'),(56,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/edit#whitelist','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Edit Profile','focus','2013-03-07 23:41:32','blur','2013-03-07 23:41:33',1609,'a few seconds'),(57,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/edit#whitelist','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Edit Profile','focus','2013-03-07 23:41:33','blur','2013-03-07 23:42:28',54837,'a minute'),(58,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/edit#whitelist','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Edit Profile','focus','2013-03-07 23:42:28','blur','2013-03-07 23:42:33',5063,'a few seconds'),(59,1,'chrome','https://groups.mit.edu/webmoira/','https://groups.mit.edu/favicon.ico','WebMoira List Manager : Joshua M Blum','update','2013-03-07 23:35:23','blur','2013-03-07 23:42:40',436871,'7 minutes'),(60,1,'chrome','http://dev.mysql.com/doc/refman/5.1/en/privileges-provided.html','http://dev.mysql.com/common/themes/sakila/favicon.ico','MySQL :: MySQL 5.1 Reference Manual :: 6','focus','2013-03-07 23:42:40','blur','2013-03-07 23:43:14',34046,'a few seconds'),(61,1,'chrome','http://dev.mysql.com/doc/refman/5.1/en/privileges-provided.html#priv_grant-option','','MySQL :: MySQL 5.1 Reference Manual :: 6','update','2013-03-07 23:43:14','blur','2013-03-07 23:43:16',1843,'a few seconds'),(62,1,'chrome','http://dev.mysql.com/doc/refman/5.1/en/privileges-provided.html','http://dev.mysql.com/common/themes/sakila/favicon.ico','MySQL :: MySQL 5.1 Reference Manual :: 6','focus','2013-03-07 23:42:40','blur','2013-03-07 23:43:14',34046,'a few seconds'),(63,2,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/?filter=firehose','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','update','2013-03-07 23:33:54','blur','2013-03-07 23:43:37',583087,'10 minutes'),(64,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/edit#whitelist','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Edit Profile','focus','2013-03-07 23:42:33','blur','2013-03-07 23:43:43',69589,'a minute'),(65,2,'chrome','http://stackoverflow.com/questions/10299148/mysql-error-1045-28000-access-denied-for-user-billlocalhost-using-passw','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','MySQL ERROR 1045 (28000): Access denied ','focus','2013-03-07 23:43:37','blur','2013-03-07 23:44:08',30571,'a few seconds'),(66,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/edit#whitelist','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Edit Profile','focus','2013-03-07 23:43:43','blur','2013-03-07 23:44:27',44070,'a few seconds'),(67,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','update','2013-03-07 23:44:27','blur','2013-03-07 23:44:45',18351,'a few seconds'),(68,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','update','2013-03-07 23:44:45','blur','2013-03-07 23:44:54',8955,'a few seconds'),(69,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','update','2013-03-07 23:44:54','blur','2013-03-07 23:44:58',3828,'a few seconds'),(70,2,'chrome','http://stackoverflow.com/questions/10299148/mysql-error-1045-28000-access-denied-for-user-billlocalhost-using-passw','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','MySQL ERROR 1045 (28000): Access denied ','update','2013-03-07 23:44:08','blur','2013-03-07 23:45:38',90110,'2 minutes'),(71,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','update','2013-03-07 23:44:58','blur','2013-03-07 23:45:44',45700,'a minute'),(72,2,'chrome','http://stackoverflow.com/questions/10299148/mysql-error-1045-28000-access-denied-for-user-billlocalhost-using-passw','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','MySQL ERROR 1045 (28000): Access denied ','focus','2013-03-07 23:45:38','blur','2013-03-07 23:45:41',3494,'a few seconds'),(73,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','focus','2013-03-07 23:45:44','blur','2013-03-07 23:45:57',13417,'a few seconds'),(74,2,'chrome','http://stackoverflow.com/questions/11657829/error-2002-hy000-cant-connect-to-local-mysql-server-through-socket-var-run','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','linux - ERROR 2002 (HY000): Can\'t connec','focus','2013-03-07 23:45:41','blur','2013-03-07 23:46:29',47568,'a minute'),(75,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','update','2013-03-07 23:45:57','blur','2013-03-07 23:47:10',72731,'a minute'),(76,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','update','2013-03-07 23:47:10','blur','2013-03-07 23:48:06',55960,'a minute'),(77,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','focus','2013-03-07 23:48:06','blur','2013-03-07 23:48:51',45115,'a minute'),(78,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','focus','2013-03-07 23:48:51','blur','2013-03-07 23:49:10',19095,'a few seconds'),(79,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','update','2013-03-07 23:49:10','blur','2013-03-07 23:49:52',42235,'a few seconds'),(80,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','update','2013-03-07 23:49:52','blur','2013-03-07 23:49:54',1765,'a few seconds'),(81,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','update','2013-03-07 23:49:54','blur','2013-03-07 23:50:11',16492,'a few seconds'),(82,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','update','2013-03-07 23:50:11','blur','2013-03-07 23:50:13',2541,'a few seconds'),(83,3,'chrome','http://eyebrowse.herokuapp.com/users/jason','','eyebrowse | Profile','update','2013-03-07 23:50:13','blur','2013-03-07 23:50:25',12250,'a few seconds'),(84,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','update','2013-03-07 23:50:26','blur','2013-03-07 23:50:31',5505,'a few seconds'),(85,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/edit','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Edit Profile','update','2013-03-07 23:50:31','blur','2013-03-07 23:50:38',6620,'a few seconds'),(86,3,'chrome','http://eyebrowse.herokuapp.com/accounts/profile/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Profile','update','2013-03-07 23:50:38','blur','2013-03-07 23:51:10',32570,'a few seconds'),(87,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','update','2013-03-07 23:51:10','blur','2013-03-07 23:51:16',5558,'a few seconds'),(88,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','update','2013-03-07 23:51:16','blur','2013-03-07 23:51:20',4535,'a few seconds'),(89,3,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','update','2013-03-07 23:51:20','blur','2013-03-07 23:52:53',92345,'2 minutes'),(90,3,'chrome','http://stackoverflow.com/questions/5764494/how-to-use-python-virtualenv','','How to use Python virtualenv - Stack Ove','update','2013-03-07 23:52:53','blur','2013-03-07 23:54:06',73106,'a minute'),(91,2,'chrome','http://stackoverflow.com/questions/7927854/start-mysql-server-from-command-line-on-mac-os-lion','','osx - start mySQL server from command li','update','2013-03-07 23:46:29','blur','2013-03-07 23:57:54',685464,'11 minutes'),(92,1,'chrome','http://dev.mysql.com/doc/refman/5.1/en/privileges-provided.html','http://dev.mysql.com/common/themes/sakila/favicon.ico','MySQL :: MySQL 5.1 Reference Manual :: 6','update','2013-03-07 23:43:16','blur','2013-03-08 00:00:19',1023151,'17 minutes'),(93,1,'chrome','http://www.heroku.com/','','New Tab','update','2013-03-08 00:00:19','blur','2013-03-08 00:00:21',1433,'a few seconds'),(94,1,'chrome','http://www.heroku.com/','https://nav.heroku.com/images/logos/favicon.ico','Heroku | Cloud Application Platform','update','2013-03-08 00:00:21','blur','2013-03-08 00:00:25',4030,'a few seconds'),(95,3,'chrome','http://stackoverflow.com/questions/5764494/how-to-use-python-virtualenv','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','How to use Python virtualenv - Stack Ove','focus','2013-03-07 23:54:06','blur','2013-03-08 00:00:38',391749,'7 minutes'),(96,3,'chrome','http://stackoverflow.com/questions/10269002/where-does-google-chrome-store-unpacked-extensions','','Where does google chrome store unpacked ','update','2013-03-08 00:00:38','blur','2013-03-08 00:01:54',76889,'a minute'),(97,1,'chrome','https://dashboard.heroku.com/apps','https://dqegdwgdd0yjs.cloudfront.net/assets/favicon-4b8fc5ed8423fc1d06847636fb10eee1.ico','Heroku | Apps','update','2013-03-08 00:00:25','blur','2013-03-08 00:03:29',184507,'3 minutes'),(98,1,'chrome','https://devcenter.heroku.com/articles/config-vars','https://devcenter.heroku.com/favicon.ico','Configuration and Config Vars | Heroku D','update','2013-03-08 00:03:29','blur','2013-03-08 00:09:00',330742,'6 minutes'),(99,1,'chrome','http://stackoverflow.com/questions/2294313/how-to-download-a-branch-with-git','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','How to download a branch with git? - Sta','focus','2013-03-08 00:09:00','blur','2013-03-08 00:11:33',153287,'3 minutes'),(100,1,'chrome','http://stackoverflow.com/questions/2294313/how-to-download-a-branch-with-git','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','How to download a branch with git? - Sta','focus','2013-03-08 00:11:33','blur','2013-03-08 00:12:41',68202,'a minute'),(101,1,'chrome','https://github.com/','https://github.com/favicon.ico','GitHub','update','2013-03-08 00:12:41','blur','2013-03-08 00:12:44',2854,'a few seconds'),(102,1,'chrome','https://github.com/joshblum/eyebrowse-server','https://github.com/favicon.ico','joshblum/eyebrowse-server · GitHub','update','2013-03-08 00:12:44','blur','2013-03-08 00:14:11',87187,'a minute'),(103,1,'chrome','https://github.com/joshblum/eyebrowse-server','https://github.com/favicon.ico','joshblum/eyebrowse-server · GitHub','focus','2013-03-08 00:14:11','blur','2013-03-08 00:15:30',78916,'a minute'),(104,1,'chrome','http://stackoverflow.com/questions/6930147/git-pull-displays-fatal-couldnt-find-remote-ref-refs-heads-xxxx-and-hungs-up','','git pull displays fatal: Couldn\'t find r','update','2013-03-08 00:15:30','blur','2013-03-08 00:17:10',99235,'2 minutes'),(105,2,'chrome','http://eyebrowse.herokuapp.com/live_stream/home/?filter=firehose','http://eyebrowse.herokuapp.com/static/common/img/favicon.ico','eyebrowse | Live Stream','focus','2013-03-07 23:57:54','blur','2013-03-08 00:17:23',1169117,'19 minutes'),(106,1,'chrome','http://stackoverflow.com/questions/6930147/git-pull-displays-fatal-couldnt-find-remote-ref-refs-heads-xxxx-and-hungs-up','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','git pull displays fatal: Couldn\'t find r','focus','2013-03-08 00:17:10','blur','2013-03-08 00:17:37',27788,'a few seconds'),(107,1,'chrome','http://stackoverflow.com/questions/6656619/git-and-nasty-error-cannot-lock-existing-info-refs-fatal','','Git and nasty \"error: cannot lock existi','update','2013-03-08 00:17:37','blur','2013-03-08 00:18:16',38430,'a few seconds'),(108,3,'chrome','http://stackoverflow.com/questions/10269002/where-does-google-chrome-store-unpacked-extensions','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','Where does google chrome store unpacked ','focus','2013-03-08 00:01:54','blur','2013-03-08 00:19:17',1042176,'17 minutes'),(109,1,'chrome','http://stackoverflow.com/questions/11245897/push-to-remote-repo-gives-the-error-there-are-still-refs-under','','git - push to remote repo gives the erro','update','2013-03-08 00:18:16','blur','2013-03-08 00:19:58',102581,'2 minutes'),(110,2,'chrome','http://stackoverflow.com/questions/1783405/git-checkout-remote-branch','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','git checkout remote branch - Stack Overf','focus','2013-03-08 00:17:23','blur','2013-03-08 00:24:17',413705,'7 minutes'),(111,2,'chrome','http://stackoverflow.com/questions/1783405/git-checkout-remote-branch','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','git checkout remote branch - Stack Overf','focus','2013-03-08 00:17:23','blur','2013-03-08 00:24:17',413705,'7 minutes'),(112,2,'chrome','http://stackoverflow.com/questions/1783405/git-checkout-remote-branch','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','git checkout remote branch - Stack Overf','focus','2013-03-08 00:24:17','blur','2013-03-08 00:24:21',4173,'a few seconds'),(113,1,'chrome','http://stackoverflow.com/questions/11245897/push-to-remote-repo-gives-the-error-there-are-still-refs-under','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','git - push to remote repo gives the erro','focus','2013-03-08 00:19:58','blur','2013-03-08 00:28:33',514588,'9 minutes'),(114,1,'chrome','http://stackoverflow.com/questions/8584064/refname-is-ambiguous-and-pull-failing','','git - refname is ambiguous and pull fail','update','2013-03-08 00:28:33','blur','2013-03-08 00:30:14',100727,'2 minutes'),(115,2,'chrome','http://stackoverflow.com/questions/945654/git-checkout-on-a-remote-branch-does-not-work','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','Git checkout on a remote branch does not','focus','2013-03-08 00:24:21','blur','2013-03-08 00:30:35',373373,'6 minutes'),(116,2,'chrome','http://stackoverflow.com/questions/945654/git-checkout-on-a-remote-branch-does-not-work','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','Git checkout on a remote branch does not','focus','2013-03-08 00:30:35','blur','2013-03-08 00:32:23',108325,'2 minutes'),(117,2,'chrome','http://stackoverflow.com/questions/945654/git-checkout-on-a-remote-branch-does-not-work','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','Git checkout on a remote branch does not','focus','2013-03-08 00:30:35','blur','2013-03-08 00:32:23',108325,'2 minutes'),(118,2,'chrome','http://stackoverflow.com/questions/945654/git-checkout-on-a-remote-branch-does-not-work','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','Git checkout on a remote branch does not','focus','2013-03-08 00:32:23','blur','2013-03-08 00:32:27',3724,'a few seconds'),(119,1,'chrome','http://stackoverflow.com/questions/2003505/how-do-i-delete-a-git-branch-both-locally-and-in-github','','How do I delete a Git branch both locall','update','2013-03-08 00:30:14','blur','2013-03-08 00:33:17',183680,'3 minutes'),(120,1,'chrome','http://stackoverflow.com/questions/2003505/how-do-i-delete-a-git-branch-both-locally-and-in-github','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','How do I delete a Git branch both locall','focus','2013-03-08 00:33:17','blur','2013-03-08 00:33:20',2175,'a few seconds'),(121,1,'chrome','https://github.com/','https://github.com/favicon.ico','GitHub','update','2013-03-08 00:33:20','blur','2013-03-08 00:33:23',3601,'a few seconds'),(122,1,'chrome','http://stackoverflow.com/questions/2003505/how-do-i-delete-a-git-branch-both-locally-and-in-github','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','How do I delete a Git branch both locall','focus','2013-03-08 00:33:17','blur','2013-03-08 00:33:20',2175,'a few seconds'),(123,1,'chrome','https://github.com/','https://github.com/favicon.ico','GitHub','update','2013-03-08 00:33:20','blur','2013-03-08 00:33:23',3601,'a few seconds'),(124,1,'chrome','https://github.com/joshblum/eyebrowse-server','https://github.com/favicon.ico','joshblum/eyebrowse-server · GitHub','update','2013-03-08 00:33:23','blur','2013-03-08 00:33:27',3873,'a few seconds'),(125,2,'chrome','http://stackoverflow.com/questions/5280212/error-on-branch-creation-warning-refname-master-is-ambiguous','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','git - Error on branch creation: \"warning','focus','2013-03-08 00:32:27','blur','2013-03-08 00:34:31',124029,'2 minutes'),(126,2,'chrome','http://stackoverflow.com/questions/5280212/error-on-branch-creation-warning-refname-master-is-ambiguous','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','git - Error on branch creation: \"warning','focus','2013-03-08 00:32:27','blur','2013-03-08 00:34:31',124029,'2 minutes'),(127,2,'chrome','http://stackoverflow.com/questions/5280212/error-on-branch-creation-warning-refname-master-is-ambiguous','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','git - Error on branch creation: \"warning','focus','2013-03-08 00:34:31','blur','2013-03-08 00:34:32',938,'a few seconds'),(128,1,'chrome','http://stackoverflow.com/questions/2003505/how-do-i-delete-a-git-branch-both-locally-and-in-github','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','How do I delete a Git branch both locall','focus','2013-03-08 00:33:27','blur','2013-03-08 00:35:37',130178,'2 minutes'),(129,1,'chrome','http://stackoverflow.com/questions/2003505/how-do-i-delete-a-git-branch-both-locally-and-in-github','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','How do I delete a Git branch both locall','focus','2013-03-08 00:35:37','blur','2013-03-08 00:35:40',3139,'a few seconds'),(130,1,'chrome','http://stackoverflow.com/questions/8584064/refname-is-ambiguous-and-pull-failing','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','git - refname is ambiguous and pull fail','focus','2013-03-08 00:35:40','blur','2013-03-08 00:35:41',1146,'a few seconds'),(131,1,'chrome','http://stackoverflow.com/questions/11245897/push-to-remote-repo-gives-the-error-there-are-still-refs-under','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','git - push to remote repo gives the erro','focus','2013-03-08 00:35:41','blur','2013-03-08 00:35:43',1152,'a few seconds'),(132,1,'chrome','https://github.com/joshblum/eyebrowse-server','https://github.com/favicon.ico','joshblum/eyebrowse-server · GitHub','focus','2013-03-08 00:35:43','blur','2013-03-08 00:35:46',3862,'a few seconds'),(133,2,'chrome','http://stackoverflow.com/questions/5280212/error-on-branch-creation-warning-refname-master-is-ambiguous','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','git - Error on branch creation: \"warning','focus','2013-03-08 00:34:32','blur','2013-03-08 00:36:11',99549,'2 minutes'),(134,1,'chrome','http://stackoverflow.com/questions/2294313/how-to-download-a-branch-with-git','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','How to download a branch with git? - Sta','focus','2013-03-08 00:35:46','blur','2013-03-08 00:36:15',28595,'a few seconds'),(135,2,'chrome','http://stackoverflow.com/questions/5280212/error-on-branch-creation-warning-refname-master-is-ambiguous','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','git - Error on branch creation: \"warning','focus','2013-03-08 00:36:11','blur','2013-03-08 00:36:16',4446,'a few seconds'),(136,2,'chrome','http://stackoverflow.com/questions/1692892/warning-refname-head-is-ambiguous','','git - warning: refname \'HEAD\' is ambiguo','update','2013-03-08 00:36:16','blur','2013-03-08 00:40:46',270393,'5 minutes'),(137,2,'chrome','http://stackoverflow.com/questions/1692892/warning-refname-head-is-ambiguous','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','git - warning: refname \'HEAD\' is ambiguo','focus','2013-03-08 00:40:46','blur','2013-03-08 00:40:53',7007,'a few seconds'),(138,1,'chrome','http://stackoverflow.com/questions/1045910/how-can-i-import-load-a-sql-or-csv-file-into-sqlite','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','ruby on rails - How can I import load a ','focus','2013-03-08 00:36:15','blur','2013-03-08 00:44:20',484509,'8 minutes'),(139,1,'chrome','http://www.heroku.com/','','New Tab','update','2013-03-08 00:44:20','blur','2013-03-08 00:44:21',1257,'a few seconds'),(140,1,'chrome','http://www.heroku.com/','https://nav.heroku.com/images/logos/favicon.ico','Heroku | Cloud Application Platform','update','2013-03-08 00:44:21','blur','2013-03-08 00:44:23',2636,'a few seconds'),(141,1,'chrome','https://dashboard.heroku.com/apps','https://dqegdwgdd0yjs.cloudfront.net/assets/favicon-4b8fc5ed8423fc1d06847636fb10eee1.ico','Heroku | Apps','update','2013-03-08 00:44:23','blur','2013-03-08 00:44:26',2475,'a few seconds'),(142,1,'chrome','https://dashboard.heroku.com/apps/eyebrowse-staging/resources','','Resources | eyebrowse-staging','update','2013-03-08 00:44:26','blur','2013-03-08 00:44:28',2207,'a few seconds'),(143,1,'chrome','https://dashboard.heroku.com/apps/eyebrowse-staging/collaborators','','Collaborators | eyebrowse-staging','update','2013-03-08 00:44:28','blur','2013-03-08 00:44:35',7040,'a few seconds'),(144,1,'chrome','https://dashboard.heroku.com/apps/eyebrowse-staging/collaborators','https://dqegdwgdd0yjs.cloudfront.net/assets/favicon-4b8fc5ed8423fc1d06847636fb10eee1.ico','Collaborators | eyebrowse-staging','update','2013-03-08 00:44:35','blur','2013-03-08 00:44:41',5934,'a few seconds'),(145,1,'chrome','https://dashboard.heroku.com/apps/eyebrowse-staging/collaborators','https://dqegdwgdd0yjs.cloudfront.net/assets/favicon-4b8fc5ed8423fc1d06847636fb10eee1.ico','Collaborators | eyebrowse-staging','update','2013-03-08 00:44:41','blur','2013-03-08 00:46:18',96551,'2 minutes'),(146,1,'chrome','https://dashboard.heroku.com/apps/eyebrowse-staging/collaborators','https://dqegdwgdd0yjs.cloudfront.net/assets/favicon-4b8fc5ed8423fc1d06847636fb10eee1.ico','Collaborators | eyebrowse-staging','focus','2013-03-08 00:46:18','blur','2013-03-08 00:47:37',79236,'a minute'),(147,1,'chrome','https://dashboard.heroku.com/apps/eyebrowse-staging/collaborators','https://dqegdwgdd0yjs.cloudfront.net/assets/favicon-4b8fc5ed8423fc1d06847636fb10eee1.ico','Collaborators | eyebrowse-staging','focus','2013-03-08 00:47:37','blur','2013-03-08 00:47:38',1091,'a few seconds'),(148,1,'chrome','https://dashboard.heroku.com/apps/eyebrowse-staging/collaborators','https://dqegdwgdd0yjs.cloudfront.net/assets/favicon-4b8fc5ed8423fc1d06847636fb10eee1.ico','Collaborators | eyebrowse-staging','focus','2013-03-08 00:47:38','blur','2013-03-08 00:49:33',114749,'2 minutes'),(149,2,'chrome','http://stackoverflow.com/questions/8839958/how-does-origin-head-get-set','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','git - How does origin/HEAD get set? - St','focus','2013-03-08 00:40:53','blur','2013-03-08 00:51:30',637342,'11 minutes'),(150,2,'chrome','http://stackoverflow.com/questions/8839958/how-does-origin-head-get-set','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','git - How does origin/HEAD get set? - St','focus','2013-03-08 00:51:30','blur','2013-03-08 00:57:15',344132,'6 minutes'),(151,1,'chrome','https://dashboard.heroku.com/apps/eyebrowse-staging/collaborators','https://dqegdwgdd0yjs.cloudfront.net/assets/favicon-4b8fc5ed8423fc1d06847636fb10eee1.ico','Collaborators | eyebrowse-staging','focus','2013-03-08 00:49:33','blur','2013-03-08 01:12:22',1369358,'23 minutes'),(152,1,'chrome','http://github.com/','','New Tab','update','2013-03-08 01:12:22','blur','2013-03-08 01:12:23',1160,'a few seconds'),(153,1,'chrome','https://github.com/','https://github.com/favicon.ico','GitHub','update','2013-03-08 01:12:23','blur','2013-03-08 01:12:26',3016,'a few seconds'),(154,1,'chrome','https://github.com/joshblum/comm.prod','https://github.com/favicon.ico','joshblum/comm.prod · GitHub','update','2013-03-08 01:12:26','blur','2013-03-08 01:12:29',2713,'a few seconds'),(155,1,'chrome','https://github.com/joshblum/comm.prod/tree/master/scripts','','joshblum/comm.prod · GitHub','update','2013-03-08 01:12:29','blur','2013-03-08 01:12:30',1446,'a few seconds'),(156,1,'chrome','https://github.com/joshblum/comm.prod/blob/master/scripts/import_db.sh','','comm.prod/scripts at master · joshblum/c','update','2013-03-08 01:12:30','blur','2013-03-08 01:18:40',369038,'6 minutes'),(157,1,'chrome','http://stackoverflow.com/questions/2050581/how-to-delete-mysql-database-through-shell-command','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','linux - how to delete mysql database thr','focus','2013-03-08 01:18:40','blur','2013-03-08 01:20:39',119471,'2 minutes'),(158,1,'chrome','http://stackoverflow.com/questions/2050581/how-to-delete-mysql-database-through-shell-command','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','linux - how to delete mysql database thr','focus','2013-03-08 01:20:39','blur','2013-03-08 01:21:49',69878,'a minute'),(159,1,'chrome','http://stackoverflow.com/questions/2050581/how-to-delete-mysql-database-through-shell-command','http://cdn.sstatic.net/stackoverflow/img/favicon.ico','linux - how to delete mysql database thr','focus','2013-03-08 01:21:49','blur','2013-03-08 01:22:07',18526,'a few seconds'),(160,1,'chrome','http://stackoverflow.com/questions/9449899/how-to-execute-sql-variable-with-mysqlcommand-in-vb','','mysql - How to execute sql variable with','update','2013-03-08 01:22:07','blur','2013-03-08 01:22:15',8067,'a few seconds'),(161,1,'chrome','http://stackoverflow.com/questions/76065/how-do-i-pass-a-variable-to-a-mysql-script','','How do I pass a variable to a mysql scri','update','2013-03-08 01:22:15','blur','2013-03-08 01:22:26',10055,'a few seconds');
/*!40000 ALTER TABLE `api_eyehistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_filterlistitem`
--

DROP TABLE IF EXISTS `api_filterlistitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_filterlistitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `url` varchar(2000) NOT NULL,
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_filterlistitem_e90f3816` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=40 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_filterlistitem`
--

LOCK TABLES `api_filterlistitem` WRITE;
/*!40000 ALTER TABLE `api_filterlistitem` DISABLE KEYS */;
INSERT INTO `api_filterlistitem` VALUES (1,1,'https://google.com','2013-03-07 22:31:18'),(2,1,'http://google.com','2013-03-07 22:31:19'),(3,1,'localhost','2013-03-07 22:31:19'),(4,1,'chrome','2013-03-07 22:31:19'),(5,1,'chrome-devtools','2013-03-07 22:31:19'),(39,1,'eyebrowse.herokuapp.com','2013-03-08 01:14:02'),(7,1,'github.com','2013-03-07 22:34:00'),(8,2,'https://google.com','2013-03-07 22:34:49'),(9,2,'http://google.com','2013-03-07 22:34:49'),(10,2,'localhost','2013-03-07 22:34:49'),(11,2,'chrome','2013-03-07 22:34:49'),(12,2,'chrome-devtools','2013-03-07 22:34:49'),(13,3,'https://google.com','2013-03-07 22:43:44'),(14,3,'http://google.com','2013-03-07 22:43:44'),(15,3,'localhost','2013-03-07 22:43:44'),(16,3,'chrome','2013-03-07 22:43:44'),(17,3,'chrome-devtools','2013-03-07 22:43:44'),(21,2,'app.asana.com','2013-03-07 22:48:28'),(22,2,'app.asana.com','2013-03-07 22:48:28'),(32,3,'eyebrowse.herokuapp.com','2013-03-07 23:29:08'),(23,2,'www.google.com','2013-03-07 22:57:41'),(24,2,'stackoverflow.com','2013-03-07 22:59:15'),(25,1,'www.heroku.com','2013-03-07 23:02:13'),(26,1,'dashboard.heroku.com','2013-03-07 23:02:24'),(27,1,'www.google.com','2013-03-07 23:20:04'),(28,1,'stackoverflow.com','2013-03-07 23:21:03'),(29,3,'stackoverflow.com','2013-03-07 23:22:17'),(30,3,'github.com','2013-03-07 23:22:36'),(33,2,'eyebrowse.herokuapp.com','2013-03-07 23:34:01'),(34,1,'groups.mit.edu','2013-03-07 23:35:24'),(35,1,'dev.mysql.com','2013-03-07 23:42:40'),(36,1,'devcenter.heroku.com','2013-03-08 00:03:30'),(37,1,'eyebrowse-staging.herokuapp.com','2013-03-08 00:06:36'),(38,1,'www.facebook.com','2013-03-08 00:37:24');
/*!40000 ALTER TABLE `api_filterlistitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_whitelistitem`
--

DROP TABLE IF EXISTS `api_whitelistitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_whitelistitem` (
  `filterlistitem_ptr_id` int(11) NOT NULL,
  `type` varchar(40) NOT NULL,
  PRIMARY KEY (`filterlistitem_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_whitelistitem`
--

LOCK TABLES `api_whitelistitem` WRITE;
/*!40000 ALTER TABLE `api_whitelistitem` DISABLE KEYS */;
INSERT INTO `api_whitelistitem` VALUES (7,'whitelist'),(25,'whitelist'),(24,'whitelist'),(26,'whitelist'),(28,'whitelist'),(29,'whitelist'),(30,'whitelist'),(32,'whitelist'),(33,'whitelist'),(34,'whitelist'),(35,'whitelist'),(36,'whitelist');
/*!40000 ALTER TABLE `api_whitelistitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_8b07cf5` (`group_id`),
  KEY `auth_group_permissions_6f299768` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_7e19a021` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=52 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add log entry',7,'add_logentry'),(20,'Can change log entry',7,'change_logentry'),(21,'Can delete log entry',7,'delete_logentry'),(22,'Can add version',8,'add_version'),(23,'Can change version',8,'change_version'),(24,'Can delete version',8,'delete_version'),(25,'Can add evolution',9,'add_evolution'),(26,'Can change evolution',9,'change_evolution'),(27,'Can delete evolution',9,'delete_evolution'),(28,'Can add registration profile',10,'add_registrationprofile'),(29,'Can change registration profile',10,'change_registrationprofile'),(30,'Can delete registration profile',10,'delete_registrationprofile'),(31,'Can add api access',11,'add_apiaccess'),(32,'Can change api access',11,'change_apiaccess'),(33,'Can delete api access',11,'delete_apiaccess'),(34,'Can add api key',12,'add_apikey'),(35,'Can change api key',12,'change_apikey'),(36,'Can delete api key',12,'delete_apikey'),(37,'Can add user profile',13,'add_userprofile'),(38,'Can change user profile',13,'change_userprofile'),(39,'Can delete user profile',13,'delete_userprofile'),(40,'Can add filter list item',14,'add_filterlistitem'),(41,'Can change filter list item',14,'change_filterlistitem'),(42,'Can delete filter list item',14,'delete_filterlistitem'),(43,'Can add white list item',15,'add_whitelistitem'),(44,'Can change white list item',15,'change_whitelistitem'),(45,'Can delete white list item',15,'delete_whitelistitem'),(46,'Can add black list item',16,'add_blacklistitem'),(47,'Can change black list item',16,'change_blacklistitem'),(48,'Can delete black list item',16,'delete_blacklistitem'),(49,'Can add eye history',17,'add_eyehistory'),(50,'Can change eye history',17,'change_eyehistory'),(51,'Can delete eye history',17,'delete_eyehistory');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'joshblum','','','joshblum@mit.edu','pbkdf2_sha256$10000$Vsh59wDtGFdx$aHKv3hBiPt1nBVlaUHB8B4K2ja09da9+5B2j/ldl0Do=',1,1,1,'2013-03-07 22:44:48','2013-03-07 22:31:17'),(2,'jason','','','mjhu@mit.edu','pbkdf2_sha256$10000$TjEutm6FtUKU$rlYMdRt8YxV4i3/yFrqThcVStjLSEQe/CBWb53HNt+U=',1,1,1,'2013-03-08 00:57:28','2013-03-07 22:34:48'),(3,'swgreen','','','swgreen@mit.edu','pbkdf2_sha256$10000$wqofx0SZQZTU$y1pgS8UanAJdQsyForHK+LJ6Cw3cG7BwYcoV3w096W0=',1,1,1,'2013-03-07 23:19:22','2013-03-07 22:43:41');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_e90f3816` (`user_id`),
  KEY `auth_user_groups_8b07cf5` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_e90f3816` (`user_id`),
  KEY `auth_user_user_permissions_6f299768` (`permission_id`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
INSERT INTO `auth_user_user_permissions` VALUES (1,1,43),(2,1,46),(3,1,49),(4,1,44),(5,1,47),(6,1,50),(7,1,45),(8,1,48),(9,1,51),(10,2,43),(11,2,46),(12,2,49),(13,2,44),(14,2,47),(15,2,50),(16,2,45),(17,2,48),(18,2,51),(19,3,43),(20,3,46),(21,3,49),(22,3,44),(23,3,47),(24,3,50),(25,3,45),(26,3,48),(27,3,51);
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_e90f3816` (`user_id`),
  KEY `django_admin_log_7e19a021` (`content_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'log entry','admin','logentry'),(8,'version','django_evolution','version'),(9,'evolution','django_evolution','evolution'),(10,'registration profile','registration','registrationprofile'),(11,'api access','tastypie','apiaccess'),(12,'api key','tastypie','apikey'),(13,'user profile','accounts','userprofile'),(14,'filter list item','api','filterlistitem'),(15,'white list item','api','whitelistitem'),(16,'black list item','api','blacklistitem'),(17,'eye history','api','eyehistory');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_evolution`
--

DROP TABLE IF EXISTS `django_evolution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_evolution` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `version_id` int(11) NOT NULL,
  `app_label` varchar(200) NOT NULL,
  `label` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_evolution_61faafd2` (`version_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_evolution`
--

LOCK TABLES `django_evolution` WRITE;
/*!40000 ALTER TABLE `django_evolution` DISABLE KEYS */;
INSERT INTO `django_evolution` VALUES (1,1,'auth','auth_delete_message'),(2,1,'sessions','session_expire_date_db_index');
/*!40000 ALTER TABLE `django_evolution` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_project_version`
--

DROP TABLE IF EXISTS `django_project_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_project_version` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `signature` longtext NOT NULL,
  `when` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_project_version`
--

LOCK TABLES `django_project_version` WRITE;
/*!40000 ALTER TABLE `django_project_version` DISABLE KEYS */;
INSERT INTO `django_project_version` VALUES (1,'(dp1\nS\'sessions\'\np2\nccopy_reg\n_reconstructor\np3\n(cdjango.utils.datastructures\nSortedDict\np4\nc__builtin__\ndict\np5\n(dp6\nS\'Session\'\np7\n(dp8\nS\'meta\'\np9\n(dp10\nS\'db_table\'\np11\nS\'django_session\'\np12\nsS\'pk_column\'\np13\nS\'session_key\'\np14\nsS\'unique_together\'\np15\n(lp16\nsS\'db_tablespace\'\np17\nS\'\'\nssS\'fields\'\np18\n(dp19\nS\'session_data\'\np20\n(dp21\nS\'field_type\'\np22\ncdjango.db.models.fields\nTextField\np23\nssg14\n(dp24\nS\'max_length\'\np25\nI40\nsS\'primary_key\'\np26\nI01\nsg22\ncdjango.db.models.fields\nCharField\np27\nssS\'expire_date\'\np28\n(dp29\nS\'db_index\'\np30\nI01\nsg22\ncdjango.db.models.fields\nDateTimeField\np31\nsssstRp32\n(dp33\nS\'keyOrder\'\np34\n(lp35\ng7\nasbsS\'registration\'\np36\ng3\n(g4\ng5\n(dp37\nS\'RegistrationProfile\'\np38\n(dp39\ng9\n(dp40\ng11\nS\'registration_registrationprofile\'\np41\nsg13\nS\'id\'\np42\nsg15\n(lp43\nsg17\nS\'\'\nssg18\n(dp44\nS\'activation_key\'\np45\n(dp46\ng25\nI40\nsg22\ng27\nssS\'user\'\np47\n(dp48\nS\'unique\'\np49\nI01\nsS\'related_model\'\np50\nS\'auth.User\'\np51\nsg22\ncdjango.db.models.fields.related\nForeignKey\np52\nssg42\n(dp53\ng26\nI01\nsg22\ncdjango.db.models.fields\nAutoField\np54\nsssstRp55\n(dp56\ng34\n(lp57\ng38\nasbsS\'accounts\'\np58\ng3\n(g4\ng5\n(dp59\nS\'UserProfile\'\np60\n(dp61\ng9\n(dp62\ng11\nS\'accounts_userprofile\'\np63\nsg13\ng42\nsg15\n(lp64\nsg17\nS\'\'\nssg18\n(dp65\nS\'use_tour\'\np66\n(dp67\ng22\ncdjango.db.models.fields\nBooleanField\np68\nssg47\n(dp69\ng49\nI01\nsg50\nS\'auth.User\'\np70\nsg22\ncdjango.db.models.fields.related\nOneToOneField\np71\nssS\'follows\'\np72\n(dp73\ng50\nS\'accounts.UserProfile\'\np74\nsg22\ncdjango.db.models.fields.related\nManyToManyField\np75\nssS\'anon_email\'\np76\n(dp77\ng22\ng68\nssS\'pic_url\'\np78\n(dp79\ng25\nI1000\nsg22\ng27\nssg42\n(dp80\ng26\nI01\nsg22\ng54\nssg45\n(dp81\ng25\nI40\nsg22\ng27\nsssstRp82\n(dp83\ng34\n(lp84\ng60\nasbsS\'common\'\np85\ng3\n(g4\ng5\n(dtRp86\n(dp87\ng34\n(lp88\nsbsS\'compressor\'\np89\ng3\n(g4\ng5\n(dtRp90\n(dp91\ng34\n(lp92\nsbsS\'messages\'\np93\ng3\n(g4\ng5\n(dtRp94\n(dp95\ng34\n(lp96\nsbsS\'humanize\'\np97\ng3\n(g4\ng5\n(dtRp98\n(dp99\ng34\n(lp100\nsbsS\'staticfiles\'\np101\ng3\n(g4\ng5\n(dtRp102\n(dp103\ng34\n(lp104\nsbsS\'pagination\'\np105\ng3\n(g4\ng5\n(dtRp106\n(dp107\ng34\n(lp108\nsbsS\'api\'\np109\ng3\n(g4\ng5\n(dp110\nS\'EyeHistory\'\np111\n(dp112\ng9\n(dp113\ng11\nS\'api_eyehistory\'\np114\nsg13\ng42\nsg15\n(lp115\nsg17\nS\'\'\nssg18\n(dp116\ng47\n(dp117\ng50\nS\'auth.User\'\np118\nsg22\ng52\nssS\'total_time\'\np119\n(dp120\ng22\ncdjango.db.models.fields\nIntegerField\np121\nssg42\n(dp122\ng26\nI01\nsg22\ng54\nssS\'start_event\'\np123\n(dp124\ng25\nI40\nsg22\ng27\nssS\'title\'\np125\n(dp126\ng25\nI40\nsg22\ng27\nssS\'src\'\np127\n(dp128\ng25\nI40\nsg22\ng27\nssS\'start_time\'\np129\n(dp130\ng22\ng31\nssS\'favIconUrl\'\np131\n(dp132\ng25\nI2000\nsg22\ncdjango.db.models.fields\nURLField\np133\nssS\'humanize_time\'\np134\n(dp135\ng25\nI200\nsg22\ng27\nssS\'url\'\np136\n(dp137\ng25\nI2000\nsg22\ng133\nssS\'end_event\'\np138\n(dp139\ng25\nI40\nsg22\ng27\nssS\'end_time\'\np140\n(dp141\ng22\ng31\nssssS\'WhiteListItem\'\np142\n(dp143\ng9\n(dp144\ng11\nS\'api_whitelistitem\'\np145\nsg13\nS\'filterlistitem_ptr_id\'\np146\nsg15\n(lp147\nsg17\nS\'\'\nssg18\n(dp148\nS\'type\'\np149\n(dp150\ng25\nI40\nsg22\ng27\nssS\'filterlistitem_ptr\'\np151\n(dp152\ng49\nI01\nsg50\nS\'api.FilterListItem\'\np153\nsg26\nI01\nsg22\ng71\nssssS\'BlackListItem\'\np154\n(dp155\ng9\n(dp156\ng11\nS\'api_blacklistitem\'\np157\nsg13\nS\'filterlistitem_ptr_id\'\np158\nsg15\n(lp159\nsg17\nS\'\'\nssg18\n(dp160\ng149\n(dp161\ng25\nI40\nsg22\ng27\nssS\'filterlistitem_ptr\'\np162\n(dp163\ng49\nI01\nsg50\nS\'api.FilterListItem\'\np164\nsg26\nI01\nsg22\ng71\nssssS\'FilterListItem\'\np165\n(dp166\ng9\n(dp167\ng11\nS\'api_filterlistitem\'\np168\nsg13\ng42\nsg15\n(lp169\nsg17\nS\'\'\nssg18\n(dp170\ng136\n(dp171\ng25\nI2000\nsg22\ng133\nssg47\n(dp172\ng50\nS\'auth.User\'\np173\nsg22\ng52\nssS\'date_created\'\np174\n(dp175\ng22\ng31\nssg42\n(dp176\ng26\nI01\nsg22\ng54\nsssstRp177\n(dp178\ng34\n(lp179\ng165\nag142\nag154\nag111\nasbsS\'admin\'\np180\ng3\n(g4\ng5\n(dp181\nS\'LogEntry\'\np182\n(dp183\ng9\n(dp184\ng11\nS\'django_admin_log\'\np185\nsg13\ng42\nsg15\n(lp186\nsg17\nS\'\'\nssg18\n(dp187\nS\'content_type\'\np188\n(dp189\nS\'null\'\np190\nI01\nsg50\nS\'contenttypes.ContentType\'\np191\nsg22\ng52\nssg47\n(dp192\ng50\nS\'auth.User\'\np193\nsg22\ng52\nssS\'action_flag\'\np194\n(dp195\ng22\ncdjango.db.models.fields\nPositiveSmallIntegerField\np196\nssS\'object_id\'\np197\n(dp198\ng190\nI01\nsg22\ng23\nssS\'action_time\'\np199\n(dp200\ng22\ng31\nssS\'change_message\'\np201\n(dp202\ng22\ng23\nssg42\n(dp203\ng26\nI01\nsg22\ng54\nssS\'object_repr\'\np204\n(dp205\ng25\nI200\nsg22\ng27\nsssstRp206\n(dp207\ng34\n(lp208\ng182\nasbsS\'sites\'\np209\ng3\n(g4\ng5\n(dp210\nS\'Site\'\np211\n(dp212\ng9\n(dp213\ng11\nS\'django_site\'\np214\nsg13\ng42\nsg15\n(lp215\nsg17\nS\'\'\nssg18\n(dp216\nS\'name\'\np217\n(dp218\ng25\nI50\nsg22\ng27\nssS\'domain\'\np219\n(dp220\ng25\nI100\nsg22\ng27\nssg42\n(dp221\ng26\nI01\nsg22\ng54\nsssstRp222\n(dp223\ng34\n(lp224\ng211\nasbsS\'admindocs\'\np225\ng3\n(g4\ng5\n(dtRp226\n(dp227\ng34\n(lp228\nsbsS\'live_stream\'\np229\ng3\n(g4\ng5\n(dtRp230\n(dp231\ng34\n(lp232\nsbsS\'auth\'\np233\ng3\n(g4\ng5\n(dp234\nS\'Permission\'\np235\n(dp236\ng9\n(dp237\ng11\nS\'auth_permission\'\np238\nsg13\ng42\nsg15\n((S\'content_type\'\nS\'codename\'\nttp239\nsg17\nS\'\'\nssg18\n(dp240\ng188\n(dp241\ng50\nS\'contenttypes.ContentType\'\np242\nsg22\ng52\nssg217\n(dp243\ng25\nI50\nsg22\ng27\nssS\'codename\'\np244\n(dp245\ng25\nI100\nsg22\ng27\nssg42\n(dp246\ng26\nI01\nsg22\ng54\nssssS\'User\'\np247\n(dp248\ng9\n(dp249\ng11\nS\'auth_user\'\np250\nsg13\ng42\nsg15\n(lp251\nsg17\nS\'\'\nssg18\n(dp252\nS\'is_superuser\'\np253\n(dp254\ng22\ng68\nssS\'first_name\'\np255\n(dp256\ng25\nI30\nsg22\ng27\nssS\'username\'\np257\n(dp258\ng49\nI01\nsg25\nI30\nsg22\ng27\nssS\'email\'\np259\n(dp260\ng25\nI75\nsg22\ncdjango.db.models.fields\nEmailField\np261\nssS\'is_active\'\np262\n(dp263\ng22\ng68\nssS\'last_name\'\np264\n(dp265\ng25\nI30\nsg22\ng27\nssS\'user_permissions\'\np266\n(dp267\ng50\nS\'auth.Permission\'\np268\nsg22\ng75\nssS\'is_staff\'\np269\n(dp270\ng22\ng68\nssS\'groups\'\np271\n(dp272\ng50\nS\'auth.Group\'\np273\nsg22\ng75\nssS\'date_joined\'\np274\n(dp275\ng22\ng31\nssg42\n(dp276\ng26\nI01\nsg22\ng54\nssS\'last_login\'\np277\n(dp278\ng22\ng31\nssS\'password\'\np279\n(dp280\ng25\nI128\nsg22\ng27\nssssS\'Group\'\np281\n(dp282\ng9\n(dp283\ng11\nS\'auth_group\'\np284\nsg13\ng42\nsg15\n(lp285\nsg17\nS\'\'\nssg18\n(dp286\ng217\n(dp287\ng49\nI01\nsg25\nI80\nsg22\ng27\nssS\'permissions\'\np288\n(dp289\ng50\nS\'auth.Permission\'\np290\nsg22\ng75\nssg42\n(dp291\ng26\nI01\nsg22\ng54\nsssstRp292\n(dp293\ng34\n(lp294\ng235\nag281\nag247\nasbsS\'__version__\'\np295\nI1\nsS\'django_evolution\'\np296\ng3\n(g4\ng5\n(dp297\nS\'Version\'\np298\n(dp299\ng9\n(dp300\ng11\nS\'django_project_version\'\np301\nsg13\ng42\nsg15\n(lp302\nsg17\nS\'\'\nssg18\n(dp303\nS\'signature\'\np304\n(dp305\ng22\ng23\nssg42\n(dp306\ng26\nI01\nsg22\ng54\nssS\'when\'\np307\n(dp308\ng22\ng31\nssssS\'Evolution\'\np309\n(dp310\ng9\n(dp311\ng11\nS\'django_evolution\'\np312\nsg13\ng42\nsg15\n(lp313\nsg17\nS\'\'\nssg18\n(dp314\nS\'label\'\np315\n(dp316\ng25\nI100\nsg22\ng27\nssS\'app_label\'\np317\n(dp318\ng25\nI200\nsg22\ng27\nssS\'version\'\np319\n(dp320\ng50\nS\'django_evolution.Version\'\np321\nsg22\ng52\nssg42\n(dp322\ng26\nI01\nsg22\ng54\nsssstRp323\n(dp324\ng34\n(lp325\ng298\nag309\nasbsS\'extension\'\np326\ng3\n(g4\ng5\n(dtRp327\n(dp328\ng34\n(lp329\nsbsS\'tastypie\'\np330\ng3\n(g4\ng5\n(dp331\nS\'ApiKey\'\np332\n(dp333\ng9\n(dp334\ng11\nS\'tastypie_apikey\'\np335\nsg13\ng42\nsg15\n(lp336\nsg17\nS\'\'\nssg18\n(dp337\ng47\n(dp338\ng49\nI01\nsg50\nS\'auth.User\'\np339\nsg22\ng71\nssS\'key\'\np340\n(dp341\ng25\nI256\nsg22\ng27\nssS\'created\'\np342\n(dp343\ng22\ng31\nssg42\n(dp344\ng26\nI01\nsg22\ng54\nssssS\'ApiAccess\'\np345\n(dp346\ng9\n(dp347\ng11\nS\'tastypie_apiaccess\'\np348\nsg13\ng42\nsg15\n(lp349\nsg17\nS\'\'\nssg18\n(dp350\ng136\n(dp351\ng25\nI255\nsg22\ng27\nssS\'request_method\'\np352\n(dp353\ng25\nI10\nsg22\ng27\nssS\'identifier\'\np354\n(dp355\ng25\nI255\nsg22\ng27\nssS\'accessed\'\np356\n(dp357\ng22\ncdjango.db.models.fields\nPositiveIntegerField\np358\nssg42\n(dp359\ng26\nI01\nsg22\ng54\nsssstRp360\n(dp361\ng34\n(lp362\ng345\nag332\nasbsS\'contenttypes\'\np363\ng3\n(g4\ng5\n(dp364\nS\'ContentType\'\np365\n(dp366\ng9\n(dp367\ng11\nS\'django_content_type\'\np368\nsg13\ng42\nsg15\n((S\'app_label\'\nS\'model\'\nttp369\nsg17\nS\'\'\nssg18\n(dp370\ng217\n(dp371\ng25\nI100\nsg22\ng27\nssS\'model\'\np372\n(dp373\ng25\nI100\nsg22\ng27\nssg317\n(dp374\ng25\nI100\nsg22\ng27\nssg42\n(dp375\ng26\nI01\nsg22\ng54\nsssstRp376\n(dp377\ng34\n(lp378\ng365\nasbs.','2013-03-07 22:31:00');
/*!40000 ALTER TABLE `django_project_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_a7f39721` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('a09a17c8589cd9acfab4039819ad55c4','NTVjZmM3YjMxZGNiNzNlM2NmZGEyMzY1M2ZmNWQzNWY4YjBlZjAzZDqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWSKAQFVEl9hdXRoX3VzZXJfYmFja2VuZFUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxAnUu\n','2013-03-21 22:44:48'),('cdddf40c145d6c776098c27bf63e34eb','MTdlYTIyYTg2ZGM4MmRkN2I3MWJjMTYwOTRiMjI4ZGYzNzRkODJlOTqAAn1xAS4=\n','2013-03-22 00:57:19'),('3a5025dae3086f1c493f120ff78a61c2','ZTQ2NzcyNjliYmI5MDNlMGI1Yzk2N2Y1YzUwMzdjOWNmZWE4MmZlMzqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWSKAQNVEl9hdXRoX3VzZXJfYmFja2VuZFUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxAnUu\n','2013-03-21 23:19:22'),('8ab7eb6419941a778973d5ef57f5b58c','ZGI4ODBmOWVmMTM0YWU3ZTc2NGNiNjUzYjU3NGIwNjVjMTI2MGY1ODqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWRxAooBAlUSX2F1dGhfdXNlcl9iYWNrZW5kcQNVKWRqYW5nby5jb250cmliLmF1dGguYmFj\na2VuZHMuTW9kZWxCYWNrZW5kcQR1Lg==\n','2013-03-22 00:57:28');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration_registrationprofile`
--

DROP TABLE IF EXISTS `registration_registrationprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registration_registrationprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `activation_key` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration_registrationprofile`
--

LOCK TABLES `registration_registrationprofile` WRITE;
/*!40000 ALTER TABLE `registration_registrationprofile` DISABLE KEYS */;
INSERT INTO `registration_registrationprofile` VALUES (1,1,'ALREADY_ACTIVATED'),(2,2,'ALREADY_ACTIVATED'),(3,3,'ALREADY_ACTIVATED');
/*!40000 ALTER TABLE `registration_registrationprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tastypie_apiaccess`
--

DROP TABLE IF EXISTS `tastypie_apiaccess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tastypie_apiaccess` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `identifier` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `request_method` varchar(10) NOT NULL,
  `accessed` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tastypie_apiaccess`
--

LOCK TABLES `tastypie_apiaccess` WRITE;
/*!40000 ALTER TABLE `tastypie_apiaccess` DISABLE KEYS */;
/*!40000 ALTER TABLE `tastypie_apiaccess` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tastypie_apikey`
--

DROP TABLE IF EXISTS `tastypie_apikey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tastypie_apikey` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `key` varchar(256) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tastypie_apikey`
--

LOCK TABLES `tastypie_apikey` WRITE;
/*!40000 ALTER TABLE `tastypie_apikey` DISABLE KEYS */;
/*!40000 ALTER TABLE `tastypie_apikey` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-03-07 20:25:38
