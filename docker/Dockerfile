FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    postgresql postgresql-contrib \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

RUN mkdir -p /app/backend /app/frontend /var/lib/postgresql/data

COPY app/backend /app/backend
COPY app/frontend /app/frontend
COPY db/init.sql /docker-entrypoint-initdb.d/init.sql

# Install backend dependencies
RUN pip3 install --no-cache-dir -r /app/backend/requirements.txt
RUN pip3 install --no-cache-dir fastapi uvicorn psycopg2 sqlalchemy

WORKDIR /app/frontend
RUN npm install

#  - 3000 for React frontend
#  - 8000 for FastAPI backend
#  - 5432 for PostgreSQL
EXPOSE 3000 8000 5432

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /app
CMD ["/entrypoint.sh"]
