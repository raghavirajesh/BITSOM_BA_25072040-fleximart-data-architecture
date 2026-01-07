# Star Schema Design Documentation

## Section 1: Schema Overview

A star schema is used to store and analyze sales data in a simple and organized way.  
In this design, the main table is the `fact_sales` table, which stores numerical sales information.  
This fact table is connected to multiple dimension tables that store descriptive details.

### FACT TABLE: fact_sales

**Grain:** One record for each product sold in an order  
**Business Process:** Sales transactions

**Measures:**
- quantity_sold: Number of items sold
- unit_price: Price of one unit
- discount_amount: Discount applied on the sale
- total_amount: Final sale amount after discount

**Foreign Keys:**
- date_key (linked to dim_date)
- product_key (linked to dim_product)
- customer_key (linked to dim_customer)

---

### DIMENSION TABLE: dim_date

The date dimension is used to analyze sales based on time.

**Attributes:**
- date_key (Primary Key): Unique date in YYYYMMDD format
- full_date: Actual date
- day_of_week: Day name
- month: Month number
- month_name: Name of the month
- quarter: Quarter of the year
- year: Year
- is_weekend: Indicates whether the date is a weekend

---

### DIMENSION TABLE: dim_product

The product dimension stores details related to products.

**Attributes:**
- product_key (Primary Key)
- product_id: Original product ID
- product_name: Name of the product
- category: Product category
- brand: Brand name

---

### DIMENSION TABLE: dim_customer

The customer dimension stores information about customers.

**Attributes:**
- customer_key (Primary Key)
- customer_id: Original customer ID
- customer_name: Name of the customer
- city: City of the customer
- state: State of the customer
- country: Country of the customer

---

## Section 2: Design Decisions

The transaction line-item level was chosen because it stores detailed sales data. This allows different types of analysis such as total sales by product, customer, or date. Having detailed data makes reporting more flexible.

Surrogate keys are used instead of natural keys because they are simpler and improve performance. They also help in handling changes in data without affecting existing records.

This star schema design supports drill-down and roll-up operations. For example, users can analyze sales yearly and then drill down to monthly or daily sales using the date dimension. Similarly, sales can be analyzed by category and then by individual products.

---

## Section 3: Sample Data Flow

**Source Transaction:**  
Order \#302, Customer "Sneha Reddy", Product "Smartphone", Quantity: 1, Price: 30000


**Stored in Data Warehouse:**

**fact_sales:**
{
date_key: 20240210,
product_key: 8,
customer_key: 20,
quantity_sold: 1,
unit_price: 30000,
discount_amount: 2000,
total_amount: 28000
}

**dim_date:**
{ date_key: 20240210, full_date: '2024-02-10', month: 2, quarter: 'Q1', year: 2024 }

**dim_product:**
{ product_key: 8, product_name: 'Smartphone', category: 'Electronics' }

**dim_customer:**
{ customer_key: 20, customer_name: 'Sneha Reddy', city: 'Hyderabad' }

This example shows how a single sales transaction is transformed into a fact record linked to multiple dimension tables using surrogate keys.
