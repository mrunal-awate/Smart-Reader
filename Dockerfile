# Use the official Python slim image as a base image
FROM python:3.10-slim

# Install Tesseract OCR and dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get install -y wget && \
    apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files into the container
COPY . /app/

# Expose the port your app will run on
EXPOSE 8080

# Run the Flask app
CMD ["python", "app.py"]
