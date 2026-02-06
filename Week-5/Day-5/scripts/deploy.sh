#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "-------------------------------------------------------"
echo "🚀 Starting Full-Stack Capstone Deployment Automation"
echo "-------------------------------------------------------"

# 1. Environment Variable Check
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found! Please create it from .env.example"
    exit 1
fi

# 2. SSL Certificate Management
echo "🔑 Checking SSL Certificates..."
mkdir -p ./nginx/ssl
# Copy certificates from Day-4 if they are missing in Day-5
if [ ! -f ./nginx/ssl/myapp.local.pem ]; then
    echo "📂 Copying mkcert files from Day-4..."
    cp ../Day-4/certs/myapp.local.pem ./nginx/ssl/
    cp ../Day-4/certs/myapp.local-key.pem ./nginx/ssl/
fi

# 3. Cleanup Existing Stack
# This prevents naming conflicts and removes "orphans" from previous runs
echo "🛑 Stopping existing containers and cleaning orphans..."
docker compose -f docker-compose.prod.yml down --remove-orphans

# 4. Build and Launch
# Uses the production-specific compose file
echo "📦 Building images and starting application stack..."
docker compose -f docker-compose.prod.yml --profile fullstack up -d --build

# 5. Cleanup unused Docker resources
echo "🧹 Pruning dangling images to save disk space..."
docker image prune -f

# 6. Verification
echo "⏳ Waiting 15 seconds for Healthchecks to complete..."
sleep 15

echo "-------------------------------------------------------"
echo "📊 Current Container Status:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo "-------------------------------------------------------"

# 7. Final Instructions
echo "✅ Deployment Successful!"
echo "🌐 Access your application at: https://myapp.local"
echo "📝 Note: If this is the first run, refresh the browser to start the visit counter."
echo "-------------------------------------------------------"