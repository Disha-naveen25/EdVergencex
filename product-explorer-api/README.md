````markdown
#  Product Explorer – API Based Product Dashboard

Product Explorer is a beginner-friendly Streamlit mini project that retrieves product information from a public REST API, processes the JSON response using Pandas, filters products based on user-selected conditions, generates category-wise statistics, and allows the processed data to be downloaded as CSV files.

This project was developed based on the concepts learned during an API and Python training session.

---

##  Project Overview

The application uses the **DummyJSON Products API** to fetch current product information using an HTTP GET request.

The API response is received in JSON format and converted into a Pandas DataFrame for further processing.

Users can:

- Fetch a selected number of products from the API
- View product information in a table
- Filter products by category
- Filter products by minimum rating
- Filter products by minimum stock
- View recommended products
- View category-wise product statistics
- View average price and rating
- Download all product data as CSV
- Download filtered/recommended products as CSV

If the public API is unavailable, the application automatically uses a local fallback CSV file.

---

##  Objectives

The main objectives of this project are to understand and implement:

- HTTP GET requests
- API parameters
- JSON responses
- Public REST APIs
- Pandas DataFrames
- Data filtering
- Data sorting
- Grouping and aggregation
- CSV file handling
- Exception handling
- Streamlit frontend development
- GitHub project management
- Streamlit deployment

---

##  Technologies Used

- **Python**
- **Streamlit**
- **Pandas**
- **Requests**
- **DummyJSON API**
- **CSV**
- **GitHub**
- **Streamlit Community Cloud**

---

##  Public API

The project uses the DummyJSON Products API.

API endpoint:

`https://dummyjson.com/products`

No API key is required.

---

##  How the Application Works

The application follows this workflow:

```text
User
  ↓
Select Number of Products
  ↓
GET Request
  ↓
DummyJSON Public API
  ↓
JSON Response
  ↓
Convert JSON to Pandas DataFrame
  ↓
Filter and Sort Products
  ↓
Category-wise Analysis
  ↓
Display Results
  ↓
Download Data as CSV
````

---

##  GET Request and Parameters

The application sends a GET request using the Python `requests` library.

The number of products is selected by the user through the Streamlit sidebar.

The selected value is passed to the API as a parameter.

Example:

```python
parameters = {
    "limit": limit
}

response = requests.get(
    api_url,
    params=parameters,
    timeout=10
)
```

The `limit` parameter controls the number of products requested from the API.

---

##  JSON Response Processing

After receiving the response from the API, the JSON data is extracted using:

```python
api_data = response.json()
```

The product records are then converted into a Pandas DataFrame:

```python
products = pd.DataFrame(api_data["products"])
```

Only the required product fields are selected:

* Product ID
* Product title
* Brand
* Category
* Price
* Rating
* Stock

The columns `id` and `price` are renamed to `product_id` and `api_price`.

---

##  Product Overview

The dashboard displays three basic product statistics:

### Total Products

Displays the total number of products retrieved.

### Average Price

Calculates the average price of the retrieved products.

### Average Rating

Calculates the average rating of the retrieved products.

---

##  Product Filtering

Users can filter products using three conditions:

### Category

Users can select a specific product category or choose `All`.

### Minimum Rating

Users can select the minimum rating required for a product.

### Minimum Stock

Users can specify the minimum stock quantity.

The application applies these conditions using Pandas filtering.

Example:

```python
recommended_products = products[
    (products["rating"] >= minimum_rating)
    &
    (products["stock"] >= minimum_stock)
]
```

The filtered products are then sorted by rating in descending order.

---

##  Recommended Products

Products that satisfy the selected filtering conditions are displayed under the **Recommended Products** section.

The displayed information includes:

* Product ID
* Product title
* Brand
* Category
* Price
* Rating
* Stock

If no products match the selected conditions, the application displays a message informing the user.

---

##  Category Summary

The application groups products based on their category.

For each category, it calculates:

* Number of products
* Average price
* Average rating

This is implemented using Pandas `groupby()` and `agg()`.

Example:

```python
category_summary = (
    products
    .groupby("category")
    .agg(
        number_of_products=("product_id", "count"),
        average_price=("api_price", "mean"),
        average_rating=("rating", "mean")
    )
    .reset_index()
)
```

The average price and average rating are rounded to two decimal places.

---

##  CSV Download

The application provides two download options.

### 1. All Products

Downloads the complete API dataset as:

```text
api_products.csv
```

### 2. Recommended Products

Downloads the filtered products as:

```text
recommended_products.csv
```

The CSV files are generated using Pandas.

Example:

```python
products.to_csv(
    index=False
)
```

---

##  Fallback Mechanism

The application includes a fallback mechanism in case the public API is unavailable.

The local file:

```text
products_fallback.csv
```

contains sample product data.

If the API request fails, the application automatically loads the fallback CSV using Pandas.

This allows the application to continue working even when the API cannot be accessed.

---

##  Project Structure

```text
Product-Explorer-API/
│
├── app.py
├── products_fallback.csv
├── requirements.txt
└── README.md
```

### `app.py`

Contains the Streamlit application, API request logic, data processing, filtering, category analysis, and CSV download functionality.

### `products_fallback.csv`

Contains sample product data used when the public API is unavailable.

### `requirements.txt`

Contains the Python libraries required to run the application.

### `README.md`

Contains project documentation and setup instructions.

---

##  Requirements

The project requires:

```text
streamlit
pandas
requests
```

These dependencies are listed in `requirements.txt`.

---

##  Running the Project Locally

### Step 1: Clone the Repository

```bash
git clone https://github.com/Disha-naveen25/EdVergencex/new/main/product-explorer-api
```

### Step 2: Open the Project Folder

```bash
cd Product-Explorer-API
```

### Step 3: Install the Required Libraries

```bash
pip install -r requirements.txt
```

### Step 4: Run the Streamlit Application

```bash
streamlit run app.py
```

The application will open in your web browser.

---

### Live Demo

**https://mini-project3.streamlit.app/**

---

##  Learning Outcomes

Through this mini project, the following concepts were practiced:

1. Sending HTTP GET requests
2. Passing parameters to a public API
3. Handling JSON responses
4. Converting JSON data into a Pandas DataFrame
5. Selecting required columns
6. Renaming DataFrame columns
7. Filtering data using conditions
8. Sorting DataFrame records
9. Grouping and aggregating data
10. Calculating averages
11. Reading and writing CSV files
12. Handling API request failures
13. Building an interactive Streamlit interface
14. Using GitHub for project management
15. Deploying a Streamlit application

---

##  Project Flow

```text
DummyJSON API
      ↓
HTTP GET Request
      ↓
Parameters
      ↓
JSON Response
      ↓
Pandas DataFrame
      ↓
Data Selection
      ↓
Filtering & Sorting
      ↓
Category Grouping
      ↓
Streamlit Dashboard
      ↓
CSV Download
```

If the API is unavailable:

```text
API Request
     ↓
Request Failure
     ↓
Fallback CSV
     ↓
Pandas DataFrame
     ↓
Streamlit Dashboard
```


##  Project Summary

**Product Explorer** is a simple API-based data dashboard that demonstrates how a public REST API can be accessed using a GET request, how JSON responses can be processed using Pandas, and how the resulting data can be filtered, analyzed, displayed through Streamlit, and exported as CSV files.

````

### Your final folder should be exactly:

```text
Product-Explorer-API
│
├── app.py
├── products_fallback.csv
├── requirements.txt
└── README.md
````

