# Use the official Python image as the base image
FROM python:3.9-slim

# Copy requirements for the project
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app's code into the container
COPY scripts /app/scripts

# Set the working directory in the container
WORKDIR /app

# Run the Python script when the container starts
CMD ["python", "scripts/main.py"]
