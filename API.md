# API Document

## 1. Customer API

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

### 1.5 Switch Customer (To be Fixed)

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

### 1.6 List Address

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

## 3. Product API

## 4. Order API