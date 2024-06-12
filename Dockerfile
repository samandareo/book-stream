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
ENV DB_HOST=aws-db.ctbwu5xukfqx.eu-north-1.rds.amazonaws.com 
ENV DB_NAME=daraja_db
ENV DB_USER=postgres
ENV DB_PASSWORD=hasanboy1403
ENV TELEGRAM_BOT_TOKEN=7319243662:AAFvtYJ-EfGB7-r2DYVTIr70QOhjD6gdjbw
ENV TELEGRAM_CHAT_ID=-1002201681248

# Expose the port the app runs on
EXPOSE 5000

# Run the Flask application
CMD ["python", "main.py"]
