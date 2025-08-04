import openai
import os


def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    return openai.embeddings.create(input=text, model=model).data[0].embedding
