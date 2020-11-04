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
   - Take **productCode** as parameter e.g. `/api/product?productCode=CFP-600-20`

- **Response**
    ```JSON
  {
    "data": {
         "data": {
        "averageCost": null,
        "barcode": null,
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
        "id": 3431,
        "imageList": null,
        "internalID": null,
        "isKitted": null,
        "isPriceTaxInclusive": null,
        "keyProductID": "CFP600/20",
        "keySellUnitID": null,
        "keyTaxcodeID": null,
        "kitProductsSetPrice": null,
        "name": null,
        "packQuantity": null,
        "priceList": null,
        "productCode": "CFP-600-20",
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
      
    }
    ```


### 3.4 Search for product codes or barcodes similar to a given identifier
This endpoint is used for live product search in the frontend `OrderPage` component
- **Request** 
    - Send **GET** to `/api/products/search`
    - Take **identifier** and **identifierType** as parameters, where `identifierType` is either `barcode` or `productCode`
    
      e.g. `/api/products/search?identifier=CFP-600-12&identifierType=productCode`

- **Response**
  ```JSON
  {
    "identifiers": [
        {
            "productCode": "CFP-600-12-LPP-150"
        },
        {
            "productCode": "CFP-600-12-LPP-200"
        },
        ...
        {
            "productCode": "CFP-600-12-LPP-250"
        }
    ],
    "message": "Successfully retrieved similar barcodes or product codes",
    "status": "success"
  }
  ```

    
### 3.5 Retrieve product from squizz api
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

  ### 3.6 Retrieve product price from squizz api
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

### 3.7 Update product from squizz api
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

  ### 3.8 Update product price from squizz api
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

### 3.9 import metadata
  **This is not a api that front end can access.  These are supposed to be called by the Postman or another similar tool that allow you to make calls to the REST API.**
  **This method is repsonbile for getting the latest  3d model's metadata**
- **Request** 
 
   - Send **POST** to `/metadata/import`
    - Request Header:
    ```JSON
    {"Content-Type":"application/json"}
    ```
    - Request body:
    ```JSON
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
  
  ### 3.10 import threedmodel
  **This is not a api that front end can access.  These are supposed to be called by the Postman or another similar tool that allow you to make calls to the REST API.**
  **After uploading the 3D model into server you should use this API to record the location of model in server **
- **Request** 
   - Send **POST** to `/threedmodel/import`
    - Request Header:
    ```JSON
    {"Content-Type":"application/json"}
    ```
    - Request body:
    ```JSON
        {"Username": "user1",
            "Password": "squizz",
            "Products": [{
                "Code": "CFP-600-20-LPP",
                "ProductParameters": null,
                "ModelURL": "https://s3-ap-southeast-2.amazonaws.com/awstest.project/3dModels/600_20_low Profile.glb"
            },{
            ...
            }]
            }
    ```
- **Response**  
  ```JSON
  {
    "message": "import success",
    "status": "success"
  }
  ```
  
### 3.11 get model's metadata 
 - **Request** 
   - Send **GET** to `/api/metadata/get`   
     the parameter is the productCode e.g`/api/metadata/get?productCode=CFP-600-12-LPP-200`
 - **Response**  
  ```JSON
{
    "found": true,
    "json_data": {
        "Description": "Radial Swirl Diffusers, Ceiling Fixed Pattern shall be Holyoake Model CFP-600/12.  Ceiling Radial Swirl Diffusers shall be designed for use in Variable Air Volume (VAV) systems with Highly Turbulent Radial  Air Flow Pattern and shall be suitable for ceiling heights of 2.4 to 4m. Ceiling Radial Swirl Diffusers shall maintain a COANDA effect at reduced air volumes and provide uniform temperature gradients throughout the occupied space. Diffusers shall be finished in powder coat and fitted with accessories and dampers where indicated as manufactured by Holyoake",
        "Diffuser Width (Length Millimeters)": "595.000000000000",
        "Flow Nom (Hvac Air Flow Liters Per Second)": "112.500000000000",
        "Holyoake Product Range": "Holyoake Swirl Diffusers.",
        "Inlet Spigot Diameter (Length Millimeters)": "250.000000000000",
        "Manufacturer": "Holyoake",
        "Material - Face": "Holyoake White",
        "Material Body": "Holyoake-Aluminium",
        "Max Flow (Hvac Air Flow Liters Per Second)": "200.000000000000",
        "Min Flow (Hvac Air Flow Liters Per Second)": "25.000000000000",
        "Model": "CFP-600/12 Low Profile complete with low profile plenum.",
        "Name": "CFP - 600/12  Swirl Diffusers  with Low Profile Plenum 200 Spigot",
        "Noise Level NC Max": "32NC",
        "Noise Level NC Min": "5 NC",
        "Plenum Box Height (Length Millimeters)": "250.000000000000",
        "Plenum Box Width (Length Millimeters)": "570.000000000000",
        "Static Pressure Max": "28 Pa",
        "Static Pressure Min": "2 Pa",
        "Type Comments": "Holyoake Swirl Diffuser CFP-600/12 c/w Low Profile Plenum.",
        "URL": "http://www.holyoake.com",
        "d_r (Length Millimeters)": "125.000000000000"
    }
}
  ```
     
## 4. Order API
 
   ### 4.1 get history order
- **Request** 
  - Send **GET** to `/api/history`
  - Take session_id as parameter e.g: `/api/history?session_id=785BC1EC135931064EC38E81A0D85952`
  
- **Response**
    ```JSON
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
    
  
