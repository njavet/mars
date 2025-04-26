#!/usr/bin/env bash
set -e

# Launch FastAPI backend
poetry run uvicorn mars.main:create_app \
  --host 127.0.0.1 \
  --port 8080 \
  --reload \
  --factory \
  > backend.log 2>&1 &

BACK_PID=$!
echo "Started FastAPI backend with PID $BACK_PID"

# Launch Vite/Vue frontend
cd frontend
npm run dev > frontend.log 2>&1 &

FRONT_PID=$!
echo "Started Vue frontend with PID $FRONT_PID"

# Open Firefox to the frontend
sleep 2
firefox-developer-edition http://localhost:5173 &

# Wait for both processes if you want (optional)
wait $BACK_PID
wait $FRONT_PID
