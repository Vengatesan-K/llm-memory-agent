MEMORY_EXTRACTION_PROMPT = """
Extract factual statements about the user in JSON format:
{"facts": ["fact1", "fact2"]}

Rules:
1. Only extract personal facts (e.g., "I live in Paris")
2. Ignore opinions/temporary statements
"""

ANSWER_GENERATION_PROMPT = """
Answer using ONLY these memories. If unsure, say "I don't remember".

Memories:
{memories}

Question: {query}
"""
