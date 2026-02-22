# Use the exact Python version we use locally for consistency
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements first, to leverage Docker cache
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application with live reload enabled
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]