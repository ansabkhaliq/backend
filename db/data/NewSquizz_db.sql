CREATE DATABASE  IF NOT EXISTS `squizz_app` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `squizz_app`;
-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: squizz_app
-- ------------------------------------------------------
-- Server version	8.0.21

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
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `Id` bigint NOT NULL AUTO_INCREMENT,
  `CategoryCode` varchar(80) NOT NULL,
  `Description1` text,
  `Description2` text,
  `Description3` text,
  `Description4` text,
  `InternalId` varchar(80) NOT NULL,
  `KeyCategoryId` varchar(80) NOT NULL,
  `KeyCategoryParentId` varchar(80) DEFAULT NULL,
  `MetaDescription` varchar(50) DEFAULT NULL,
  `MetaKeywords` varchar(50) DEFAULT NULL,
  `Name` varchar(60) NOT NULL,
  `Ordering` int DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categoryproducts`
--

DROP TABLE IF EXISTS `categoryproducts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoryproducts` (
  `Id` bigint NOT NULL AUTO_INCREMENT,
  `CategoryId` bigint NOT NULL,
  `ProductId` bigint NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `CategoryId` (`CategoryId`),
  KEY `ProductId` (`ProductId`),
  CONSTRAINT `categoryproducts_ibfk_1` FOREIGN KEY (`CategoryId`) REFERENCES `categories` (`Id`),
  CONSTRAINT `categoryproducts_ibfk_2` FOREIGN KEY (`ProductId`) REFERENCES `products` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoryproducts`
--

