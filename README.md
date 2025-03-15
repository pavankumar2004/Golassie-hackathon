# Payer Management System

A Flask-based web application for managing healthcare payer information, including payer groups, payers, and payer details.

## Features

- View and manage payer groups
- View and edit payer details
- Fuzzy matching for payer identification
- Database integration with PostgreSQL
- Data extraction and clustering from multiple sources

## Database Schema

![Database ERD](erd.png)

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