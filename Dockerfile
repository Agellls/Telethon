FROM python:3.11-slim

WORKDIR /app

# Set environment variables for proper logging
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .

# Create downloads directory
RUN mkdir -p downloads

# Run the application
CMD ["python", "main.py"]
