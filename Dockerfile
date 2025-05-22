# 1. Base image
FROM python:3.9-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements.txt and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# 4. Copy application code
COPY . .

# 5. Expose port
EXPOSE 5000

# 6. Set the run command
CMD ["flask", "run", "--host=0.0.0.0"]
