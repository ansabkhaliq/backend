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
    Send **GET** to `/api/barcode`
    take **barcode** as parameter e.g. `/api/barcode?barcode=933044000895`

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

    Send **GET** to `/api/product`
    take **productCode** as parameter e.g. `/api/barcode?productCode=CFP-600-20`

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

    Send **GET** to `/api/metadata/get`
    take **productCode** as parameter e.g. `/api/metadata/get?productCode=CFP-600-12`

- **Response**
    ```JSON
    {
    "found": "true",
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
        "Name": "CFP - 600/12 Swirl Diffusers  with  Low Profile Plenum 250 Spigot",
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
    
### 3.4 Retrieve product from squizz api
  **This is not a api that front end can assess.  These are supposed to be called by the Postman or another similar tool thatallow you to make calls to the REST API.
    This method is repsonbile for getting the latest products from SQUIZZ platform and updating the table in the local database **
- **Request** 
    Before retrieve data from squizz api, you should log in first 
    Send **GET** to `/retrieveProduct`
  
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
  **This method is repsonbile for getting the latest price from SQUIZZ platform and updating the table in the local database **
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
  **This method is repsonbile for getting the latest products from SQUIZZ platform and updating the table in the local database **
- **Request** 
    Before retrieve data from squizz api, you should log in first 
    Send **GET** to `/updateProducts`
   
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
  **This method is repsonbile for getting the latest products from SQUIZZ platform and updating the table in the local database **
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
  **This method is repsonbile for getting the latest  3d model's metadata **
- **Request** 
 
    Send **POST** to `/updateProducts`
    Header:
    ```JSON
    {"Content-Type":"application/json"}
    ```
    request body:
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
                    "Key": "URL",
                    "Value": "http://www.holyoake.com"
                }, {
                    "Key": "Type Comments",
                    "Value": "Holyoake Swirl Diffuser CFP-600/12 c/w Low Profile Plenum."
                }, {
                    "Key": "Static Pressure Min",
                    "Value": "2 Pa"
                }, {
                    "Key": "Static Pressure Max",
                    "Value": "28 Pa"
                }, {
                    "Key": "Noise Level NC Min",
                    "Value": "5 NC"
                }, {
                    "Key": "Noise Level NC Max",
                    "Value": "32NC"
                }, {
                    "Key": "Model",
                    "Value": "CFP-600/12 Low Profile complete with low profile plenum."
                }, {
                    "Key": "Min Flow (Hvac Air Flow Liters Per Second)",
                    "Value": "25.000000000000"
                }, {
                    "Key": "Max Flow (Hvac Air Flow Liters Per Second)",
                    "Value": "200.000000000000"
                }, {
                    "Key": "Material Body",
                    "Value": "Holyoake-Aluminium"
                }, {
                    "Key": "Material - Face",
                    "Value": "Holyoake White"
                }, {
                    "Key": "Manufacturer",
                    "Value": "Holyoake"
                }, {
                    "Key": "d_r (Length Millimeters)",
                    "Value": "125.000000000000"
                }, {
                    "Key": "Inlet Spigot Diameter (Length Millimeters)",
                    "Value": "250.000000000000"
                }, {
                    "Key": "Plenum Box Height (Length Millimeters)",
                    "Value": "250.000000000000"
                }, {
                    "Key": "Holyoake Product Range",
                    "Value": "Holyoake Swirl Diffusers."
                }, {
                    "Key": "Flow Nom (Hvac Air Flow Liters Per Second)",
                    "Value": "112.500000000000"
                }, {
                    "Key": "Diffuser Width (Length Millimeters)",
                    "Value": "595.000000000000"
                }, {
                    "Key": "Plenum Box Width (Length Millimeters)",
                    "Value": "570.000000000000"
                }, {
                    "Key": "Description",
                    "Value": "Radial Swirl Diffusers, Ceiling Fixed Pattern shall be Holyoake Model CFP-600/12.  Ceiling Radial Swirl Diffusers shall be designed for use in Variable Air Volume (VAV) systems with Highly Turbulent Radial  Air Flow Pattern and shall be suitable for ceiling heights of 2.4 to 4m. Ceiling Radial Swirl Diffusers shall maintain a COANDA effect at reduced air volumes and provide uniform temperature gradients throughout the occupied space. Diffusers shall be finished in powder coat and fitted with accessories and dampers where indicated as manufactured by Holyoake"
                }]
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

