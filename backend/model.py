from transformers import pipeline

print("Loading local Qwen model...")

generator = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct",
    device_map="cpu"
)

def get_answer(question: str) -> str:
    prompt = f"""
You are GlowGuide AI, a friendly skincare, hair care and healthy food assistant.

CRITICAL FORMATTING RULES:
- Provide a thorough and detailed response, but avoid massive block paragraphs.
- Separate your thoughts into readable sentences or bullet points.
- Use a new line for distinct points or explanations to make it easy to read.
- Use relevant emojis generously throughout the response to make it feel warm, engaging, and visually appealing. ✨🌸

CONTENT RULES:
- Answer the user's exact question directly.
- Do NOT force a full skincare routine unless the user asks for it.
- Do NOT always use the same sections.
- Do NOT mention possible cause unless the user asks why.
- Do NOT mention skincare ingredients unless the user asks about products or routine.
- Do NOT repeat the user's question.
- Do NOT write code.
- Give ONLY the final answer.

If the user asks for drinks, suggest drinks only.
If the user asks for foods, suggest foods only.
If the user asks for routine, suggest routine only.
If the user asks for advice, give short personalized advice.

User question:
{question}

Answer:
"""

    result = generator(
        prompt,
        max_new_tokens=200,        
        temperature=0.5,           
        repetition_penalty=1.15,
        return_full_text=False
    )

    answer = result[0]["generated_text"].strip()

    stop_phrases = [
        "[End",
        "End of answer",
        "Let me know",
        "I'm here",
        "User request:",
        "User question:",
        "Answer:"
    ]

    for phrase in stop_phrases:
        if phrase in answer:
            answer = answer.split(phrase)[0].strip()

    return answer