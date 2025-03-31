#!/bin/bash

set -e

echo "STARTING PostgreSQL..."

sleep 5

echo "STARTING FASTAPI BACKEND..."

cd /app/app/backend
nohup uvicorn main:app --host 0.0.0.0 --port 8000 --reload > /tmp/backend.log 2>&1 &

echo "STARTING REACT FRONTEND..."

cd /app/app/frontend
export CHOKIDAR_USEPOLLING=true
nohup npm start > /tmp/frontend.log 2>&1 &


echo "ALL SERVICES ARE STARTING. TAILING LOGS..."
tail -f /tmp/backend.log /tmp/frontend.log