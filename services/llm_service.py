from groq import Groq
from core.config import settings
from typing import AsyncGenerator
import asyncio

client = Groq(api_key=settings.GROQ_API_KEY)

async def stream_response(prompt: str, model: str = "qwen/qwen3-32b") -> AsyncGenerator[bytes, None]:
    # Wrap the synchronous Groq streaming call in a thread executor
    def sync_stream():
        return client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_completion_tokens=4096,
            top_p=0.95,
            stream=True,
        )

    completion = await asyncio.to_thread(sync_stream)

    for chunk in completion:
        text = chunk.choices[0].delta.content
        if text:
            yield text.encode("utf-8")  # StreamingResponse expects bytes