
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
    type VARCHAR(255) NOT NULL, 
    received_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    product_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE prices (
    price_id VARCHAR(255) PRIMARY KEY,
    currency VARCHAR(3) NOT NULL,
    unit_amount INT NOT NULL, -- cents for USD
    recurring_interval VARCHAR(255),
    product_id VARCHAR(255) NOT NULL REFERENCES products(product_id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);







CREATE TABLE subscriptions (
    subscription_id VARCHAR(255) PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id),
    invoice_activated_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cancelled_at TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE subscription_items (
    id SERIAL PRIMARY KEY,
    subscription_id VARCHAR(255) REFERENCES subscriptions(subscription_id),
    price_id VARCHAR(255) NOT NULL REFERENCES prices(price_id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cancelled_at TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);











CREATE TABLE invoices (
    invoice_id VARCHAR(255) PRIMARY KEY,
    subscription_id VARCHAR(255) NOT NULL REFERENCES subscriptions(subscription_id),
    currency VARCHAR(3) NOT NULL,
    amount_due INT NOT NULL, -- cents for USD
    paid_amount INT, -- cents for USD, might be NULL if the payment failed
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);