# SecureInfo Concierge

SecureInfo Concierge is an educational platform simulating a sophisticated financial assistant application. It integrates LLM capabilities with database retrievals, designed to teach secure data handling and interactions.

## Features

- FastAPI backend with RESTful services
- Azure OpenAI integration for intelligent responses
- SQLite database for storing financial data
- JWT-based authentication for secure endpoints
- Minimalist web interface for user interactions
- Dockerized environment for easy deployment

## Prerequisites

- Docker and Docker Compose installed on your system
- Git (optional, for cloning the repository)

## Quick Start

1. Clone the repository (or download the source code):

   ```
   git clone <repository-url>
   cd secure-info-concierge
   ```

2. Build and run the application using Docker Compose:

   ```
   docker compose up --build
   ```

3. Access the application in your web browser:

   ```
   http://localhost:8000
   ```

4. Login with the following credentials:
   - Username: johndoe
   - Password: secret

## Environment Variables

The application can be configured using the following environment variables:

- `DATABASE_PATH`: Path to the SQLite database file (default: `data/financial_data.db`)
- `JWT_SECRET_KEY`: Secret key for JWT token generation (default: a predefined key for development)
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI API endpoint URL (e.g., https://your-resource-name.openai.azure.com)
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_DEPLOYMENT`: Your Azure OpenAI deployment name (e.g., "gpt-4o-mini")
- `AZURE_OPENAI_API_VERSION`: Your Azure OpenAI API version (default: "2023-05-15")

You can set these variables in a `.env` file in the project root directory.

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

## Development

The application runs in a Docker container:

1. Start the application with Docker Compose:

   ```
   docker compose up
   ```

2. For rebuilding after changes:

   ```
   docker compose up --build
   ```
