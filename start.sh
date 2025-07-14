
# uvicorn main:app --host 0.0.0.0 --port 8000

# echo "🔁 Installing dependencies..."
# pip install --upgrade pip
# pip install -r requirements.txt

# echo "🚀 Starting app with Gunicorn + Uvicorn worker"
# exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
#!/bin/bash
pip install -r requirements.txt
exec gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
