#!/bin/bash
ENGINE_BASE_URL=https://engine.wilco.gg
WILCO_ID=620ba777a0cccde6931ad14d
# Read WILCO_ID from .wilco file
#WILCO_ID="`cat .wilco`"
ENGINE_EVENT_ENDPOINT="${ENGINE_BASE_URL}/users/${WILCO_ID}/event"
ENGINE_WILCO_AI_CONFIG="${ENGINE_BASE_URL}/users/${WILCO_ID}/wilcoAiConfig"
CODESPACE_BACKEND_HOST=$(curl -s "${ENGINE_BASE_URL}/api/v1/codespace/backendHost?codespaceName=${CODESPACE_NAME}&portForwarding=${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}" | jq -r '.codespaceBackendHost')
CODESPACE_BACKEND_URL="https://${CODESPACE_BACKEND_HOST}"

# Update engine that codespace started for user
curl -L -X POST "${ENGINE_EVENT_ENDPOINT}" -H "Content-Type: application/json" --data-raw "{ \"event\": \"github_codespace_started\" }"

# Export backend envs when in codespaces
echo "export CODESPACE_BACKEND_HOST=\"${CODESPACE_BACKEND_HOST}\"" >> ~/.bashrc
echo "export CODESPACE_BACKEND_URL=\"${CODESPACE_BACKEND_URL}\"" >> ~/.bashrc
echo "export ENGINE_WILCO_AI_URL=\"${ENGINE_WILCO_AI_CONFIG}\"" >> ~/.bashrc
echo "export CODESPACE_WDS_SOCKET_PORT=443" >> ~/.bashrc

# Build Docker images in the background
echo "Starting Docker image build in the background..."
(
    # Build the application image
    echo "Building application Docker image..."
    docker compose build --parallel &

    # Wait for all background processes to complete
    wait
    echo "✅ Docker images prepared and ready to use!"
) &

# Export welcome prompt in bash:
echo "printf \"\n\n🔒 Secure Info Concierge: Your Personal Security Assistant 🔒\n\"" >> ~/.bashrc
echo "printf \"\n\x1b[31m \x1b[1m👉 Run: \\\`docker compose up\\\` to start the secure info service. 👈\n\n\"" >> ~/.bashrc 