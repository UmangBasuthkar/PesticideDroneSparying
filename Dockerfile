FROM python:2.7

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    python-dev \
    gcc

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
