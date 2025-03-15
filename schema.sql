-- Payer_Groups Table
CREATE TABLE payer_groups (
    payer_group_id SERIAL PRIMARY KEY,              
    payer_group_name VARCHAR(255) NOT NULL UNIQUE   
);

-- Payers Table
CREATE TABLE payers (
    payer_id VARCHAR(255) PRIMARY KEY,     
    payer_group_id INT NOT NULL,           
    payer_name VARCHAR(255) NOT NULL,                        
    FOREIGN KEY (payer_group_id) REFERENCES payer_groups(payer_group_id)  
);

-- Payer_Details Table
CREATE TABLE payer_details (
    payer_detail_id SERIAL PRIMARY KEY,    
    payer_id VARCHAR(255) NOT NULL,       
    payer_name VARCHAR(255),               
    short_name VARCHAR(100),               
    tax_id VARCHAR(255),                   
    FOREIGN KEY (payer_id) REFERENCES payers(payer_id)  
);
