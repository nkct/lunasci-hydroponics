## First Time Setup
1. Setup the Python virtual enviroment: `python3 -m venv env`
 - You might need to run `apt install python3.12-venv` beforehand
2. Activate the venv with `source env/bin/activate`
3. Install required packages: `pip install -r requirements.txt`
4. Create your `.env.local` file: `cp .env.sample .env.local`
 - Uncomment the lines and change the variables according to your enviroment
 - The only things you *always* need to set are: `SECRET_KEY`
5. Run `set -a && source .env.local && set +a` to set env vars from your `.env.local` file