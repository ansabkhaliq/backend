CREATE DATABASE  IF NOT EXISTS `squizz_app`;
USE `squizz_app`;

DROP TABLE IF EXISTS `Organizations`;
CREATE TABLE Organizations
(
  Id bigint auto_increment,
  OrganizationId VARCHAR(80) NOT NULL,
  APIOrganizationKey Text NOT NULL,
  APIOrganizationPassword VARCHAR(80) NOT NULL,
  AccountCode VARCHAR(60),
  PRIMARY KEY (Id),
  UNIQUE (OrganizationId)
);

DROP TABLE IF EXISTS `Categories`;
CREATE TABLE Categories
(
  Id bigint auto_increment,
  CategoryCode VARCHAR(80) NOT NULL,
  Description1 Text,
  Description2 Text,
  Description3 Text,
  Description4 Text,
  InternalId VARCHAR(80) NOT NULL,
  KeyCategoryId VARCHAR(80) NOT NULL,
  KeyCategoryParentId VARCHAR(80),
  MetaDescription VARCHAR(50),
  MetaKeywords VARCHAR(50),
  Name VARCHAR(60) NOT NULL,
  Ordering INT,
  PRIMARY KEY (Id)
);

DROP TABLE IF EXISTS `Orders`;
CREATE TABLE Orders
(
  Id bigint auto_increment,
  SupplierOrganizationId VARCHAR(80) NOT NULL,
  KeySupplierAccountId VARCHAR(80),
  CreatedOnDate DATE NOT NULL,
  Instructions Text,
  DeliveryOrganizationName VARCHAR(50),
  DeliveryContact VARCHAR(50),
  DeliveryEmail VARCHAR(100),
  DeliveryAddress1 VARCHAR(100),
  DeliveryAddress2 VARCHAR(100),
  DeliveryAddress3 VARCHAR(100),
  DeliveryRegionName VARCHAR(60),
  DeliveryCountryName VARCHAR(60),
  DeliveryPostCode VARCHAR(30),
  BillingContact VARCHAR(50),
  BillingEmail VARCHAR(100),
  BillingOrganizationName VARCHAR(50),
  BillingAddress1 VARCHAR(100),
  BillingAddress2 VARCHAR(100),
  BillingAddress3 VARCHAR(100),
  BillingRegionName VARCHAR(60),
  BillingCountryName VARCHAR(60),
  BillingPostCode VARCHAR(30),
  IsDropship ENUM('Y','N'),
  BillStatus VARCHAR(60) NOT NULL,
  OrganizationId bigint NOT NULL,
  PRIMARY KEY (Id),
  FOREIGN KEY (OrganizationId) REFERENCES Organizations(Id)
);

DROP TABLE IF EXISTS `Products`;
CREATE TABLE Products
(
  Id bigint auto_increment,
  KeyProductId VARCHAR(100) NOT NULL,
  Barcode VARCHAR(100) NOT NULL,
  BarcodeInner VARCHAR(100) NOT NULL,
  Description1 Text,
  Description2 Text,
  Description3 Text,
  Description4 Text,
  InternalId VARCHAR(80) NOT NULL,
  Brand TinyText,
  Height decimal(10,2),
  Depth decimal(10,2),
  Width decimal(10,2),
  Weight decimal(10,2),
  Volume decimal(10,2),
  ProductCondition TinyText,
  IsPriceTaxInclusive ENUM('Y','N') NOT NULL,
  IsKitted ENUM('Y','N') NOT NULL,
  KeyTaxcodeId VARCHAR(45) NOT NULL,
  StockQuantity decimal(10,2),
  ProductName Text NOT NULL,
  KitProductsSetPrice ENUM('Y','N'),
  ProductCode VARCHAR(45) NOT NULL,
  ProductSearchCode VARCHAR(50),
  StockLowQuantity decimal(10,2) NOT NULL,
  AverageCost decimal(10,2),
  ProductDrop VARCHAR(45),
  PackQuantity decimal(10,2),
  SupplierOrganizationId VARCHAR(80) NOT NULL,  
  PRIMARY KEY (Id),  
  UNIQUE (KeyProductId)
);

