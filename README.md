# Hydroponics API

## Overview

The Hydroponics API is a RESTful backend service designed to manage and monitor hydroponic systems. Built with Django and Django REST Framework, this project provides an interface for:

- **Hydroponic System Management:**  
  Create, retrieve, update, and delete records of hydroponic systems. Each system is associated with a user and can be tracked over time.

- **Sensor Data Logging:**  
  Record and access sensor readings, including pH, temperature, and total dissolved solids (TDS), for each system.

- **User Management:**  
  Manage user accounts with endpoints for authentication and user-specific data, ensuring that only authorized users can modify their own systems.

The API uses Django Filters for query options and drf-spectacular for generating interactive API documentation. PostgreSQL is the database backend.

## First Time Setup
*Note*: This guide is for Ubuntu Linux, if you're on Windows, it's recommended you install [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) and set it up there.

1. **Set Up the Python Virtual Environment**
   - Create a virtual environment:
     ```bash
     python3 -m venv env
     ```
   - *Note:* If you encounter an error, you might need to install the venv module:
     ```bash
     sudo apt install python3.12-venv
     ```

2. **Activate the Virtual Environment**
   - Activate it with:
     ```bash
     source env/bin/activate
     ```

3. **Install Required Packages**
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

4. **Configure Environment Variables**
   - Copy the sample environment file:
     ```bash
     cp .env.sample .env.local
     ```
   - Open `.env.local`, uncomment the lines, and modify the variables as needed.
   - **Essential Variables:** You must always set:
     - `SECRET_KEY`
     - `POSTGRES_USER`
     - `POSTGRES_PASSWORD`

5. **Load Environment Variables**
   - Run the following command to export variables from your `.env.local` file:
     ```bash
     set -a && source .env.local && set +a
     ```

6. **Set Up PostgreSQL**
   - **Option A: Local Installation**
     - Install PostgreSQL:
       ```bash
       sudo apt install postgres
       ```
     - Open the PostgreSQL prompt:
       ```bash
       sudo -u postgres psql
       ```
     - Create the database (replace `<POSTGRES_DB>` with the value from `.env.local`):
       ```sql
       CREATE DATABASE <POSTGRES_DB>;
       ```
     - Create the user (replace `<POSTGRES_USER>` and `<POSTGRES_PASSWORD>` with your values):
       ```sql
       CREATE USER <POSTGRES_USER> WITH PASSWORD '<POSTGRES_PASSWORD>';
       ```
     - Grant the necessary permissions:
       ```sql
       ALTER USER lunasci CREATEDB;
       ALTER DATABASE <POSTGRES_DB> OWNER TO <POSTGRES_USER>;
       ```
   - **Option B: Docker**
     - *TODO*

7. **Apply Database Migrations**
   - Run:
     ```bash
     python manage.py migrate
     ```

8. **Start the Development Server**
   - Run:
     ```bash
     python manage.py runserver
     ```

9. **Creating a Superuser**
  You might want to create the initial superuser.
  Other users can be added from the admin panel.
   - Run:
     ```bash
     python manage.py createsuperuser
     ```

## Development

- **Running the Tests:**  
  ```bash
  python manage.py test
  ```

- **PEP8 Compliance:**  
  After making changes, ensure your code adheres to PEP8 by running:
  ```bash
  pylint --load-plugins pylint_django --django-settings-module=lunasci.settings lunasci/settings.py
  ```