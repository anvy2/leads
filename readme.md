## Steps to run in dev 

1. Install dev-requirements.txt
2. Setup postgres url in either .env or src/conf.py 
3. Run ```alembic upgrade head```
4. Run ```fastapi dev src/api/main.py --port=8080``` from root folder
5. Open localhost:8080/docs to access swagger UI

### NOTE:- for prod use uvicorn instead of fastapi dev server

