# easy-apply-ats
Easy Apply Application Tracking System

This repository builds upon the original [Automated Bots - Easy Apply Jobs Bot](https://github.com/wodsuz/EasyApplyJobsBot), enhancing the automated process with LinkedIn's Easy Apply feature.  It addresses a few compatibility issues with the former codebase on the Linkedin website.  Most importantly, an issue with the *unfollow* feature is addressed so that you will not return in one hour to find that there are one thousand profiles you follow on Linkedin.  Also, we introduce the recording of company names, position titles, and job descriptions so that you are prepared for your callbacks!  At last, we debut advanced analytics capabilities and a Dockerized Grafana dashboard for real-time application monitoring.  This all comes preconfigured so you are ready to go with applying to every job, and keyword matches are configurable by setting in *config.py*.

<p align="center">
<img src="https://github.com/user-attachments/assets/869a8194-c400-4f7b-bafb-8f5cb10afd5d" />
<!-- <img src="https://github.com/user-attachments/assets/76395cce-bc02-494b-9a0a-5d66ce2b64e8" /> -->
<img src="https://github.com/user-attachments/assets/96d4137b-6e24-46e4-8b77-089972783e9f" />
</p>

## Key Features 💡

- **Automated Applications:** Fully automated submission to LinkedIn Easy Apply jobs based on user-defined preferences.
- **Advanced Data Analytics:** Utilizes dynamic plotting in-depth analysis of application success rates, customizable dashboards in Grafana.
- **Real-Time Monitoring:** Pre-configured and dockerized Grafana application paired with a MySQL database for live tracking and dashboarding of application processes.
- **Cross-Platform Compatibility:** Supports multiple browsers and operating systems.

## Supported Platforms

| Browser | Mac | Windows | Linux-Ubuntu | Note                    |
|---------|-----|---------|--------------|-------------------------|
| Chrome  | ✅  | ✅     | ✅           |  * + bot environment         |
| Firefox  | ✅  | ✅     | ✅           |  * = dashboarding capability       |
| Safari  | ✅  | ✅     | ✅           | *       |
| Edge  | ✅  | ✅     | ✅           |  *       |
| Opera  | ✅  | ✅     | ✅           |  *       |

## Getting Started

### Prerequisites

- Docker
- Python 3.x
- Pip
- Selenium WebDriver

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/alexander-wei/easy-apply-ats/job-application-bot

2. Navigate to the project directory:
    ```bash
    cd job-application-bot

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
        UBUNTU/DEBIAN
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        WINDOWS/MAC
    follow instructions at https://docs.docker.com/desktop/

5. Start the Docker services for Grafana and MySQL with a single command:
    ```bash
    docker-compose up -d

6. Run the bot:
    ```bash
    python linkedin.py
    python linkedin.py -h
    python linkedin.py --hands-free
    python linkedin.py --hands-free --recommended-jobs 
    python linkedin.py --retry

7. Launch the dashboard: this Grafana container comes preconfigured with the MySQL datasource and is already provisioned with a dashboard.  All you need to do is navigate to http://localhost:3000/ in your favorite web browser, and click on the *Job Applications Tracker* dashboard link.

<p align="center">
<img src="https://github.com/user-attachments/assets/5dc81c48-415a-465c-b3b7-3b2b5e053fa0" />
<img src="https://github.com/user-attachments/assets/dc468395-8560-4904-a0da-96c0d2973cdf" />
</p>
    
