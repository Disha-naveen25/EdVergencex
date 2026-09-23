import streamlit as st
import pandas as pd
import requests
from pathlib import Path


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Product Explorer",
    page_icon="🛍️",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🛍️ Product Explorer")
st.subheader("API-Based Product Data Dashboard")

st.write(
    "Explore product information fetched from a public API, "
    "filter products, view category statistics, and download data as CSV."
)


# --------------------------------------------------
# API CONFIGURATION
# --------------------------------------------------

api_url = "https://dummyjson.com/products"


# --------------------------------------------------
# LOAD FALLBACK DATA
# --------------------------------------------------

def load_fallback_data():
    fallback_file = Path("products_fallback.csv")

    if fallback_file.exists():
        return pd.read_csv(fallback_file)

    return pd.DataFrame(
        columns=[
            "product_id",
            "title",
            "brand",
            "category",
            "api_price",
            "rating",
            "stock"
        ]
    )


# --------------------------------------------------
# FETCH PRODUCTS FROM API
# --------------------------------------------------

def fetch_products(limit):
    parameters = {
        "limit": limit
    }

    try:
        response = requests.get(
            api_url,
            params=parameters,
            timeout=10
        )

        response.raise_for_status()

        api_data = response.json()

        products = pd.DataFrame(api_data["products"])

        products = products[
            [
                "id",
                "title",
                "brand",
                "category",
                "price",
                "rating",
                "stock"
            ]
        ]

        products = products.rename(
            columns={
                "id": "product_id",
                "price": "api_price"
            }
        )

        return products, "Live API"

    except (requests.RequestException, ValueError):

        products = load_fallback_data()

        return products, "Fallback CSV"


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("⚙️ API Settings")

number_of_products = st.sidebar.slider(
    "Number of products",
    min_value=5,
    max_value=30,
    value=10,
    step=5
)

fetch_button = st.sidebar.button(
    "🔄 Fetch Products"
)


# --------------------------------------------------
# FETCH DATA
# --------------------------------------------------

if fetch_button or "products" not in st.session_state:

    products, data_source = fetch_products(
        number_of_products
    )

    st.session_state.products = products
    st.session_state.data_source = data_source


# Get stored data

products = st.session_state.products
data_source = st.session_state.data_source


# --------------------------------------------------
# DATA SOURCE STATUS
# --------------------------------------------------

if data_source == "Live API":

    st.success(
        "🟢 Data Source: Live DummyJSON API"
    )

else:

    st.warning(
        "🟡 Data Source: Fallback CSV"
    )


st.caption(
    f"API Endpoint: {api_url}"
)


# --------------------------------------------------
# PRODUCT OVERVIEW
# --------------------------------------------------

st.header("📊 Product Overview")

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Products",
        len(products)
    )


with col2:

    average_price = products["api_price"].mean()

    st.metric(
        "Average Price",
        f"${average_price:.2f}"
    )


with col3:

    average_rating = products["rating"].mean()

    st.metric(
        "Average Rating",
        f"{average_rating:.2f}"
    )


# --------------------------------------------------
# SHOW API DATA
# --------------------------------------------------

st.header("📦 Product Data")

st.dataframe(
    products,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# FILTER SECTION
# --------------------------------------------------

st.header("🔎 Product Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)


with filter_col1:

    categories = ["All"] + sorted(
        products["category"].unique().tolist()
    )

    selected_category = st.selectbox(
        "Category",
        categories
    )


with filter_col2:

    minimum_rating = st.slider(
        "Minimum Rating",
        min_value=0.0,
        max_value=5.0,
        value=4.0,
        step=0.1
    )


with filter_col3:

    minimum_stock = st.number_input(
        "Minimum Stock",
        min_value=0,
        value=1,
        step=1
    )


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

recommended_products = products[
    (products["rating"] >= minimum_rating)
    &
    (products["stock"] >= minimum_stock)
]


if selected_category != "All":

    recommended_products = recommended_products[
        recommended_products["category"]
        == selected_category
    ]


# Sort by rating

recommended_products = recommended_products.sort_values(
    "rating",
    ascending=False
)


# --------------------------------------------------
# RECOMMENDED PRODUCTS
# --------------------------------------------------

st.header("⭐ Recommended Products")

if len(recommended_products) > 0:

    st.dataframe(
        recommended_products[
            [
                "product_id",
                "title",
                "brand",
                "category",
                "api_price",
                "rating",
                "stock"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No products match the selected filters."
    )


# --------------------------------------------------
# CATEGORY SUMMARY
# --------------------------------------------------

st.header("📈 Category Summary")

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


category_summary["average_price"] = (
    category_summary["average_price"]
    .round(2)
)


category_summary["average_rating"] = (
    category_summary["average_rating"]
    .round(2)
)


st.dataframe(
    category_summary,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# DOWNLOAD SECTION
# --------------------------------------------------

st.header("📥 Download Data")


all_products_csv = products.to_csv(
    index=False
).encode("utf-8")


recommended_products_csv = recommended_products.to_csv(
    index=False
).encode("utf-8")


download_col1, download_col2 = st.columns(2)


with download_col1:

    st.download_button(
        label="⬇️ Download All Products",
        data=all_products_csv,
        file_name="api_products.csv",
        mime="text/csv"
    )


with download_col2:

    st.download_button(
        label="⬇️ Download Recommended Products",
        data=recommended_products_csv,
        file_name="recommended_products.csv",
        mime="text/csv"
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Mini Project: Product Explorer | "
    "GET Request • Parameters • JSON • Pandas • CSV • Streamlit"
)