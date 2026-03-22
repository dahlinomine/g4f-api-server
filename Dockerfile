FROM python:3.12-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install g4f with API support
RUN pip install --no-cache-dir \
    g4f[all]==7.3.4 \
    uvicorn[standard] \
    fastapi

# Write startup script
COPY server.py ./server.py

EXPOSE 8080

CMD ["python", "server.py"]
