## First Time Setup
1. Setup the Python virtual enviroment: `python3 -m venv env`
   - You might need to run `apt install python3.12-venv` beforehand
2. Activate the venv with `source env/bin/activate`
3. Install required packages: `pip install -r requirements.txt`
4. Create your `.env.local` file: `cp .env.sample .env.local`
   - Uncomment the lines and change the variables according to your enviroment
   - The only things you *always* need to set are: 
     - `SECRET_KEY` 
     - `POSTGRES_USER` 
     - `POSTGRES_PASSWORD`
5. Run `set -a && source .env.local && set +a` to set env vars from your `.env.local` file
6. Setup postgres:
   - You can set it up locally:
     - You need to install it: `sudo apt install postgres`
     - Open the psql prompt: `sudo -u postgres psql`
     - Create the database: `CREATE DATABASE <POSTGRES_DB from .env.local>;`
     - Create the user: `CREATE USER <POSTGRES_USER from .env.local> WITH PASSWORD '<POSTGRES_PASSWORD from .env.local>';`
     - Give your user the nessecary permissions: `ALTER DATABASE <POSTGRES_DB> OWNER TO <POSTGRES_USER>;`
   - Or, alternatively, launch it in Docker:
     - **TODO**
7. Apply migrations: `python manage.py migrate`