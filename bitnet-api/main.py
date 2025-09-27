import datetime
import time
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import torch
import uuid
from datetime import datetime
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer

app = FastAPI()

# Load model and tokenizer at startup
model_id = "microsoft/bitnet-b1.58-2B-4T"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    force_download=True,
)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    max_new_tokens: Optional[int] = 700

class Choice(BaseModel):
    index: int
    message: Dict[str, str]
    finish_reason: str

class ChatResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]

@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completions(request: ChatRequest):
    # Prepare prompt using chat template
    prompt = tokenizer.apply_chat_template(
        [msg.dict() for msg in request.messages],
        tokenize=False,
        add_generation_prompt=True
    )
    chat_input = tokenizer(prompt, return_tensors="pt").to(model.device)
    chat_outputs = model.generate(**chat_input, max_new_tokens=request.max_new_tokens)
    response = tokenizer.decode(
        chat_outputs[0][chat_input['input_ids'].shape[-1]:], 
        skip_special_tokens=True
    )
    # Return response in OpenAI-compatible format
    # return JSONResponse({
    #     "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
    #     "object": "chat.completion",
    #     "created": int(time.time()),
    #     "model": model_id,
    #     "choices": [
    #         {
    #             "index": 0,
    #             "message": {
    #                 "role": "assistant",
    #                 "content": response
    #             },
    #             "finish_reason": "stop"
    #         }
    #     ]
    # })
    chat_response = ChatResponse(
        id=f"chatcmpl-{uuid.uuid4().hex[:12]}",
        object="chat.completion",
        created=int(time.time()),
        model=model_id,
        choices=[
            Choice(
                index=0,
                message={"role": "assistant", "content": response},
                finish_reason="stop"
            )
        ]
    )

    logging.info("ChatResponse: %s", chat_response.json())
    return chat_response

@app.get("/")
def root():
    """Root endpoint with API info"""
    return JSONResponse({
        "message": "OpenAI-Compatible API for Open WebUI",
        "version": "1.0.0",
        "endpoints": {
            "models": "/v1/models",
            "chat": "/v1/chat/completions",
            "health": "/health"
        }
    })

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return JSONResponse({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.get("/v1/models")
def list_models():
    """List available models"""
    return JSONResponse({
        "data": [
            {
                "id": model_id,
                "object": "model",
                "created": int(time.time()),  #  datetime.now().isoformat()
                "owned_by": "microsoft",
                "permission": []
            }
        ]
    })