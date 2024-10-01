# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Set environment variables
ENV DB_HOST=host
ENV DB_NAME=name
ENV DB_USER=user
ENV DB_PASSWORD=password
ENV TELEGRAM_BOT_TOKEN=bot-token
ENV TELEGRAM_CHAT_ID=-100id

# Expose the port the app runs on
EXPOSE 5000

# Run the Flask application
CMD ["python", "main.py"]
