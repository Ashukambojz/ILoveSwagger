FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY app.py .
COPY templates/ templates/
COPY scripts/ scripts/
COPY uploads/ uploads/

# Expose the port
EXPOSE 5000

# Run the application with increased timeout and more workers
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
