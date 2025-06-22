pip install --upgrade pip && pip install -r requirements.txt

uvicorn main:app --host 0.0.0.0 --port 8000

http://192.168.1.101:8000