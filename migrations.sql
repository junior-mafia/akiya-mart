
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







-- CREATE TABLE one_off_purchases (
--     one_off_purchase_id VARCHAR(255) PRIMARY KEY,
--     user_id INT NOT NULL REFERENCES users(user_id),
--     price_id VARCHAR(255) NOT NULL REFERENCES prices(price_id),
--     created_at TIMESTAMP NOT NULL,
--     updated_at TIMESTAMP NOT NULL,
--     deleted_at TIMESTAMP
-- );






-- also record payment_intent
-- payment_intent will store one-off purchases and subscriptions
-- invoices will store subscription payments
-- these records fail until they succeed and then no more events will fire for it
-- events may arrive out of order so we need to handle on conflict


-- CREATE TABLE invoices (
--     invoice_id VARCHAR(255) PRIMARY KEY,
--     subscription_id VARCHAR(255) NOT NULL,
--     currency VARCHAR(3) NOT NULL,
--     amount_due INT NOT NULL, -- cents for USD
--     amount_paid INT, -- cents for USD, might be NULL if the payment failed
--     status VARCHAR(255) NOT NULL,
--     paid_at TIMESTAMP,
--     created_at TIMESTAMP NOT NULL,
--     updated_at TIMESTAMP NOT NULL
-- );

-- CREATE TABLE payment_intents (
--     payment_intent_id VARCHAR(255) PRIMARY KEY,
--     currency VARCHAR(3) NOT NULL,
--     amount_requested INT NOT NULL, -- cents for USD
--     amount_received INT NOT NULL, -- cents for USD
--     invoice_id VARCHAR(255),
--     status VARCHAR(255) NOT NULL,
--     paid_at TIMESTAMP,
--     created_at TIMESTAMP NOT NULL,
--     updated_at TIMESTAMP NOT NULL
-- );