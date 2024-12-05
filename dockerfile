# Stage 1: Build the Vite React app
FROM node:16 AS frontend

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the Flask app
FROM python:3.9-slim AS backend

WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app source code
COPY . ./

# Copy the React build files from the frontend stage
COPY --from=frontend /app/frontend/dist ./frontend/dist

# Expose the port
EXPOSE 8000

# Run the Flask app
CMD ["python", "app.py"]

