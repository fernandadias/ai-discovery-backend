#!/bin/bash
# Script para deploy direto do backend no Google Cloud Run

# Configurações
PROJECT_ID="search-ai-booster"
REGION="southamerica-east1"
SERVICE_NAME="ai-discovery-backend"
BUCKET_NAME="discoveryagent"
OPENAI_API_KEY="$OPENAI_API_KEY"

echo "Iniciando deploy do backend no Google Cloud Run"
echo "Projeto: $PROJECT_ID"
echo "Região: $REGION"
echo "Serviço: $SERVICE_NAME"

# Configurar gcloud
echo "Configurando Google Cloud CLI..."
gcloud config set project $PROJECT_ID

# Habilitar APIs necessárias
echo "Habilitando APIs necessárias..."
gcloud services enable cloudbuild.googleapis.com run.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com

# Construir e enviar a imagem
echo "Construindo e enviando imagem..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Realizar o deploy no Cloud Run
echo "Realizando deploy no Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 1Gi \
  --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_BUCKET_NAME=$BUCKET_NAME,OPENAI_API_KEY=$OPENAI_API_KEY

# Obter URL do serviço
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')

echo "Deploy concluído com sucesso!"
echo "Seu backend está disponível em: $SERVICE_URL"
echo $SERVICE_URL > backend_url.txt
