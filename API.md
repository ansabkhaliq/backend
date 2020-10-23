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

### 3.1 Retrieve product by product barcode

- **Request** 
    - Send **GET** to `/api/barcode`
    - Take **barcode** as parameter e.g. `/api/barcode?barcode=933044000895`

- **Response**

  ```JSON
  {
    "data": {
        "averageCost": null,
        "barcode": "933044000895",
        "barcodeInner": null,
        "brand": null,
        "categoryList": null,
        "depth": 0,
        "description1": null,
        "description2": null,
        "description3": null,
        "description4": null,
        "drop": null,
        "height": 0,
        "id": 1,
        "imageList": null,
        "internalID": null,
        "isKitted": null,
        "isPriceTaxInclusive": null,
        "keyProductID": "21479231976900",
        "keySellUnitID": null,
        "keyTaxcodeID": null,
        "kitProductsSetPrice": null,
        "name": null,
        "packQuantity": null,
        "priceList": null,
        "productCode": "00089",
        "productCondition": null,
        "productSearchCode": null,
        "sellUnits": null,
        "sellUnitsIdList": null,
        "stockLowQuantity": 0,
        "stockQuantity": 0,
        "supplierOrganizationId": null,
        "volume": 0,
        "weight": 0,
        "width": 0
    },
    "Message": "successfully retrieved product",
    "status": "success"
  }
  ```

### 3.2 Retrieve product by product code

- **Request** 

   - Send **GET** to `/api/product`
   - Take **productCode** as parameter e.g. `/api/barcode?productCode=CFP-600-20`

- **Response**
    ```JSON
  {
    "data": {
        "averageCost": null,
        "barcode": "933044000895",
        "barcodeInner": null,
        "brand": null,
        "categoryList": null,
        "depth": 0,
        "description1": null,
        "description2": null,
        "description3": null,
        "description4": null,
        "drop": null,
        "height": 0,
        "id": 1,
        "imageList": null,
        "internalID": null,
        "isKitted": null,
        "isPriceTaxInclusive": null,
        "keyProductID": "21479231976900",
        "keySellUnitID": null,
        "keyTaxcodeID": null,
        "kitProductsSetPrice": null,
        "name": null,
        "packQuantity": null,
        "priceList": null,
        "productCode": "00089",
        "productCondition": null,
        "productSearchCode": null,
        "sellUnits": null,
        "sellUnitsIdList": null,
        "stockLowQuantity": 0,
        "stockQuantity": 0,
        "supplierOrganizationId": null,
        "volume": 0,
        "weight": 0,
        "width": 0
    },
    "Message": "successfully retrieved product",
    "status": "success"
  }
  ```

  ### 3.3 Retrieve product metadata by product code

- **Request** 

    - Send **GET** to `/api/metadata/get`
    - Take **productCode** as parameter e.g. `/api/metadata/get?productCode=CFP-600-12`

- **Response**
    ```JSON
    {
    "found": true,
    "json_data": {
        "Diffuser Width (Length Millimeters)": "595.000000000000",
        "Flow Nom (Hvac Air Flow Liters Per Second)": "112.500000000000",
        "Holyoake Product Range": "Holyoake Swirl Diffusers.",
        "Inlet Spigot Diameter (Length Millimeters)": "250.000000000000",
        "Manufacturer": "Holyoake",
       ...
    }
}
    ```
    
### 3.4 Retrieve product from squizz api
  **This is not a api that front end can assess.  These are supposed to be called by the Postman or another similar tool thatallow you to make calls to the REST API.**
   **This method is repsonbile for getting the latest products from SQUIZZ platform and updating the table in the local database**
- **Request** 
    - Before retrieve data from squizz api, you should log in first 
    - Send **GET** to `/retrieveProduct`
  
- **Response**  
  ```JSON
  {
    "data": {
        "failed": []
    },
    "message": "successfully stored products",
    "status": "success"
  }
  ```
  ### 3.5 Retrieve product price from squizz api
  **This is not a api that front end can access.  These are supposed to be called by the Postman or another similar tool thatallow you to make calls to the REST API.**
  **This method is repsonbile for getting the latest price from SQUIZZ platform and updating the table in the local database**
- **Request** 
    Before retrieve data from squizz api, you should log in first 
    Send **GET** to `/retrievePrices`
   
