CREATE TABLE uber_management (
    id SERIAL PRIMARY KEY,
    day DATE NOT NULL,
    weekday VARCHAR(20) NOT NULL,
    kilometer INTEGER NOT NULL,
    balance_kilometer NUMERIC NOT NULL,
    average_comsuption NUMERIC NOT NULL,
    liter_gasoline_value NUMERIC NOT NULL,
    worked_hours NUMERIC NOT NULL,
    prejudice INTEGER NOT NULL,
    receipt_id INTEGER,
    CONSTRAINT fk_receipts
      FOREIGN KEY(receipts_id) 
      REFERENCES uber_management_receipts(id)
);
