
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    stripe_customer_id VARCHAR(255) UNIQUE NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    last_login_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stripe_webhook_events (
    event_id VARCHAR(255) PRIMARY KEY,
    event_type VARCHAR(255) NOT NULL,
    received_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    product_id VARCHAR(255) PRIMARY KEY,
    internal_name VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    active BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE prices (
    price_id VARCHAR(255) PRIMARY KEY,
    currency VARCHAR(3) NOT NULL,
    unit_amount INT NOT NULL, -- cents for USD
    recurring_interval VARCHAR(255),
    product_id VARCHAR(255) NOT NULL REFERENCES products(product_id),
    active BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscriptions (
    subscription_id VARCHAR(255) PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id),
    promotion_code_id VARCHAR(255),
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL , 
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE subscription_items (
    subscription_item_id VARCHAR(255) PRIMARY KEY,
    subscription_id VARCHAR(255) REFERENCES subscriptions(subscription_id),
    price_id VARCHAR(255) NOT NULL REFERENCES prices(price_id),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    deleted_at TIMESTAMP
);

CREATE TABLE coupons (
    coupon_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    valid BOOLEAN NOT NULL,
    currency VARCHAR(3),
    amount_off DECIMAL(10, 2),
    percent_off DECIMAL(5, 2),
    duration VARCHAR(255),
    duration_in_months INT,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE promotion_codes (
    promotion_code_id VARCHAR(255) PRIMARY KEY,
    code VARCHAR(255) NOT NULL UNIQUE,
    active BOOLEAN NOT NULL,
    coupon_id VARCHAR(255) NOT NULL REFERENCES coupons(coupon_id),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
