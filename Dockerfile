# Use a specific, secure Python image
FROM python:3.12.4-slim

# Install dependencies and security updates
RUN apt-get update && apt-get upgrade -y

# Install necessary Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Set up app and other configurations
COPY . /app
WORKDIR /app

# Expose the application port
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]
