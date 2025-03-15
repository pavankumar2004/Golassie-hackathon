# Payer Management System

A Flask-based web application for managing healthcare payer information, including payer groups, payers, and payer details.

## Features

- View and manage payer groups
- View and edit payer details
- Fuzzy matching for payer identification
- Database integration with PostgreSQL
- Data extraction and clustering from multiple sources
- DB Scan Clustering for Payer Group Clustering.

## Database Schema

![Database ERD](erd.png)

## 🏛 Database Schema

### 📌 `payer_groups` Table
Manages payer groups.

| Column Name       | Data Type      | Constraints       | Description |
|-------------------|---------------|------------------|-------------|
| `payer_group_id`  | `SERIAL`       | `PRIMARY KEY`    | Unique ID for each payer group. |
| `payer_group_name` | `VARCHAR(255)` | `UNIQUE, NOT NULL` | Name of the payer group. |

---

### 📌 `payers` Table
Stores payer information.

| Column Name       | Data Type      | Constraints       | Description |
|-------------------|---------------|------------------|-------------|
| `payer_id`       | `SERIAL`       | `PRIMARY KEY`    | Unique ID for each payer. |
| `payer_group_id` | `INT`          | `FOREIGN KEY` (payer_groups) | Links payer to a payer group. |
| `payer_name`     | `VARCHAR(255)` | `NOT NULL`       | Name of the payer. |
| `payer_number`   | `VARCHAR(255)` | `NOT NULL, UNIQUE` | Unique payer number. |
| `tax_id`         | `VARCHAR(255)` | `NULLABLE`       | Optional tax identifier. |

---

### 📌 `payer_details` Table
Stores additional details about each payer.

| Column Name       | Data Type      | Constraints       | Description |
|-------------------|---------------|------------------|-------------|
| `payer_detail_id` | `SERIAL`       | `PRIMARY KEY`    | Unique ID for each payer detail. |
| `payer_id`        | `INT`          | `FOREIGN KEY` (payers) | Links to a payer. |
| `payer_name`      | `VARCHAR(255)` | `NOT NULL`       | Payer name. |
| `payer_number`    | `VARCHAR(255)` | `NOT NULL`       | Payer number. |
| `tax_id`          | `VARCHAR(255)` | `NULLABLE`       | Optional tax ID. |
| `source_id`       | `VARCHAR(255)` | `NULLABLE`       | Source identifier (if applicable). |

---

## 🔗 Relationships
1. **One-to-Many:** Each **payer group** (`payer_groups`) can have multiple **payers** (`payers`).
2. **One-to-Many:** Each **payer** (`payers`) can have multiple **payer details** (`payer_details`).

---

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database using schema.sql

4. Run the application:
```bash
python app.py
```

## Data Processing Pipeline

1. Extract payer data: `python extract.py`
2. Initialize payer groups: `python db.py`
3. Insert payers: `python insert_payer.py`
4. Insert payer details: `python insert_payer_details.py`

## Project Structure

```
.
├── app.py                  # Flask application
├── db.py                   # Database initialization
├── extract.py             # Data extraction script
├── insert_payer.py        # Payer insertion script
├── insert_payer_details.py # Payer details insertion
├── schema.sql             # Database schema
├── requirements.txt       # Project dependencies
└── templates/             # HTML templates
    ├── base.html
    ├── home.html
    ├── payer_groups.html
    └── payer_details.html
```

## Environment Variables

Store your database credentials in a `.env` file:
```
DATABASE_URL=postgresql://username:password@host:port/database
```
