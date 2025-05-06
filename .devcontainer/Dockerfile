FROM mcr.microsoft.com/devcontainers/python:1.2.4-3.13-bookworm
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install -r requirements.txt
