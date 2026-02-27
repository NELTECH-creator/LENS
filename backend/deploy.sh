#!/bin/bash
# ──────────────────────────────────────────────
# LENS Backend — Deploy to Google Cloud Run
# ──────────────────────────────────────────────
#
# Usage:
#   ./deploy.sh
#
# Prerequisites:
#   - gcloud CLI installed and authenticated
#   - .env file with PROJECT_ID set
#   - Docker (or Cloud Build) available
#
# ──────────────────────────────────────────────

set -euo pipefail

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Configuration
PROJECT_ID="${PROJECT_ID:?Error: PROJECT_ID not set. Create a .env file with PROJECT_ID=your-project-id}"
REGION="${LOCATION:-us-central1}"
SERVICE_NAME="lens-backend"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "╔══════════════════════════════════════════╗"
echo "║   LENS Backend — Cloud Run Deployment    ║"
echo "╠══════════════════════════════════════════╣"
echo "║  Project:  ${PROJECT_ID}"
echo "║  Region:   ${REGION}"
echo "║  Service:  ${SERVICE_NAME}"
echo "╚══════════════════════════════════════════╝"
echo ""

# Step 1: Build container using Cloud Build
echo "▸ Building container image..."
gcloud builds submit \
    --tag "${IMAGE_NAME}" \
    --project "${PROJECT_ID}" \
    --quiet

# Step 2: Deploy to Cloud Run
echo "▸ Deploying to Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
    --image "${IMAGE_NAME}" \
    --region "${REGION}" \
    --project "${PROJECT_ID}" \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars "PROJECT_ID=${PROJECT_ID},LOCATION=${REGION}" \
    --memory 512Mi \
    --cpu 1 \
    --timeout 600 \
    --min-instances 0 \
    --max-instances 5 \
    --quiet

# Step 3: Get the service URL
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" \
    --region "${REGION}" \
    --project "${PROJECT_ID}" \
    --format "value(status.url)")

echo ""
echo "══════════════════════════════════════════"
echo "✓ Deployment complete!"
echo ""
echo "  Service URL:    ${SERVICE_URL}"
echo "  Health check:   ${SERVICE_URL}/health"
echo "  WebSocket:      ${SERVICE_URL/https/wss}/ws"
echo ""
echo "══════════════════════════════════════════"
