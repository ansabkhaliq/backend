# API Document

## 0. Pagination

The APIs having 'page' parameter support paging, in all those APIs, page is an optional parameter. If

-  **200 Response**

  ```json
  {
      "total_pages": 11,
      "total_items": 210,
      "page_num": 10,
      "page_items": 20,
      "items": [
          "item goes here"
      ]
  }
  ```

  > ***page_num*** *stands for the current page, **page_items** stands for the number of items in current page.*

- **404 Response**

  ```json
  {
      "message": "Page number out of bounds for listing XXXX",
      "total_pages": 11
  }
  ```

  > ***XXXX*** *is model name*

## 1. Customer API

### 1.0 List Customer Codes

- **Request**

  Send **GET** to `/api/customer_codes`

  | Params | Description                                 | Example | Optional |
  | ------ | ------------------------------------------- | ------- | -------- |
  | used   | To get used (1) or unused (0) customer code | used=1  | T        |
  |        |                                             |         |          |

  > *Return all codes if 'used' is not set.*

- **Response**

  ```json
  ["TESTDEBTOR", "ALLUNEED", ...]
  ```

- **Status Code**

  - **200: OK**

### 1.1 List Customers

- **Request** 

  Send **GET** to `/api/customers`

- **Response**

  ```JSON
  [
      {
          "id": 1,
          "customer_code": "TESTDEBTOR",
          "title": "Miss",
          "first_name": "Junlu",
          "last_name": "zzzzzzzz",
          "phone": "0987654321",
          "email": "aaa@bbb.xyz",
          "nationality_code": "CN",
          "organization_desc": "HolySAS"
      }, {
          ...
      }
  ]
  ```

- **Status Code**

  - **200: OK**

### 1.2 Create Customer

- **Request** 

  - Send **POST** to `/api/customers`

  ```json
  // address is optional
  {
      "customer": {
          "customer_code": "TESTDEBTOR",
          "title": "Mr",
          "first_name": "Eric",
          "last_name": "Z",
          "phone": "0123456789",
          "email": "xxzz@xxx.xyz",
          "nationality_code": "CN",
          "organization_desc": "HolySAS",
      },
      "address": {
          "contact": "9876543210",
          "address_line1": "xxxx",
          "address_line2": "yyyy",
          "postcode": "VIC3000",
          "region": "",
          "country": ""
      }
  }
  ```

- **Response**

  ```json
  {
      "customer": {
          "customer_obj"
      },
      "address": {
          "address_obj"
      }
  }
  ```

- **Status code**

  - **201: Create successfully**
  - **404: Customer code not found**
  - **409: Customer code already used**
  - **400: Bad request eg. Lack of necessary data**

### 1.3 Get Customer

- **Request**

  Send **GET** to `/api/customer/<customer_id>`

- **Response**

  ```json
  {
  	"customer_code": "TESTDEBTOR",
  	"title": "Mr",
  	"first_name": "Eric",
  	"last_name": "Z",
  	"phone": "0123456789",
  	"email": "xxzz@xxx.xyz",
  	"nationality_code": "CN",
  	"organization_desc": "HolySAS",
  }
  ```

- **Status Code**

  - **200: OK**
  - **404: Customer Not Found**

### 1.4 Delete Customer

- **Request**

  Send **DELETE** to `/api/customer/<customer_id>`

- **Response**

  ```json
  {
  	"message": "Customer XX deleted."
  }
  ```

- **Status Code**

  - **200: OK**
  - **404: Customer Not Found**

### 1.5 Switch Customer

- POST current customer **(Slow API approx 10 seconds)**

  - **POST** /api/switch_customer

  - **Request**

    ```json
    { "customer_code": "ALLUNEED" }
    ```

  - **Response**

    ```json
    {"message": "Switch to XXXXX successful"}
    ```

  - **Status Code**

    - **200: OK**
    - **404: Customer Code does not exist or match any customers**
    - **400: Bad request lack of customer_code**

### 1.6 List Addresses

- **Request**

  Send **GET** to `/api/customer/<customer_id>/addresses`

