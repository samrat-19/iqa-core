db_metadata = {
  "tables": [
    {
      "foreignKeys": [],
      "primaryKeys": [
        {
          "pkName": "PRIMARY",
          "pkColumn": "id"
        }
      ],
      "columns": [
        "id",
        "order_id",
        "product_id",
        "quantity"
      ],
      "description": "This table stores itemized details of orders, linking each product to its respective order and quantity ordered.",
      "tableName": "order_items"
    },
    {
      "foreignKeys": [
        {
          "referencedTable": "orders",
          "referencedColumn": "id",
          "fkName": "order_items_ibfk_1",
          "fkColumn": "order_id"
        }
      ],
      "primaryKeys": [
        {
          "pkName": "PRIMARY",
          "pkColumn": "id"
        }
      ],
      "columns": [
        "id",
        "user_id",
        "total_amount",
        "status",
        "created_at"
      ],
      "description": "Database table \"orders\" stores order data with foreign key to \"order_items\", containing user-specific information and order status.",
      "tableName": "orders"
    },
    {
      "foreignKeys": [
        {
          "referencedTable": "products",
          "referencedColumn": "id",
          "fkName": "order_items_ibfk_2",
          "fkColumn": "product_id"
        }
      ],
      "primaryKeys": [
        {
          "pkName": "PRIMARY",
          "pkColumn": "id"
        }
      ],
      "columns": [
        "id",
        "name",
        "price"
      ],
      "description": "Products table contains unique product IDs with attributes name and price, related to order items through product ID.",
      "tableName": "products"
    },
    {
      "foreignKeys": [
        {
          "referencedTable": "users",
          "referencedColumn": "id",
          "fkName": "orders_ibfk_1",
          "fkColumn": "user_id"
        }
      ],
      "primaryKeys": [
        {
          "pkName": "PRIMARY",
          "pkColumn": "id"
        }
      ],
      "columns": [
        "id",
        "name",
        "email",
        "created_at"
      ],
      "description": "Users table stores information about user accounts with attributes: id, name, email and creation date. Related to orders through a foreign key referencing the users table.",
      "tableName": "users"
    }
  ],
  "databaseProductName": "MySQL"
}
