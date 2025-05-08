#!/usr/bin/env bash
set -e

# install backend deps
poetry install

# Launch FastAPI backend
poetry run uvicorn mars.main:create_app \
  --host 127.0.0.1 \
  --port 8080 \
  --reload \
  --factory &

BACK_PID=$!
echo "Started FastAPI backend with PID $BACK_PID"

# Launch Vite/Vue frontend
cd frontend
npm install
npm run dev > frontend.log 2>&1 &

FRONT_PID=$!
echo "Started Vue frontend with PID $FRONT_PID"

# Wait for both processes if you want 
wait $BACK_PID
wait $FRONT_PID
