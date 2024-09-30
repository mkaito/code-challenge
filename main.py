from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

from lib.llm import OpenAIClient
from lib.masker import Masker

app = FastAPI()
client = OpenAIClient()


@app.post("/process")
async def process_request(request: Request):
    """
    Mask PII in the prompt and context, then call the LLM with the masked inputs.
    Tokens are unmasked and streamed back as they arrive.
    """
    data = await request.json()
    prompt = data["prompt"]
    context = data["context"]

    masked_prompt, prompt_pii = Masker.mask(prompt)
    masked_context, context_pii = Masker.mask(context)

    async def token_generator():
        async for token in client.call(masked_prompt, masked_context):
            unmasked_token = Masker.unmask(token, prompt_pii + context_pii)
            yield unmasked_token + " "

    return StreamingResponse(token_generator(), media_type="text/plain")
