# API Document

## 0. Pagination

The APIs having 'page' parameter support paging

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

### 1.4 Update Customer

- **Request**

  Send **PUT** to `/api/customer/<customer_id>`

  ```json
  // Example PUT /api/customer/11
  {
      "first_name": "Petra",
      "title": "Mrs"
  }
  ```

- **Response**

  ```json
  {
      "id": 11,
      "customer_code": "ALLUNEED",
      "title": "Mrs",
      "first_name": "Petra",
      "last_name": "S",
      "phone": "0123456789",
      "email": "233456@123.com",
      "nationality_code": "AUS",
      "organization_desc": "holySAS"
  }
  ```

  

### 1.5 Delete Customer

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

### 1.6 Switch Customer

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

### 1.7 List Addresses

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

### 1.8 Create Address

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

### 1.9 Update Address

- **Request**

  Send **PUT** to `/api/customer/<customer_id>/address/<address_id>`

  ```json
  // Example PUT /api/customer/11/address/22
  {
      "postcode": "QLD1111",
      "email": "petra2333@gmail.com"
  }
  ```

- **Response**

  ```json
  {
      "id": 22,
      "customer_id": 11,
      "contact": "9876541230",
      "organization": null,
      "email": "petra2333@gmail.com",
      "fax": null,
      "address_line1": "No.12",
      "address_line2": "Murry St, Xet, QLD",
      "address_line3": null,
      "postcode": "QLD1111",
      "region": "QLD",
      "country": "Australia"
  }
  ```

### 1.10 Delete Address

- **Request**

  Send **DELETE** to `/api/customer/<customer_id>/address/<address_id>`

  Example `/api/customer/14/address/39`

- **Response**

  ```json
  {
      "message": "Address 39 deleted"
  }
  ```

- **Status Code**

  - **200: OK**
  - **404: Customer or Address Not Found**

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

- **Request**

  Send **GET** to `/updateCategories`

- **Response**

  ```json
  {
      "message": "Category data Updated",
      "status": "Success"
  }
  ```

  

### 3.1 List Products

- **Request**

  Send **GET** to `/api/products`

  | Params | Description                           | Example   | Optional |
  | ------ | ------------------------------------- | --------- | -------- |
  | page   | Pagination, page size = 20            | page=1    | F        |
  | cate   | Retrieve product in specific category | cate=2079 | T        |
  |        |                                       |           |          |

- **Response**

  ```json
  {
      "items": [
          {
              "barcode": "9326243152575",
              "id": 372,
              "image": "https://attachments....",
              "name": "Book Sudoku 96pg A4",
              "price": 0.86,
              "productCode": "152575"
          },
          {
              "barcode": "9326243170319",
              "id": 566,
              "image": null,
              "name": "Book Sudoku 496pg A5",
              "price": 3.08,
              "productCode": "170319"
          },{
              ...
          }
      ],
      "page_items": 14,
      "page_num": 1,
      "total_items": 14,
      "total_pages": 1
  }
  ```

### 3.2 Get Product

