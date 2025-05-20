mkdir -p src/api
cat > src/api/main.py << 'EOF'
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
import logging
import openai

# Carregar variáveis de ambiente
load_dotenv('.env.prod')

# Configurar logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar a API FastAPI
app = FastAPI(
    title="AI Discovery Backend",
    description="Backend para o sistema de chat com IA usando RAG",
    version="0.1.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class ChatMessage(BaseModel):
    role: str = Field(..., description="Papel do remetente (user ou assistant)")
    content: str = Field(..., description="Conteúdo da mensagem")

class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(..., description="Histórico de mensagens")
    objective: str = Field(..., description="Objetivo da conversa")
    max_tokens: int = Field(1000, description="Número máximo de tokens na resposta")

class DocumentReference(BaseModel):
    title: str = Field(..., description="Título do documento")
    snippet: str = Field(..., description="Trecho relevante do documento")
    filename: str = Field(..., description="Nome do arquivo")
    distance: float = Field(..., description="Distância semântica")

class ChatResponse(BaseModel):
    response: str = Field(..., description="Resposta gerada pelo assistente")
    references: list[DocumentReference] = Field(..., description="Referências de documentos")

# Endpoints
@app.get("/")
async def root():
    """Endpoint raiz para verificar se a API está funcionando."""
    return {"status": "online", "message": "AI Discovery Backend API"}

@app.get("/health")
async def health_check():
    """Verificar saúde da API e suas dependências."""
    return {
        "status": "healthy",
        "environment": os.getenv('GOOGLE_CLOUD_PROJECT', 'local')
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Processar mensagem de chat e gerar resposta usando RAG."""
    try:
        # Simulação de resposta para teste inicial
        system_prompt = f"Você é um assistente especializado em discovery de design de produto para o objetivo: {request.objective}"
        
        # Preparar mensagens para o LLM
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Adicionar histórico de mensagens
        for msg in request.messages:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Chamar LLM (OpenAI)
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=0.7
        )
        
        # Extrair resposta
        assistant_response = response.choices[0].message.content
        
        # Simular referências para teste inicial
        references = [
            DocumentReference(
                title="Pesquisa de Usuários",
                snippet="Os usuários indicaram preferência por interfaces personalizadas...",
                filename="pesquisa_usuarios.pdf",
                distance=0.23
            ),
            DocumentReference(
                title="Análise de Mercado",
                snippet="Concorrentes têm adotado abordagens de personalização...",
                filename="analise_mercado.pdf",
                distance=0.35
            )
        ]
        
        return ChatResponse(
            response=assistant_response,
            references=references
        )
    
    except Exception as e:
        logger.error(f"Erro ao processar chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar chat: {str(e)}")

# Iniciar servidor se executado diretamente
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
EOF
