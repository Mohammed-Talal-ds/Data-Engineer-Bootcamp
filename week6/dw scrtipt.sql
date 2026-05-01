CREATE DATABASE brazilian_ecommerce_dw;
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id TEXT,
    customer_unique_id TEXT,
    zip_code_prefix INT,
    city TEXT,
    state TEXT,

    start_date DATE,
    end_date DATE,
    is_current BOOLEAN
);

CREATE TABLE dim_seller (
    seller_key SERIAL PRIMARY KEY,
    seller_id TEXT,
    zip_code_prefix INT,
    city TEXT,
    state TEXT,

    start_date DATE,
    end_date DATE,
    is_current BOOLEAN
);

CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id TEXT,
    category_name TEXT,
    category_name_english TEXT,

    weight_g REAL,
    length_cm REAL,
    height_cm REAL,
    width_cm REAL,

    start_date DATE,
    end_date DATE,
    is_current BOOLEAN
);



CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day INT,
    month INT,
    year INT,
    quarter INT,
    weekday INT,
    is_weekend BOOLEAN
);

CREATE TABLE dim_payment_type (
    payment_type_key SERIAL PRIMARY KEY,
    payment_type TEXT
);


CREATE TABLE dim_order_status (
    order_status_key SERIAL PRIMARY KEY,
    order_status TEXT
);


CREATE TABLE dim_lead (
    lead_key SERIAL PRIMARY KEY,
    mql_id TEXT,
    origin TEXT,
    landing_page_id TEXT,
    lead_type TEXT,
    business_segment TEXT,

    start_date DATE,
    end_date DATE,
    is_current BOOLEAN
);

CREATE TABLE dim_review (
    review_dim_key SERIAL PRIMARY KEY,
    review_id TEXT,
    review_comment_title TEXT,
    review_comment_message TEXT
);

CREATE TABLE fact_order_items (
    order_item_key SERIAL PRIMARY KEY,

    -- Degenerate
    order_id TEXT NOT NULL,

    -- Foreign Keys
    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    seller_key INT NOT NULL,

    order_date_key INT NOT NULL,
    shipping_limit_date_key INT,

    -- Measures
    price REAL NOT NULL,
    freight_value REAL NOT NULL,
    total_item_value REAL NOT NULL,

    -- Constraints
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (seller_key) REFERENCES dim_seller(seller_key),
    FOREIGN KEY (order_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (shipping_limit_date_key) REFERENCES dim_date(date_key)
);


CREATE TABLE fact_orders (
    order_key SERIAL PRIMARY KEY,

    order_id TEXT NOT NULL UNIQUE,

    customer_key INT NOT NULL,

    purchase_date_key INT NOT NULL,
    approval_date_key INT,
    delivery_date_key INT,
    estimated_delivery_date_key INT,
	order_status_key INT NOT NULL,


    order_count INT DEFAULT 1,
    delivery_days INT,
    approval_delay INT,

    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (purchase_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (approval_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (delivery_date_key) REFERENCES dim_date(date_key),
	FOREIGN KEY (order_status_key) REFERENCES dim_order_status(order_status_key),
    FOREIGN KEY (estimated_delivery_date_key) REFERENCES dim_date(date_key)
);


CREATE TABLE fact_payments (
    payment_key SERIAL PRIMARY KEY,

    order_id TEXT NOT NULL,

    payment_type_key INT NOT NULL,

    payment_value REAL NOT NULL,
    payment_installments INT,

    FOREIGN KEY (payment_type_key) REFERENCES dim_payment_type(payment_type_key)
);


CREATE TABLE fact_reviews (
    review_key SERIAL PRIMARY KEY,

    order_id TEXT NOT NULL,

    review_date_key INT NOT NULL,
	review_dim_key INT,

    review_score INT,

    FOREIGN KEY (review_date_key) REFERENCES dim_date(date_key),
	FOREIGN KEY (review_dim_key) REFERENCES dim_review(review_dim_key)
);


CREATE TABLE fact_leads_funnel (
    lead_fact_key SERIAL PRIMARY KEY,

    lead_key INT NOT NULL,
    seller_key INT,

    first_contact_date_key INT NOT NULL,
    won_date_key INT,

    conversion_flag INT,

    declared_monthly_revenue REAL,
    declared_product_catalog_size REAL,

    FOREIGN KEY (lead_key) REFERENCES dim_lead(lead_key),
    FOREIGN KEY (seller_key) REFERENCES dim_seller(seller_key),
    FOREIGN KEY (first_contact_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (won_date_key) REFERENCES dim_date(date_key)
);


INSERT INTO dim_date (date_key, full_date, day, month, year, quarter, weekday, is_weekend)
SELECT 
    to_char(d, 'YYYYMMDD')::INT AS date_key,
    d::DATE AS full_date,
    extract(day from d) AS day,
    extract(month from d) AS month,
    extract(year from d) AS year,
    extract(quarter from d) AS quarter,
    extract(isodow from d) AS weekday,
    CASE WHEN extract(isodow from d) IN (6, 7) THEN TRUE ELSE FALSE END AS is_weekend
FROM generate_series('2016-01-01'::DATE, '2028-12-31'::DATE, '1 day'::interval) d;


INSERT INTO dim_date (date_key, full_date, day, month, year, quarter, weekday, is_weekend)
VALUES (-1, '1900-01-01', 0, 0, 0, 0, 0, FALSE);