- **Response**  
  ```JSON
  {
    "data": {
        "failed": []
    },
    "message": "successfully stored product prices",
    "status": "success"
  }
  ```
  ### 3.6 Update product from squizz api
  **This is not a api that front end can access.  These are supposed to be called by the Postman or another similar tool thatallow you to make calls to the REST API.**
  **This method is repsonbile for getting the latest products from SQUIZZ platform and updating the table in the local database**
- **Request** 
   - Before retrieve data from squizz api, you should log in first 
   - Send **GET** to `/updateProducts`
   
- **Response**  
  ```JSON
   {
    "data": {
        "failed": []
    },
    "message": "successfully updated products",
    "status": "success"
  }
  ```
  ### 3.7 Update product price from squizz api
  **This is not a api that front end can access.  These are supposed to be called by the Postman or another similar tool thatallow you to make calls to the REST API.**
  **This method is repsonbile for getting the latest products from SQUIZZ platform and updating the table in the local database**
- **Request** 
    Before retrieve data from squizz api, you should log in first 
    Send **GET** to `/updateProducts`
   
- **Response**  
  ```JSON
  {
    "data": {
        "failed": []
    },
    "message": "successfully stored product prices",
    "status": "success"
  }
  ```
  ### 3.8 import metadata
  **This is not a api that front end can access.  These are supposed to be called by the Postman or another similar tool that allow you to make calls to the REST API.**
  **This method is repsonbile for getting the latest  3d model's metadata**
- **Request** 
 
   - Send **POST** to `/updateProducts`
    - Request Header:
    ```JSON
    {"Content-Type":"application/json"}
    ```
    - Request body:
    ``` JSON
        {
        "Username": "user1",
        "Password": "squizz",
        "Products": [
            {
                "Code": "CFP-600-12",
                "ProductParameters": [{
                    "Key": "Name",
                    "Value": "CFP - 600/12 Swirl Diffusers  with  Low Profile Plenum 250 Spigot"
                }, {
                  ...
                },
                ]
            },{
            ...
            }
          ]
        }
    ```
- **Response**  
  ```JSON
  {
    "message": "import success",
    "status": "success"
  }
  ```
## 4. Order API
  ### 4.1： Make an order
-  **Request**
  - Send **POST** to `/api/purchase`
  - Request Header:
     ``` JSON
     {"Content-Type": "application/json"}
     ```
    - Request Body:
     ```JSON
     {"lines":[
         {            "barcode": "9326243001224",
                      "depth": 0,
                      "height": 0,
                      "id": 5,
                      "keyProductID": "21479231981826",
                      "lineType": "PRODUCT",
                      "price": 8.23,
                      "priceTotalExTax": 8.23,
                      "productCode": "01224",
                      "productCondition": null,
                      "productName": "Tarpaulin 240cm x 300cm (8' x 10')",
                      "productSearchCode": null,
                      "quantity": 1,
                      "stockLowQuantity": 0,
                      "stockQuantity": 0,
                      "totalPrice": 8.23,
                      "unitPrice": 8.23,
                      "volume": 0,
                      "weight": 0,
                      "width": 0},{
                      ...
                      }
          ],
          "sessionKey":"785BC1EC135931064EC38E81A0D85952"
        }
        ```
   **Response**:
        ``` JSON
          {
          "data": {
          "puchaseID": 35
          },
          "message": "Successfully inserted order and order details",
          "status": "success"
        }
        
        ```
   ### 4.2 get history order
- **Request** 
  - Send **GET** to `/api/history`
  - Take session_id as parameter e.g: `/api/history?session_id=785BC1EC135931064EC38E81A0D85952`
  
  - **Response**
    ``` JSON
    {
    "message": "Successfully retrieved order history",
    "orders": [
        {
            "billStatus": "SERVER_SUCCESS",
            "id": 33,
            "instructions": "Leave goods at the back entrance",
            "isDropship": "N",
            "lines": [
                {
                    "id": 30,
                    "keyProductId": "CRA350",
                    "orderId": 33,
                    "productCode": "CRA350",
                    "productId": 3504,
                    "productName": "Circular Louvred Diffuser",
                    "quantity": 1.00,
                    "totalPrice": 29.99,
                    "totalPriceExTax": 29.99,
                    "totalPriceIncTax": null,
                    "unitPrice": 29.99
                },
                {
                ...
                }
            ],
            "organizationId": 1,
            "supplierOrganizationId": "11EAF2251136B090BB69B6800B5BCB6D"
        },
       {
       ...
       }
    ],
    "status": "success"
}
    ```
    
  
