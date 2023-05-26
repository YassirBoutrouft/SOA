# Use the base Python image
FROM python:3.9

# Install Tesseract OCR
RUN apt-get update && apt-get install -y tesseract-ocr

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable to include Tesseract executable
ENV PATH="/usr/bin/tesseract:${PATH}"

# Copy the code to the working directory
COPY main.py .

# Set the working directory
WORKDIR /app

# Expose the necessary port
EXPOSE 8000

# Run the command to start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

