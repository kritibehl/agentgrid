from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="AgentGrid AI Workflow API")
app.include_router(router)
