# Start server for development
python3 -m uvicorn src.app:app --reload

# Start server
python3 -m uvicorn src.app:app

# Run flake to check codestyle
flake8 %abs_progect_dir%/src

# Add new requirement
pip install %new requirement name% 

# Create/update requirements.txt by pip 
pip freeze > requirements.txt

# Run App
 python3 -m uvicorn src.app:app
 
# How to start project first
- Create venv with python 3.8 or higher
- install pip 
  
  python get-pip.py

- install pipreqs

  pip install pipreqs
- update requirements.txt

  pipreqs . --force
  
  create .env file in root of project and add variables on it
  DB_USER=%...% 
  DB_PASS=%...% 
  DB_HOST=%...% 
  DB_PORT=%...% 
  DB_NAME=%...% 
  run src/main.py to start server
  to test endpoints run src/test_route.py 

# Generate secrets
openssl rand -hex 32

# Start Database 
docker-compose up