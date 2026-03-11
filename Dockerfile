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
COPY login.py .
COPY start-northflank.sh .

# Make startup script executable
RUN chmod +x /app/start-northflank.sh

# Create downloads directory
RUN mkdir -p downloads

# Run via startup script untuk better error handling
CMD ["/app/start-northflank.sh"]
