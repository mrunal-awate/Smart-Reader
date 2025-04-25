# Use a Python base image
FROM python:3.12-slim

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    # Add necessary dependencies here if required
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app


# Copy the application code into the container
COPY . /app

# Add platform-specific pip install command
RUN if [ "$(uname)" == "Darwin" ]; then pip install --no-cache-dir -r requirements.txt; fi
RUN if [ "$(uname)" == "Linux" ]; then pip install --no-cache-dir -r requirements.txt; fi

# Expose the port the app will run on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
