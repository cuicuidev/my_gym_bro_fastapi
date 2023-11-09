FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt .

# Install required system packages
RUN apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev && \
    apk add --no-cache libffi-dev libressl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

# Install uvicorn
RUN pip install uvicorn

# Copy your application code into the container
COPY . .

# Expose the port that your application will run on
EXPOSE 8000