# MARS
Multi Agent RAG system 

# setup
poetry for project / dependencies management

### FastAPI backend
```
cd mars
poetry install
poetry run mars
```

For pip / venv
```
poetry export -f requirements.txt --without-hashes > requirements.txt
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Vue frontend
```
cd mars/frontend
npm install
npm install vue-router@4
npm run dev
```