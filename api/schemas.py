from pydantic import BaseModel

class AgentRequest(BaseModel):
    request_id: str
    user_request: str
