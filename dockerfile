# Stage 1: Build the Vite React app
FROM node:20 AS frontend

WORKDIR /app/frontend

# Copy package.json and package-lock.json
COPY cryptoboard/frontend/package*.json ./

# Install frontend dependencies
RUN npm install

# Copy the rest of the frontend code
COPY cryptoboard/frontend/ ./

# Build the frontend
RUN npm run build

# Stage 2: Build the Flask app
FROM python:3.9-slim AS backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY cryptoboard/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app source code
COPY cryptoboard/ ./

# Copy the React build files from the frontend stage
COPY --from=frontend /app/frontend/dist ./frontend/dist

# Expose the port
EXPOSE 8000

# Run the Flask app
CMD ["python", "app.py"]
