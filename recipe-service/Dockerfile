# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make port 6002 available to the world outside this container
EXPOSE 6002

# Run app.py when the container launches
CMD ["python", "app.py"]