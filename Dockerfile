# Use a lightweight Python image
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy our script into the container
COPY broken_link_checker.py .

# Run the script; the URL to check should be provided as an argument
ENTRYPOINT ["python", "broken_link_checker.py"]