DROP TABLE IF EXISTS `SellUnits`;
CREATE TABLE SellUnits
(
  Id Bigint auto_increment,
  KeySellUnitId VARCHAR(50) NOT NULL,
  BaseQuantity FLOAT NOT NULL,
  IsBaseUnit CHAR(1) NOT NULL,
  IsPricedOffBaseUnit CHAR(1) NOT NULL,
  KeySellUnitParentId VARCHAR(50),
  SellUnitCode VARCHAR(10) NOT NULL,
  SellUnitLabel VARCHAR(10) NOT NULL,
  ProductId BigInt NOT NULL,
  PRIMARY KEY (Id),
  FOREIGN KEY (ProductId) REFERENCES Products(Id)
);


Drop Table If Exists `Images`;
CREATE TABLE Images
(
  Id bigint auto_increment,
  FileName VARCHAR(60),
  SmallImageLocation VARCHAR(250),
  MediumImageLocation VARCHAR(250),
  LargeImageLocation VARCHAR(250),
  3DModelLocation VARCHAR(250),
  Is3DModelType ENUM('Y','N') NOT NULL,
  ProductId BigInt NOT NULL,
  PRIMARY KEY (Id),
  FOREIGN KEY (ProductId) REFERENCES Products(Id)
);

Drop Table If Exists `Users`;
CREATE TABLE Users
(
  Id bigint auto_increment,
  Username VARCHAR(60) NOT NULL,
  Password VARCHAR(255) NOT NULL,
  OrganizationId BigInt NOT NULL,
  PRIMARY KEY (Id),
  FOREIGN KEY (OrganizationId) REFERENCES Organizations(Id)
);

Drop Table If Exists `Sessions`;
CREATE TABLE Sessions
(
  Id bigint auto_increment,
  SessionKey VARCHAR(100) NOT NULL,
  DateTime DATETime NOT NULL,
  UserId bigint NOT NULL,
  OrganizationId VARCHAR(80) NOT NULL,
  PRIMARY KEY (Id),
  FOREIGN KEY (UserId) REFERENCES Users(Id)
);

Drop Table If Exists `CategoryProducts`;
CREATE TABLE CategoryProducts
(
  Id bigint auto_increment,
  CategoryId BigInt NOT NULL,
  ProductId BigInt NOT NULL,
  PRIMARY KEY (Id),
  FOREIGN KEY (CategoryId) REFERENCES Categories(Id),
  FOREIGN KEY (ProductId) REFERENCES Products(Id)
);

Drop Table If Exists `OrderDetails`;
CREATE TABLE OrderDetails
(
  Id bigint auto_increment,
  KeyProductId VARCHAR(100) NOT NULL,
  ProductName tinytext,
  Quantity decimal(10,2) NOT NULL,
  UnitPrice decimal(10,2),
  TotalPrice decimal(10,2),
  TotalPriceIncTax decimal(10,2),
  TotalPriceExTax decimal(10,2),
  ProductCode VARCHAR(45),
  OrderId BigINT NOT NULL,
  ProductId BigINT NOT NULL,
  PRIMARY KEY (Id),
  FOREIGN KEY (OrderId) REFERENCES Orders(Id),
  FOREIGN KEY (ProductId) REFERENCES Products(Id)
);

Drop Table If Exists `Prices`;
CREATE TABLE Prices
(
  Id bigint auto_increment,
  KeyProductId VARCHAR(100) NOT NULL,
  KeySellUnitId VARCHAR(45) NOT NULL,
  Price decimal(10,2) NOT NULL,
  ReferenceId VARCHAR(45),
  ReferenceType VARCHAR(45),
  ProductId BigInt NOT NULL,
  PRIMARY KEY (Id),
  FOREIGN KEY (ProductId) REFERENCES Products(Id)
);

Drop Table If Exists `Addresses`;
CREATE TABLE Addresses
(
  Id bigint auto_increment,
  DeliveryContact VARCHAR(50),
  DeliveryOrgName VARCHAR(50),
  DeliveryEmail VARCHAR(100),
  DeliveryFax VARCHAR(50),
  DeliveryAddress1 VARCHAR(100),
  DeliveryAddress2 VARCHAR(100),
  DeliveryAddress3 VARCHAR(100),
  DeliveryPostcode VARCHAR(30),
  DeliveryRegionName VARCHAR(60),
  DeliveryCountryName VARCHAR(60),
  DeliveryCountryCodeISO2 VARCHAR(20),
  DeliveryCountryCodeISO3 VARCHAR(20),
  OrganizationId BigInt NOT NULL,
  PRIMARY KEY (Id),
  FOREIGN KEY (OrganizationId) REFERENCES Organizations(Id)
);
