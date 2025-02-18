## First Time Setup
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

## Development

- **PEP8 Compliance:**  
  After making changes, ensure your code adheres to PEP8 by running:
  ```bash
  pylint --load-plugins pylint_django --django-settings-module=lunasci.settings lunasci/settings.py
  ```