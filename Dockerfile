# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]
