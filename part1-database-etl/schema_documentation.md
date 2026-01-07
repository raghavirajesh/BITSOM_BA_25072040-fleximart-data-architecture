SECTION 1: Entity–Relationship Description

Entity–Relationship Description

ENTITY: customers
Purpose: Stores customer personal and contact information.

Attributes:
customer_id (Primary Key): Unique identifier for each customer
first_name: Customer’s first name
last_name: Customer’s last name
email: Customer’s email address (unique)
phone: Customer’s phone number
city: Customer’s city
registration_date: Date of customer registration

Relationships:
One customer can place many sales

Relationship type: 
One-to-Many (customers → sales)

ENTITY: products
Purpose: Stores product-related details.

Attributes:
product_id (Primary Key): Unique identifier for each product
product_name: Name of the product
category: Product category
price: Price of the product
stock_quantity: Quantity available in stock

Relationships:
One product can be associated with many sales

Relationship type: 
One-to-Many (products → sales)

ENTITY: sales
Purpose: Stores transactional sales information.

Attributes:
transaction_id (Primary Key): Unique identifier for each transaction
customer_id (Foreign Key): References customers.customer_id
product_id (Foreign Key): References products.product_id
quantity: Number of units sold
unit_price: Price per unit
transaction_date: Date of transaction
status: Status of the order

Relationships:
Many sales belong to one customer
Many sales belong to one product

SECTION 2: Normalization Explanation (3NF)

The database is designed following Third Normal Form (3NF) to ensure proper organization of data and to reduce redundancy. Each table represents a single entity, and all attributes in a table depend only on the primary key.

In the customers table, attributes such as first_name, last_name, email, phone, city, and registration_date are directly dependent on customer_id. There are no repeating groups or multi-valued attributes, which satisfies First Normal Form (1NF). Since customer_id is a single primary key and all non-key attributes depend fully on it, the table also satisfies Second Normal Form (2NF).

The products table stores only product-related information. Attributes like product_name, category, price, and stock_quantity depend entirely on product_id. Product details are not duplicated in other tables, which helps maintain data consistency and avoids unnecessary redundancy.

The sales table stores transaction-level information and connects customers and products using foreign keys. Attributes such as quantity, unit_price, transaction_date, and status depend only on transaction_id. Customer and product details are not stored directly in the sales table; instead, references are used. This removes transitive dependencies and ensures the table follows Third Normal Form (3NF).

This normalized design helps prevent update anomalies by allowing changes to customer or product information in one place. Insert anomalies are avoided because customer and product records can be added independently of sales. Delete anomalies are prevented since deleting a sales record does not remove customer or product data. Overall, normalization improves data consistency and makes the database easier to understand and maintain.

SECTION 3: Sample Data Representation

Examples used from the csv files.
### Customers Table

| customer_id | first_name | last_name | email                    | phone           | city       | registration_date |
|------------|------------|-----------|--------------------------|-----------------|------------|-------------------|
| C001       | Rahul      | Sharma    | rahul.sharma@gmail.com   | 9876543210      | Bangalore  | 2023-01-15        |
| C002       | Priya      | Patel     | priya.patel@yahoo.com    | +91-9988776655  | Mumbai     | 2023-02-20        |

### Products Table

| product_id | product_name           | category     | price    | stock_quantity |
|-----------|------------------------|--------------|----------|----------------|
| P001      | Samsung Galaxy S21     | Electronics  | 45999.00 | 150            |
| P002      | Nike Running Shoes     | Fashion      | 3499.00  | 80             |

### Sales Table

| transaction_id | customer_id | product_id | quantity | unit_price | transaction_date | status     |
|---------------|------------|------------|----------|------------|------------------|------------|
| T001          | C001       | P001       | 1        | 45999.00   | 2024-01-15       | Completed  |
| T002          | C002       | P004       | 2        | 2999.00    | 2024-01-16       | Completed  |

