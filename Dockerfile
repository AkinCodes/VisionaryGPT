# Use a full Python 3.9 image (not slim)
FROM python:3.9

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

# Copy the requirements.txt first for better Docker layer caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of your app code
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run the app using uvicorn
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