LOCK TABLES `categoryproducts` WRITE;
/*!40000 ALTER TABLE `categoryproducts` DISABLE KEYS */;
/*!40000 ALTER TABLE `categoryproducts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `images`
--

DROP TABLE IF EXISTS `images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `images` (
  `Id` bigint NOT NULL AUTO_INCREMENT,
  `FileName` varchar(60) DEFAULT NULL,
  `SmallImageLocation` varchar(250) DEFAULT NULL,
  `MediumImageLocation` varchar(250) DEFAULT NULL,
  `LargeImageLocation` varchar(250) DEFAULT NULL,
  `3DModelLocation` varchar(250) DEFAULT NULL,
  `Is3DModelType` enum('Y','N') NOT NULL,
  `ProductId` bigint NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `ProductId` (`ProductId`),
  CONSTRAINT `images_ibfk_1` FOREIGN KEY (`ProductId`) REFERENCES `products` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `images`
--

LOCK TABLES `images` WRITE;
/*!40000 ALTER TABLE `images` DISABLE KEYS */;
/*!40000 ALTER TABLE `images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orderdetails`
--

DROP TABLE IF EXISTS `orderdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orderdetails` (
  `Id` bigint NOT NULL AUTO_INCREMENT,
  `KeyProductId` varchar(100) NOT NULL,
  `ProductName` tinytext,
  `Quantity` decimal(10,2) NOT NULL,
  `UnitPrice` decimal(10,2) DEFAULT NULL,
  `TotalPrice` decimal(10,2) DEFAULT NULL,
  `TotalPriceIncTax` decimal(10,2) DEFAULT NULL,
  `TotalPriceExTax` decimal(10,2) DEFAULT NULL,
  `ProductCode` varchar(45) DEFAULT NULL,
  `OrderId` bigint NOT NULL,
  `ProductId` bigint NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `OrderId` (`OrderId`),
  KEY `ProductId` (`ProductId`),
  CONSTRAINT `orderdetails_ibfk_1` FOREIGN KEY (`OrderId`) REFERENCES `orders` (`Id`),
  CONSTRAINT `orderdetails_ibfk_2` FOREIGN KEY (`ProductId`) REFERENCES `products` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderdetails`
--

LOCK TABLES `orderdetails` WRITE;
/*!40000 ALTER TABLE `orderdetails` DISABLE KEYS */;
/*!40000 ALTER TABLE `orderdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `Id` bigint NOT NULL AUTO_INCREMENT,
  `SupplierOrganizationId` varchar(80) NOT NULL,
  `KeySupplierAccountId` varchar(80) DEFAULT NULL,
  `CreatedOnDate` date NOT NULL,
  `Instructions` text,
  `DeliveryOrganizationName` varchar(50) DEFAULT NULL,
  `DeliveryContact` varchar(50) DEFAULT NULL,
  `DeliveryEmail` varchar(100) DEFAULT NULL,
  `DeliveryAddress1` varchar(100) DEFAULT NULL,
  `DeliveryAddress2` varchar(100) DEFAULT NULL,
  `DeliveryAddress3` varchar(100) DEFAULT NULL,
  `DeliveryRegionName` varchar(60) DEFAULT NULL,
  `DeliveryCountryName` varchar(60) DEFAULT NULL,
  `DeliveryPostCode` varchar(30) DEFAULT NULL,
  `BillingContact` varchar(50) DEFAULT NULL,
  `BillingEmail` varchar(100) DEFAULT NULL,
  `BillingOrganizationName` varchar(50) DEFAULT NULL,
  `BillingAddress1` varchar(100) DEFAULT NULL,
  `BillingAddress2` varchar(100) DEFAULT NULL,
  `BillingAddress3` varchar(100) DEFAULT NULL,
  `BillingRegionName` varchar(60) DEFAULT NULL,
  `BillingCountryName` varchar(60) DEFAULT NULL,
  `BillingPostCode` varchar(30) DEFAULT NULL,
  `IsDropship` enum('Y','N') DEFAULT NULL,
  `BillStatus` varchar(60) NOT NULL,
  `OrganizationId` bigint NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `OrganizationId` (`OrganizationId`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`OrganizationId`) REFERENCES `organizations` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organizations`
--

DROP TABLE IF EXISTS `organizations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organizations` (
  `Id` bigint NOT NULL AUTO_INCREMENT,
  `OrganizationId` varchar(80) NOT NULL,
  `APIOrganizationKey` text NOT NULL,
  `APIOrganizationPassword` varchar(80) NOT NULL,
  `AccountCode` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `OrganizationId` (`OrganizationId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organizations`
--

LOCK TABLES `organizations` WRITE;
/*!40000 ALTER TABLE `organizations` DISABLE KEYS */;
INSERT INTO `organizations` VALUES (1,'11EA64D91C6E8F70A23EB6800B5BCB6D','3a62ea5aa2d8845a72dd030369dd571d5123567f70fa76b5bc3bcdf103e3307cc52b01030230c4f2807b44f88ce0052e91f3b7550341f38fe6544d02abfd7d87','Squizzunimelb!0',NULL);
/*!40000 ALTER TABLE `organizations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prices`
--

DROP TABLE IF EXISTS `prices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prices` (
  `Id` bigint NOT NULL AUTO_INCREMENT,
  `KeyProductId` varchar(100) NOT NULL,
  `KeySellUnitId` varchar(45) NOT NULL,
  `Price` decimal(10,2) NOT NULL,
  `ReferenceId` varchar(45) DEFAULT NULL,
  `ReferenceType` varchar(45) DEFAULT NULL,
  `ProductId` bigint NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `ProductId` (`ProductId`),
  CONSTRAINT `prices_ibfk_1` FOREIGN KEY (`ProductId`) REFERENCES `products` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prices`
--

LOCK TABLES `prices` WRITE;
/*!40000 ALTER TABLE `prices` DISABLE KEYS */;
/*!40000 ALTER TABLE `prices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `Id` bigint NOT NULL AUTO_INCREMENT,
  `KeyProductId` varchar(100) NOT NULL,
  `Barcode` varchar(100) NOT NULL,
  `BarcodeInner` varchar(100) NOT NULL,
  `Description1` text,
  `Description2` text,
  `Description3` text,
  `Description4` text,
  `InternalId` varchar(80) NOT NULL,
  `Brand` tinytext,
  `Height` decimal(10,2) DEFAULT NULL,
  `Depth` decimal(10,2) DEFAULT NULL,
  `Width` decimal(10,2) DEFAULT NULL,
  `Weight` decimal(10,2) DEFAULT NULL,
  `Volume` decimal(10,2) DEFAULT NULL,
  `ProductCondition` tinytext,
  `IsPriceTaxInclusive` enum('Y','N') NOT NULL,
  `IsKitted` enum('Y','N') NOT NULL,
  `KeyTaxcodeId` varchar(45) NOT NULL,
  `StockQuantity` decimal(10,2) DEFAULT NULL,
  `ProductName` text NOT NULL,
  `KitProductsSetPrice` enum('Y','N') DEFAULT NULL,
  `ProductCode` varchar(45) NOT NULL,
  `ProductSearchCode` varchar(50) DEFAULT NULL,
  `StockLowQuantity` decimal(10,2) NOT NULL,
  `AverageCost` decimal(10,2) DEFAULT NULL,
  `ProductDrop` varchar(45) DEFAULT NULL,
  `PackQuantity` decimal(10,2) DEFAULT NULL,
  `SupplierOrganizationId` varchar(80) NOT NULL,
  `SellUnitId` bigint DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `KeyProductId` (`KeyProductId`),
  KEY `SellUnitId` (`SellUnitId`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`SellUnitId`) REFERENCES `sellunits` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sellunits`
--

DROP TABLE IF EXISTS `sellunits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sellunits` (
  `Id` bigint NOT NULL AUTO_INCREMENT,
  `KeySellUnitId` varchar(50) NOT NULL,
  `BaseQuantity` decimal(10,2) NOT NULL,
  `IsBaseUnit` enum('Y','N') NOT NULL,
  `IsPricedOffBaseUnit` enum('Y','N') NOT NULL,
  `KeySellUnitParentId` varchar(50) DEFAULT NULL,
  `SellUnitCode` varchar(10) NOT NULL,
  `SellUnitLabel` varchar(10) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sellunits`
--

LOCK TABLES `sellunits` WRITE;
/*!40000 ALTER TABLE `sellunits` DISABLE KEYS */;
/*!40000 ALTER TABLE `sellunits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sessions` (
  `Id` bigint NOT NULL AUTO_INCREMENT,
  `SessionKey` varchar(100) NOT NULL,
  `DateTime` datetime NOT NULL,
  `UserId` bigint NOT NULL,
  `OrganizationId` varchar(80) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `UserId` (`UserId`),
  CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `users` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `Id` bigint NOT NULL AUTO_INCREMENT,
  `Username` varchar(60) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `OrganizationId` bigint NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `OrganizationId` (`OrganizationId`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`OrganizationId`) REFERENCES `organizations` (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'user1','pbkdf2:sha256:150000$yIG2rYDn$6a2a2ea2679c6d4f697899b1daeed251db794a400b7574af4f1ef065530b5544',1),(2,'user2s','pbkdf2:sha256:150000$Bo1mhoFA$4c3cebd8696a885d5e02c813a1ef1d09e25b0d42ce2ba639cd781e485f7ef3e1',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-09-17 22:36:08
