# Stage 1: Build Stage
FROM python:3.9-alpine as builder

# Install dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev

# Set working directory
WORKDIR /app

# Copy only requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production Stage
FROM python:3.9-alpine

# Set working directory
WORKDIR /app

# Copy built Python dependencies from the build stage
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy your Python script(s)
COPY your_script.py .

# Run your Python script
CMD ["python", "your_script.py"]
