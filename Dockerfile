FROM python:3.9

WORKDIR /app

# Install any necessary dependencies
RUN apt-get update && apt-get install -y libxml2-dev libxslt-dev gcc

COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
