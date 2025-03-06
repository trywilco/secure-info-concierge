# SecureInfo Concierge

SecureInfo Concierge is an educational platform simulating a sophisticated financial assistant application. It integrates LLM capabilities with database retrievals, designed to teach secure data handling and interactions.

## Features

- FastAPI backend with RESTful services
- Azure OpenAI integration for intelligent responses
- SQLite database for storing financial data
- JWT-based authentication for secure endpoints
- Minimalist web interface for user interactions
- Dockerized environment for easy deployment

## Quick start

The application runs in a Docker container:

1. Start the application with Docker Compose:

   ```
   docker compose up
   ```

2. Access the application in your web browser on port 8000

3. If you want to login, use the following default credentials:
   - Username: johndoe
   - Password: secret

## Project Structure

- `app/`: Main application directory
  - `api/`: API routes and endpoints
  - `auth/`: Authentication related code
  - `database/`: Database connection and queries
  - `models/`: LLM service implementation
  - `static/`: Static assets (CSS, JavaScript)
  - `templates/`: HTML templates
- `data/`: Directory for storing the SQLite database
- `Dockerfile`: Instructions for building the Docker image
- `docker-compose.yml`: Docker Compose configuration
- `requirements.txt`: Python dependencies