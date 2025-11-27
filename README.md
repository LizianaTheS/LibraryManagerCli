# LibraryManagerCli

A Command-Line Interface (CLI) for managing library operations including books, copies, members, loans, and reservations. Built with Python, SQLAlchemy, and Marshmallow.

## Features

- Add, update, and list books and copies
- Manage library members
- Track loans and returns
- Handle reservations
- Validation of input data
- CLI prompts for user interaction using Typer

## Installation

```bash
git clone https://github.com/LizianaTheS/LibraryManagerCli.git
cd LibraryManagerCli
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

# Usage
Start the CLI and follow prompts:
```bash
python main.py
```

## Example commands
```bash
# Create a new member
python main.py create-member

# Add a new book
python main.py add-book

# Borrow a copy
python main.py borrow-copy

# Reserve a copy
python main.py reserve-copy
```

# Configuration
Database connection: Configure your SQLAlchemy database URL in the config.py or environment variables.

Migrations: Alembic is used for database migrations.
```bash
alembic upgrade head
```

# Contributing
1. Fork the repository

2. Create a feature branch

3. Commit your changes

4. Submit a pull request
