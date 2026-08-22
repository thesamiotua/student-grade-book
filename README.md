# Student Grade Book (CLI + MySQL)

A command-line tool to manage students and their grades, backed by a
MySQL database.

## Features
- Add students
- Log grades per subject for a student
- View a student's grades and their calculated average
- List all students

## Requirements
- Python 3.7+
- MySQL Server
- `mysql-connector-python` package

## Setup

1. Install and start MySQL, then create the database and a dedicated user:
```sql
CREATE DATABASE grade_book;
CREATE USER 'gradebook_user'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON grade_book.* TO 'gradebook_user'@'localhost';
FLUSH PRIVILEGES;
```

2. Load the schema:
```bash
mysql -u gradebook_user -p grade_book < schema.sql
```

3. Set up a Python virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install mysql-connector-python
```

4. Update the `DB_CONFIG` dictionary at the top of `gradebook.py` with your
   own username/password if different from the defaults.

## Usage
```bash
python3 gradebook.py
```

## Project structure
```
student-grade-book/
├── gradebook.py   # main script
├── schema.sql     # database schema
└── README.md
```