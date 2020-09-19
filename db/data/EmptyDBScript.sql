CREATE DATABASE  IF NOT EXISTS `squizz_app`;
USE `squizz_app`;

DROP TABLE IF EXISTS `Organizations`;
CREATE TABLE Organizations
(
  id bigint auto_increment,
  organizationId VARCHAR(80) NOT NULL,
  apiOrganizationKey Text NOT NULL,
  apiOrganizationPassword VARCHAR(80) NOT NULL,
  accountCode VARCHAR(60),
  PRIMARY KEY (id),
  UNIQUE (organizationId)
);

DROP TABLE IF EXISTS `Categories`;
CREATE TABLE Categories
(
  id bigint auto_increment,
  categoryCode VARCHAR(80) NOT NULL,
  description1 Text,
  description2 Text,
  description3 Text,
  description4 Text,
  internalId VARCHAR(80) NOT NULL,
  keyCategoryId VARCHAR(80) NOT NULL,
  keyCategoryParentId VARCHAR(80),
  metaDescription VARCHAR(50),
  metaKeywords VARCHAR(50),
  categoryName VARCHAR(60) NOT NULL,
  ordering INT,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS `Orders`;
CREATE TABLE Orders
(
  id bigint auto_increment,
  supplierOrganizationId VARCHAR(80) NOT NULL,  
  createdOnDate datetime NOT NULL,
  instructions Text,
  deliveryOrganizationName VARCHAR(50),
  deliveryContact VARCHAR(50),
  deliveryEmail VARCHAR(100),
  deliveryAddress1 VARCHAR(100),
  deliveryAddress2 VARCHAR(100),
  deliveryAddress3 VARCHAR(100),
  deliveryRegionName VARCHAR(60),
  deliveryCountryName VARCHAR(60),
  deliveryPostCode VARCHAR(30),
  billingContact VARCHAR(50),
  billingEmail VARCHAR(100),
  billingOrganizationName VARCHAR(50),
  billingAddress1 VARCHAR(100),
  billingAddress2 VARCHAR(100),
  billingAddress3 VARCHAR(100),
  billingRegionName VARCHAR(60),
  billingCountryName VARCHAR(60),
  billingPostCode VARCHAR(30),
  isDropship ENUM('Y','N'),
  billStatus VARCHAR(60),
  organizationId bigint NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (organizationId) REFERENCES Organizations(id)
);

DROP TABLE IF EXISTS `Products`;
CREATE TABLE Products
(
  id bigint auto_increment,
  keyProductId VARCHAR(100) NOT NULL,
  barcode VARCHAR(100),
  barcodeInner VARCHAR(100),
  description1 Text,
  description2 Text,
  description3 Text,
  description4 Text,
  internalId VARCHAR(80) NOT NULL,
  brand TinyText,
  height decimal(10,2),
  depth decimal(10,2),
  width decimal(10,2),
  weight decimal(10,2),
  volume decimal(10,2),
  productCondition TinyText,
  isPriceTaxInclusive ENUM('Y','N') NOT NULL,
  isKitted ENUM('Y','N') NOT NULL,
  keyTaxcodeId VARCHAR(45) NOT NULL,
  stockQuantity decimal(10,2),
  productName Text,
  kitProductsSetPrice ENUM('Y','N'),
  productCode VARCHAR(45) NOT NULL,
  productSearchCode text,
  stockLowQuantity decimal(10,2) NOT NULL,
  averageCost decimal(10,2),
  productDrop VARCHAR(45),
  packQuantity decimal(10,2),
  supplierOrganizationId VARCHAR(80) NOT NULL,  
  keySellUnitID VARCHAR(50),
  PRIMARY KEY (id),  
  UNIQUE (keyProductId)
);

DROP TABLE IF EXISTS `SellUnits`;
CREATE TABLE SellUnits
(
  id Bigint auto_increment,
  keySellUnitId VARCHAR(50) NOT NULL,
  baseQuantity FLOAT NOT NULL,
  isBaseUnit ENUM ('Y', 'N') NOT NULL,
  isPricedOffBaseUnit ENUM ('Y', 'N') NOT NULL,
  keySellUnitParentId VARCHAR(50),
  sellUnitCode VARCHAR(10) NOT NULL,
  sellUnitLabel VARCHAR(10) NOT NULL,
  productId BigInt NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (productId) REFERENCES Products(id)
);


Drop Table If Exists `Images`;
CREATE TABLE Images
(
  id bigint auto_increment,
  fileName VARCHAR(60),
  smallImageLocation VARCHAR(250),
  mediumImageLocation VARCHAR(250),
  largeImageLocation VARCHAR(250),
  threeDModelLocation VARCHAR(250),
  is3DModelType ENUM('Y','N') NOT NULL,
  productId BigInt NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (productId) REFERENCES Products(id)
);

Drop Table If Exists `Users`;
CREATE TABLE Users
(
  id bigint auto_increment,
  username VARCHAR(60) NOT NULL,
  password VARCHAR(255) NOT NULL,
  organizationId BigInt NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (organizationId) REFERENCES Organizations(id)
);

Drop Table If Exists `Sessions`;
CREATE TABLE Sessions
(
  id bigint auto_increment,
  sessionKey VARCHAR(100) NOT NULL,
  dateTime DateTime NOT NULL,
  userId bigint NOT NULL,
  organizationId VARCHAR(80) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (userId) REFERENCES Users(id)
);

Drop Table If Exists `CategoryProducts`;
CREATE TABLE CategoryProducts
(
  id bigint auto_increment,
  categoryId BigInt NOT NULL,
  productId BigInt NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (categoryId) REFERENCES Categories(id),
  FOREIGN KEY (productId) REFERENCES Products(id)
);

Drop Table If Exists `OrderDetails`;
CREATE TABLE OrderDetails
(
  id bigint auto_increment,
  keyProductId VARCHAR(100) NOT NULL,
  productName tinytext,
  quantity decimal(10,2) NOT NULL,
  unitPrice decimal(10,2),
  totalPrice decimal(10,2),
  totalPriceIncTax decimal(10,2),
  totalPriceExTax decimal(10,2),
  productCode VARCHAR(45),
  orderId BigINT NOT NULL,
  productId BigINT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (orderId) REFERENCES Orders(id),
  FOREIGN KEY (productId) REFERENCES Products(id)
);

Drop Table If Exists `Prices`;
CREATE TABLE Prices
(
  id bigint auto_increment,
  keyProductId VARCHAR(100) NOT NULL,
  keySellUnitId VARCHAR(45) NOT NULL,
  price decimal(10,2) NOT NULL,
  referenceId VARCHAR(45),
  referenceType VARCHAR(45),
  productId BigInt NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (productId) REFERENCES Products(id)
);

Drop Table If Exists `Addresses`;
CREATE TABLE Addresses
(
  id bigint auto_increment,
  deliveryContact VARCHAR(50),
  deliveryOrgName VARCHAR(50),
  deliveryEmail VARCHAR(100),
  deliveryFax VARCHAR(50),
  deliveryAddress1 VARCHAR(100),
  deliveryAddress2 VARCHAR(100),
  deliveryAddress3 VARCHAR(100),
  deliveryPostcode VARCHAR(30),
  deliveryRegionName VARCHAR(60),
  deliveryCountryName VARCHAR(60),
  deliveryCountryCodeISO2 VARCHAR(20),
  deliveryCountryCodeISO3 VARCHAR(20),
  organizationId BigInt NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (organizationId) REFERENCES Organizations(id)
);
