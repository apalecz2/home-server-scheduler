FROM python:3.12-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends cron curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home-server-scheduler

# 1. Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy the actual jobs (Good practice even with volumes)
COPY jobs/ ./jobs/

# 3. Setup Cron
COPY crontab /etc/cron.d/scheduler-cron
RUN chmod 0644 /etc/cron.d/scheduler-cron \
    && crontab /etc/cron.d/scheduler-cron

# 4. Create log directory
RUN mkdir -p /var/log/home-server-scheduler

# Start env dump and cron
CMD ["sh", "-c", "printenv > /etc/environment && cron -f"]