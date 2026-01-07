Section A: Limitations of RDBMS

Relational databases like MySQL work well when data structure is fixed, but they struggle with highly diverse product catalogs. In an e-commerce system, different products have different attributes. For example, laptops require fields like RAM and processor, while shoes need size and color. In an RDBMS, this leads to many nullable columns or multiple tables, making the schema complex and hard to manage.

Frequent schema changes are another limitation. Adding new product types often requires altering tables, which can be time-consuming and risky when the database is large. This reduces development speed and flexibility.

Additionally, storing customer reviews as nested data is difficult in relational databases. Reviews usually need separate tables and joins, which increases query complexity and affects performance. Overall, RDBMS systems lack flexibility when handling rapidly changing and diverse data structures.

Section B: NoSQL Benefits

MongoDB addresses these issues by offering a flexible and scalable document-based model. Its flexible schema allows different products to store different attributes within the same collection. This makes it easy to add new product types without modifying existing schemas.

MongoDB also supports embedded documents, allowing customer reviews to be stored directly inside product documents. This reduces the need for complex joins and improves read performance, especially for product-related queries.

Another key benefit is horizontal scalability. MongoDB can distribute data across multiple servers using sharding, allowing the system to handle large volumes of data and high user traffic efficiently. This makes MongoDB well suited for applications like FlexiMart, where the product catalog is continuously expanding.

Section C: Trade-offs

One disadvantage of using MongoDB instead of MySQL is weaker enforcement of relational constraints. MongoDB does not support foreign keys, making it harder to maintain strict relationships between entities like customers and orders.

Another drawback is data redundancy. Since MongoDB uses a denormalized structure, the same data may be duplicated across documents. This can lead to consistency issues if updates are not handled carefully. Additionally, for complex transactional systems, relational databases like MySQL still provide stronger ACID guarantees.