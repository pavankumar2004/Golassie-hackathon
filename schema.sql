--  Payer_Groups Table
CREATE TABLE payer_groups (
    payer_group_id SERIAL PRIMARY KEY,  -- Unique identifier for each payer group 
    payer_group_name VARCHAR(255) NOT NULL UNIQUE  -- Name of the payer group (e.g., "Delta Dental")
);

-- Payers Table
CREATE TABLE payers (
    payer_id SERIAL PRIMARY KEY,           -- Unique identifier for each payer 
    payer_group_id INT NOT NULL,           -- Foreign key to the payer_group table
    payer_name VARCHAR(255) NOT NULL,      -- Name of the payer 
    payer_number VARCHAR(255),             -- Payer number 
    tax_id VARCHAR(255),                   -- Tax ID (optional, can be NULL)
    FOREIGN KEY (payer_group_id) REFERENCES payer_groups(payer_group_id)  -- Foreign key constraint
);

-- Payer_Details Table
CREATE TABLE payer_details (
    payer_detail_id SERIAL PRIMARY KEY,    -- Unique identifier for payer detail 
    payer_id INT NOT NULL,                  -- Foreign key to the payer table
    payer_name VARCHAR(255),                -- Name as it appears in the payment document
    payer_number VARCHAR(255),              -- Payer number as it appears in the document
    tax_id VARCHAR(255),                    -- Tax ID as it appears in the document (can be NULL)
    source_id VARCHAR(255),                 -- Source of the data (e.g., "Vyne")
    FOREIGN KEY (payer_id) REFERENCES payers(payer_id)  -- Foreign key constraint linking to payers
);
