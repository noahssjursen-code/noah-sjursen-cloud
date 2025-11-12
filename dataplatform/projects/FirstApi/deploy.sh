#!/bin/bash

# Deploy FirstApi to Google Cloud Run
# Uses source-based deployment (no Dockerfile needed!)

# Configuration
SERVICE_NAME="firstapi"
REGION="us-central1"
PROJECT_ID="noah-sjursen-cloud"

echo "Deploying FirstApi to Cloud Run..."
echo "Service: $SERVICE_NAME"
echo "Region: $REGION"

# Copy reusables into the project for deployment
echo "Copying reusables library..."
cp -r ../reusables .

# Deploy to Cloud Run (source-based deployment)
gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --project $PROJECT_ID \
  --max-instances 10 \
  --memory 256Mi

# Clean up copied reusables
echo "Cleaning up..."
rm -rf reusables

echo "Deployment complete!"
echo "Your API should be available at the URL shown above."

