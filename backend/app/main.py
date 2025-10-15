import logging
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.restmessage import DeepChatRequest, DeepChatResponse
from app.conf.config import APP_PORT, FRONT_END
from app.core.agent import Agent

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONT_END],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = Agent()


@app.post("/incoming_message")
async def incoming_message(request: DeepChatRequest) -> Optional[DeepChatResponse]:
    if not request.messages:
        return None

    last_message = request.messages[-1]
    user_text = last_message.text

    response_text = await agent.process_message(user_text)

    return DeepChatResponse(text=response_text)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=APP_PORT, reload=False, log_level="info")
