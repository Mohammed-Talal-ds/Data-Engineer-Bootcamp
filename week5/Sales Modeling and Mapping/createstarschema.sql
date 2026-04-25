CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE NOT NULL,
    day INT,
    month INT,
    year INT,
    quarter INT,
    weekday VARCHAR(10),
    is_weekend BOOLEAN,

    is_ramadan BOOLEAN DEFAULT FALSE,
    is_eid_al_fitr BOOLEAN DEFAULT FALSE,
    is_eid_al_adha BOOLEAN DEFAULT FALSE
);


CREATE TABLE dim_users (
    user_id INT PRIMARY KEY,
    full_name VARCHAR(150),
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT
);

CREATE TABLE dim_branches (
    branch_id INT PRIMARY KEY,
    branch_name VARCHAR(100),
    city VARCHAR(50),
    manager_name VARCHAR(100)
);

CREATE TABLE dim_products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(200),
    brand_name VARCHAR(100),
    category_name VARCHAR(100)
);

CREATE TABLE dim_payment_methods (
    method_id INT PRIMARY KEY,
    method_name VARCHAR(50)
);

CREATE TABLE dim_currencies (
    currency_id INT PRIMARY KEY,
    currency_code VARCHAR(3),
    currency_name VARCHAR(50)
);