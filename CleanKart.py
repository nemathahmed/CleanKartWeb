
import pandas as pd
from streamlit_card import card
import random

import json 
image_cache = {}

# def get_product_image_url(product_name):
#     # Check if the image URL is already cached
#     if product_name in image_cache:
#         return image_cache[product_name]

#     try:
#         # Perform a Google search for the product name and get the first image result
#         search_results = search(product_name + " product", num=1, stop=1, pause=2)
        
#         # Extract the URL of the first image result
#         for url in search_results:
#             if url.endswith(('.jpg', '.png', '.jpeg', '.gif', '.bmp', '.webp')):
#                 # Cache the image URL
#                 image_cache[product_name] = url
#                 return url
#     except Exception as e:
#         print("Error:", e)
    
#     # Return None if no image URL is found
#     return None




# Function to load cart data from a JSON file
# Function to load cart data from a JSON file
def load_cart():
    try:
        with open("cart.json", "r") as file:
            data = file.read()
            if data:  # Check if the file is not empty
                return json.loads(data)
            else:
                return {}  # Return an empty cart if the file is empty
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Return an empty cart if the file is not found or corrupted

# Function to save cart data to a JSON file
def save_cart(cart):
    with open("cart.json", "w") as file:
        json.dump(cart, file)

# Load cart data from the file
cart = load_cart()
# Load CSV data
@st.cache  # This will cache the data for better performance
def load_data():
    data = pd.read_csv('GroceryDB_foods.csv')  # Replace 'GroceryDB_foods.csv' with your CSV file
    return data

products_data = load_data()

# Get unique categories from the 'store' column
categories = products_data['store'].unique()

# Streamlit app
st.title('Clean Kart')

# Search bar
search_query = st.text_input('Search for a product:')
selected_category = st.selectbox('Select a store:', ['All'] + list(categories))

# Filter products based on search query and selected category
filtered_data = products_data.copy()
filtered_data = filtered_data.dropna(subset=['f_FPro'])
if selected_category != 'All':
    filtered_data = filtered_data[filtered_data['store'] == selected_category]
if search_query:
    filtered_data = filtered_data.dropna(subset=['name']) 
    filtered_data = filtered_data[filtered_data['name'].str.contains(search_query, case=False)]

# Display random products as cards
st.write(f"Found {len(filtered_data)} results:")
col1, col2= st.columns(2)
col3, col4= st.columns(2)
cols=[col1, col2,col3,col4 ]


i=0
rows=[]
num_products_displayed = 4
i=0
for index, row in filtered_data.head(num_products_displayed).iterrows():
    product_name = row['name']
    f_FPro = round(row['f_FPro'], 2)
    f_min_FPro = round(row['f_min_FPro'], 2)
    add_to_cart_button = cols[i].button(f"Add Product",key=product_name)

    # If "Add to Cart" button is clicked, add the product to the cart
    if add_to_cart_button:
        if product_name in cart:
            cart[product_name] += 1
        else:
            cart[product_name] = 1
        st.success(f"{product_name} added to cart!")
        print(cart)
    # Display product details
    cols[i].metric(product_name, f_FPro, f_min_FPro)
    num_products_displayed -= 1
    i += 1

# Button to load more products
if st.button("Load More"):
    num_products_displayed += 4
    for index, row in filtered_data.iloc[num_products_displayed:num_products_displayed+4].iterrows():
        # Display new products
        add_to_cart_button = cols[num_products_displayed % 4].button(f"Add Product",key=row['name'])
        cols[num_products_displayed % 4].metric(row['name'], round(row['f_FPro'], 2), round(row['f_min_FPro'], 2))
        num_products_displayed += 1

else:
    st.warning('No results found.')

# Save the cart data to the file
save_cart(cart)
st.title('Your Cart')
# When "Remove" button is clicked, remove the item from the cart
for product in list(cart.keys()):
    quantity = cart[product]
    remove_button = st.button(f"Remove {product} from Cart ({quantity} in cart)")
    if remove_button:
        if quantity > 1:
            cart[product] -= 1
        else:
            del cart[product]
        st.success(f"{product} removed from cart!")

# Save the cart data to the file
save_cart(cart)

# Calculate and display the average f_FPro for all products in the cart
if cart:
    total_f_FPro = 0
    total_products = 0
    for product, quantity in cart.items():
        # Assuming products_data is your original data source containing 'f_FPro' values
        # You need to replace it with your actual data source.
        f_FPro = filtered_data.loc[filtered_data['name'] == product, 'f_FPro'].values[0]
        total_f_FPro += f_FPro * quantity
        total_products += quantity
    avg_f_FPro = total_f_FPro / total_products

    st.metric("Average Processed Content In Your Cart", avg_f_FPro, min(0,f_FPro-0.25))

else:
    st.warning("Your cart is empty.")

# Save the cart data to the file
save_cart(cart)


# Display cart contents

# for product, quantity in cart.items():
#     st.write(f"- {product}: {quantity}")