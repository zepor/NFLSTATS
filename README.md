# NFLSTATS Development Environment
This is the NFLSTATS project, designed to provide statistical insights for the NFL.
## THIS APP NEEDS A TON OF WORK 
## 1. PIPELINES FROM SPORTS RADAR APIS FOR LIVE DATA 
## 2. OTHER ADVANCED ANALYTICS DATASOURCES FOR ADDTIONAL ANALYSIS FOR AN AI MODEL
## 3. DATA VISUALIZATION/DISPLAY
## 4. ADDING OTHER SPORTS
## 5. MAKING AI MODELS FOR SPECIFIC GAMES AND THEIR CONFIDENCE INTERVALS IN A PARTICULAR BET
This guide will help you set up the environment using GitHub Codespaces or set it up locally using Docker and Docker Compose. Be aware the application is half built right now. It needs quite a bit of TLC. THis is my first project, feel free to critisize and make recommendations as you see fit!


![system diagram](diagram.png)

## Using GitHub Codespaces

1. **Fork and Clone**: Fork this repository to your GitHub account and then clone it.
2. **Open in Codespaces**: In your GitHub repository, click on the "Code" button and select "Open with Codespaces". This will open the project in a virtual environment with all the dependencies and settings configured.
3. **Run the App**: Once in Codespaces, you can start the backend and frontend services as you would on your local machine.

## Setting Up Locally

1. **Clone the Repository**: If you haven't already, clone this repository to your local machine.

```bash
git clone https://github.com/[your_username]/NFLSTATS.git
cd NFLSTATS

Docker and Docker Compose: Ensure you have Docker and Docker Compose installed on your local machine. If not, you can download them from the official Docker website.

Build and Start Services: Use Docker Compose to build and start the services defined in the docker-compose.yml file.

bash
Copy code
docker-compose up --build
Access the App: Once the services are up and running, you can access the app via your web browser.
Notes
Ensure your Docker environment has enough resources (CPU, RAM) allocated to run all the services smoothly.
If you encounter any issues or have suggestions, please raise an issue on the GitHub repository.
Contributions are always welcome! Feel free to create pull requests with improvements or new features.
csharp
Copy code


You can copy and paste this directly into your markdown file, and it should render as intended on platforms like GitHub.
