Service account creation
```bash
gcloud iam service-accounts create ${SA_NAME} \
    --display-name="Service Account for body_weight_assistant"
```

Service account permissions
```bash 
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/aiplatform.user"
```

Deploy to Cloud Run
```bash
adk deploy cloud_run \
  --project=$PROJECT_ID \
  --region=us-central1 \
  --service_name=body-weight-assistant \
  --allow_origins="*" \
  --with_ui \
  . \
  -- \
  --labels=genai-hackathon=body-weight-assistant \
  --service-account=$SERVICE_ACCOUNT
```