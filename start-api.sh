gunicorn -k uvicorn.workers.UvicornWorker -w 2 -b :8000 app:app  --log-level DEBUG --access-logfile "/srv/logs/api/api.log" --error-logfile "/srv/logs/api/error.log" 2>/srv/logs/api/output.log &
