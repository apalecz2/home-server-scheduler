# Home Server Scheduler

A containerized, lightweight task scheduler designed for home servers running Debian. It uses Docker, Python, and Cron to automate repetitive tasks, such as polling APIs or managing local database records, without cluttering the host system's crontab. This also aims to keep these tasks organised and provide an easy method of tracking active schedules.

### Project Structure

```
home-server-scheduler/
├── env/
│   └── scheduler.env        # Environment variables (API keys, URLs)
├── jobs/
│   └── youtube-summarizer-poll.py  # Python scripts / tasks
├── logs/
│   └── *.log                # Persistent log output (created at runtime)
├── crontab                  # Task schedule configuration
├── Dockerfile               # Image definition (Python + cron)
├── docker-compose.yml       # Service orchestration
└── requirements.txt         # Python dependencies (requests, etc.)
```

### Quick Start

1. Configure Environment

Create a file at ./env/scheduler.env and add your secrets:

YT_SUMM_URL=https://your-api-endpoint.com

YT_SUMM_API_KEY=your_secret_key

TZ=America/New_York

2. Define the Schedule
    - Edit the crontab file to set your intervals.
    - Note: Always ensure there is a blank newline at the end of the file.
    
3. Deploy
    - Run the following command to build the image and start the service in detached mode:
    - ```docker compose up -d --build```
    
### Technical Implementation

- The Docker-Cron "Bridge"
- Standard Cron does not inherit environment variables from Docker. To bridge this gap, the Dockerfile uses a custom entrypoint:
    1. Dumps Environment: printenv > /etc/environment captures Docker variables.
    2. Sources Variables: The crontab uses . /etc/environment; to load them before executing Python.
    3. Foreground Execution: cron -f keeps the container alive.

- Volumes & Persistence
    - Scripts: The ./jobs folder is mounted to the container. You can update your Python logic on the host without rebuilding the image.
    - Logs: The ./logs folder maps to the container's log directory, allowing you to monitor activity using tail -f logs/youtube-summarizer-poll.log.
    
### Debugging & Maintenance

Manual Trigger

To test a script immediately without waiting for the Cron timer:

```bash
docker exec home-scheduler python /home-server-scheduler/jobs/youtube-summarizer-poll.py
```

Check Environment Variables

To verify that your API keys are correctly loaded inside the container:

```bash
docker exec home-scheduler cat /etc/environment
```

Logs & Permissions

If logs are not appearing, ensure the host directory has the correct permissions:

```bash
sudo chmod -R 777 ./logs
```

### Scalability

To add a new job:

1. Place a new .py script in the /jobs folder.

2. Add a new line to the crontab file.

3. Restart the container: ```docker compose up -d --build```