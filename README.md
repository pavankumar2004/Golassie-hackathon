# Payer Management System

A Flask-based web application for managing healthcare payer information, including payer groups, payers, and payer details.

## 🚀 Features

- DB Scan Clustering for Payer Group Clustering
- View and manage payer groups
- View and edit payer details
- Fuzzy matching for payer identification
- Database integration with PostgreSQL
- Data extraction and clustering from multiple sources

## 🏛 Database Schema

### 📌 `payer_groups` Table
Manages payer groups.

| Column Name       | Data Type      | Constraints       | Description |
|-------------------|---------------|------------------|-------------|
| `payer_group_id`  | `SERIAL`      | `PRIMARY KEY`    | Unique ID for each payer group |
| `payer_group_name`| `VARCHAR(255)`| `UNIQUE, NOT NULL`| Name of the payer group |

### 📌 `payers` Table
Stores payer information.

| Column Name      | Data Type      | Constraints       | Description |
|-----------------|---------------|------------------|-------------|
| `payer_id`      | `VARCHAR(255)`| `PRIMARY KEY`    | Unique ID for each payer |
| `payer_group_id`| `INT`         | `FOREIGN KEY`    | References payer_groups(payer_group_id) |
| `payer_name`    | `VARCHAR(255)`| `NOT NULL`       | Name of the payer |

### 📌 `payer_details` Table
Stores additional payer information.

| Column Name      | Data Type      | Constraints    | Description |
|-----------------|---------------|---------------|-------------|
| `payer_detail_id`| `SERIAL`      | `PRIMARY KEY` | Unique ID for each detail record |
| `payer_id`      | `VARCHAR(255)`| `FOREIGN KEY` | References payers(payer_id) |
| `payer_name`    | `VARCHAR(255)`| -             | Payer name in this context |
| `short_name`    | `VARCHAR(100)`| -             | Short/abbreviated name |
| `tax_id`        | `VARCHAR(255)`| -             | Tax identifier |

## 🔗 Entity Relationships

![ER Diagram](erdiagram.png)

## 🛠 Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set up PostgreSQL database
4. Configure environment variables:
```bash
export DATABASE_URL="postgresql://username:password@host:port/dbname"
```
5. Run the insertion scripts one by one
    db.py
    insert_player.py
    inerter_player_details.py

## 🚀 Running the Application

```bash
python app.py
```
## 📁 Project Structure

```
golassie-hackathon/
├── app.py                 # Main Flask application
├── db.py                  # Database connection and setup
├── extract.py            # Data extraction utilities
├── insert_payer.py       # Payer insertion logic
├── insert_payer_details.py # Payer details insertion
├── requirements.txt      # Project dependencies
├── schema.sql           # Database schema
├─ erdiagram.png         # Entity Relationship Diagram
└── templates/
    ├── base.html        # Base template
    ├── home.html        # Home page
    ├── payer_groups.html
    ├── payers.html
    ├── payer_details.html
    ├── payer_detail.html
    ├── edit_payer_detail.html
    ├── add_payer_group.html
    └── hierarchy.html
```
## 📝 API Endpoints

- `GET /payer_groups`: List all payer groups
- `POST /payer_groups/add`: Add new payer group
- `GET /payers`: List all payers
- `GET /payer_details`: View payer details
- `POST /payer_details/edit/<id>`: Edit payer details



## 📦 Dependencies

- Flask 2.0.1
- PostgreSQL (psycopg2-binary 2.9.3)
- pandas 1.4.0
- scikit-learn 1.0.2
- fuzzywuzzy 0.18.0



````
