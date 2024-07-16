CREATE TABLE uber_management_receipts (
    id SERIAL PRIMARY KEY,
    uber_value NUMERIC NOT NULL,
    pop_99_value NUMERIC NOT NULL,
    promotions NUMERIC NOT NULL,
    run_outside NUMERIC NOT NULL
);