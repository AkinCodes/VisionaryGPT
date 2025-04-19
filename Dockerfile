# Use Python 3.8 base image
FROM python:3.8

# Avoid prompts during apt install
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for dlib, opencv, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    g++ \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-python-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip early
RUN pip install --upgrade pip

# Install fire explicitly (if needed early for your code)
RUN pip install fire==0.7.0

# Copy the requirements file before installing (for caching benefit)
COPY requirements.txt .

# Install face_recognition_models manually to bypass broken dependency
RUN pip install face_recognition_models==0.1.3

# Install face-recognition, ignoring the broken model version requirement
RUN pip install face-recognition==1.2.3

# Install remaining dependencies from requirements.txt
# Make sure face-recognition and models are removed from this file!
RUN pip install -r requirements.txt

# Copy the rest of your codebase into the container
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run the app using uvicorn
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
