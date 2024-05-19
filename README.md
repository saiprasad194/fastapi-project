# FastAPI Project

This is a FastAPI project with SQLAlchemy for database interactions and Alembic for migrations.

## Requirements

- Python 3.10
- Git
- Virtualenv (optional but recommended)

## Setup

### Step 1: Clone the repository

```sh
git clone git@github-account1:saiprasad194/fastapi-project.git
cd fastapi-project
```

### Step 2: Create a virtual environment
```sh
# On macOS and Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

### Step 3: Install dependencies
```sh
pip install -r requirements.txt
```

### Step 4: Set up environment variables
Create a .env file in the project root directory and add the necessary environment variables. For example:
Run the Application
```sh
DATABASE_URL=mysql+mysqlconnector://username:password@localhost/dbname
```

### Step 5: Run database migrations
Initialize the database with Alembic:
```sh
alembic upgrade head
```
### Step 6: Run the application
```sh
python3 main.py
```
## Development
### Running the server
To run the server in development mode:
```sh
uvicorn main:app --reload
```