- **Response**

  ```json
  [
      {
          "id": 1,
          "customer_id": 1,
          "contact": "9876543210",
          "address_line1": "xxxx",
          "address_line2": "yyyy",
          "address_line3": "",
          "postcode": "VIC3000",
          "fax": "",
          "email": "",
          "region": "",
          "country": ""
      }, {
          ...
      }
  ]
  ```

- **Status Code**

  - **200: OK**
  - **404: Customer Not Found**

### 1.7 Create Address

- **Request**

  Send **POST** t0 `/api/customer/<customer_id>/addresses`

  ```json
  {
  	"contact": "9876543210",
  	"address_line1": "xxxx",
  	"address_line2": "yyyy",
  	"postcode": "VIC3000",
  	"region": "Victoria",
  	"country": "AUS"
  }
  ```

- **Response**

  ```json
  {
      "id": 19,
      "customer_id": 19,
      "contact": "9876543210",
      "address_line1": "xxxx",
      "address_line2": "yyyy",
      "address_line4": "",
      "postcode": "VIC3000",
      "region": "Victoria",
      "country": "AUS",
      "email": "",
      "fax": ""
  }
  ```

- **Status Code**

  - **201: Create Address for customer successful**
  - **404: Customer Not Found**



## 2. Category API

### 2.1 List Categories

- **Request**

  Send **GET** to `/api/categories`

- **Response**

  ```json
  [
      {
          "categoryCode": "Baby",
          "description1": null,
          "description2": null,
          "description3": null,
          "description4": null,
          "id": 2036,
          "internalID": "11EAF256D8E35DB2A1626AF3476460FC",
          "keyCategoryID": "Baby",
          "keyCategoryParentID": null,
          "keyProductIDs": null,
          "metaDescription": null,
          "metaKeywords": null,
          "name": "Baby",
          "ordering": 2,
          "Children": [
              {
                  "categoryCode": "Accessories-Baby",
                  "description1": null,
                  "description2": null,
                  "description3": null,
                  "description4": null,
                  "id": 2028,
                  "internalID": "11EAF256D8E384D4A1626AF3476460FC",
                  "keyCategoryID": "Accessories-Baby",
                  "keyCategoryParentID": "Baby",
                  "keyProductIDs": null,
                  "metaDescription": null,
                  "metaKeywords": null,
                  "name": "Accessories",
                  "ordering": 6
              }
          ]
      }
  ]
  ```

- **Status Code**

  - **200: OK**

## 3. Product API

### 3.0 Sync Data from Squizz

#### Sync Categories

### 3.1 List Products

- **Request**

  Send **GET** to `/api/products`

  | Params | Description                           | Example   | Optional |
  | ------ | ------------------------------------- | --------- | -------- |
  | page   | Pagination, page size = 20            | page=1    | T        |
  | cate   | Retrieve product in specific category | cate=2079 | T        |
  |        |                                       |           |          |

- **Response**

  ```json
  [
      {
          "averageCost": null,
          "barcode": "9326243178476",
          "barcodeInner": "5040.000000",
          "brand": null,
          "categoryList": null,
          "depth": 0.0,
          "description1": "Bandage Self Adhesive",
          "description2": "29-12-2020",
          "description3": null,
          "description4": null,
          "drop": null,
          "height": 12.0,
          "id": 749,
          "imageList": null,
          "internalID": "11EAF25670585D9DA1626AF3476460FC",
          "isKitted": "N",
          "isPriceTaxInclusive": "N",
          "keyProductID": "21479232456673",
          "keySellUnitID": "1",
          "keyTaxcodeID": "34333235303332303734313136",
          "kitProductsSetPrice": "N",
          "name": "Bandage Self Adhesive",
          "packQuantity": null,
          "priceList": null,
          "productCode": "178476",
          "productCondition": null,
          "productSearchCode": "Bandage-Self-Adhesive-21479232456673",
          "sellUnits": null,
          "sellUnitsIdList": null,
          "stockLowQuantity": 144.0,
          "stockQuantity": 4124.0,
          "supplierOrganizationId": "11EAF2251136B090BB69B6800B5BCB6D",
          "volume": 0.0,
          "weight": 0.0,
          "width": 144.0
      },
  ]
  ```

### 3.2 Get Product

