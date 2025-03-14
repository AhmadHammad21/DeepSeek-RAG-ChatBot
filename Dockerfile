# Use a lightweight Python 3.12 image
FROM python:3.12-alpine

WORKDIR /app

# Install dependencies
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt  

# Copy project files
COPY . .  

# Expose FastAPI port
EXPOSE 8000  

# Run FastAPI
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
