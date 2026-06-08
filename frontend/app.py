import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8002/ask"

st.set_page_config(
    page_title="GlowGuide AI",

    layout="centered"
)

st.title("✨GlowGuide AI")
st.markdown("Your AI skincare + healthy food assistant")
st.divider()

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = 0

if "profile" not in st.session_state:
    st.session_state.profile = {
        "skin_type": "",
        "skin_concern": "",
        "sleep": "",
        "water": "",
        "stress": "",
        "products": ""
    }

if "advice_generated" not in st.session_state:
    st.session_state.advice_generated = False


questions = [
    {
        "key": "skin_type",
        "question": "Hi ✨ What is your skin type?",
        "type": "select",
        "options": ["Oily", "Dry", "Combination", "Sensitive", "Normal"]
    },
    {
        "key": "skin_concern",
        "question": "What is your main skin concern right now?",
        "type": "select",
        "options": ["Acne", "Dryness", "Redness", "Dark spots", "Oily skin", "Irritation"]
    },
    {
        "key": "sleep",
        "question": "How many hours do you usually sleep?",
        "type": "slider",
        "min": 0,
        "max": 12,
        "default": 7
    },
    {
        "key": "water",
        "question": "How much water do you drink daily?",
        "type": "select",
        "options": ["Low", "Moderate", "Good"]
    },
    {
        "key": "stress",
        "question": "What is your stress level?",
        "type": "slider",
        "min": 0,
        "max": 10,
        "default": 5
    },
    {
        "key": "products",
        "question": "What skincare products do you currently use?",
        "type": "text",
        "placeholder": "Example: cleanser, moisturizer, sunscreen..."
    }
]


# -----------------------------
# Display chat history
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"].replace("\n", "  \n"))


# -----------------------------
# Ask profile questions
# -----------------------------
if st.session_state.step < len(questions):
    current_q = questions[st.session_state.step]

    if (
        len(st.session_state.messages) == 0
        or st.session_state.messages[-1]["content"] != current_q["question"]
    ):
        st.session_state.messages.append({
            "role": "assistant",
            "content": current_q["question"]
        })
        st.rerun()

    if current_q["type"] == "select":
        answer = st.selectbox(
            "Choose an option:",
            current_q["options"],
            key=f"input_{current_q['key']}"
        )

    elif current_q["type"] == "slider":
        answer = st.slider(
            "Select value:",
            current_q["min"],
            current_q["max"],
            current_q["default"],
            key=f"input_{current_q['key']}"
        )

    else:
        answer = st.text_area(
            "Type your answer:",
            placeholder=current_q["placeholder"],
            key=f"input_{current_q['key']}"
        )

    if st.button("Next"):
        st.session_state.profile[current_q["key"]] = answer

        st.session_state.messages.append({
            "role": "user",
            "content": str(answer)
        })

        st.session_state.step += 1
        st.rerun()


# -----------------------------
# Generate first personalized advice
# -----------------------------
elif not st.session_state.advice_generated:
    intro_message = "Perfect 🌸 I have your skin profile now. I’ll analyze it and give you personalized advice."

    if (
        len(st.session_state.messages) == 0
        or st.session_state.messages[-1]["content"] != intro_message
    ):
        st.session_state.messages.append({
            "role": "assistant",
            "content": intro_message
        })
        st.rerun()

    if st.button("Generate My Advice"):
        profile = st.session_state.profile

        user_prompt = f"""
You are GlowGuide AI.

Create a personalized skincare and nutrition recommendation based on this profile.

Skin type: {profile["skin_type"]}
Main skin concern: {profile["skin_concern"]}
Sleep hours: {profile["sleep"]}
Water intake: {profile["water"]}
Stress level: {profile["stress"]}
Current skincare products: {profile["products"]}

Rules:
- Give ONLY the final answer.
- Do not explain what the response provides.
- Do not say "this response".
- Do not mention instructions.
- Do not write code.
- Use friendly chatbot language.
- Use short sections with emojis.

Use this format:

✨ Skin insight
[Write a short, friendly summary of the user's skin and what to focus on.]

🧴 Ingredients to focus on
[Name 1–2 ingredients or product types to consider.]

⚠️ What to avoid
[Give a brief warning or avoidance tip.]

🥗 Foods that may support skin
[Recommend skin-supportive foods or drinks.]

💧 Hydration tips
[Give a hydration-related tip.]

🌙 Lifestyle tip
[Give one simple lifestyle habit to support skin health.]
"""

        with st.spinner("GlowGuide AI is thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": user_prompt},
                    timeout=300
                )

                if response.status_code == 200:
                    answer = response.json().get("answer", "").strip()

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                    st.session_state.advice_generated = True
                    st.rerun()

                else:
                    st.error(f"Backend returned an error: {response.status_code}")
                    st.write(response.text)

            except Exception as e:
                st.error(f"❌ Error connecting to backend: {e}")


# -----------------------------
# Follow-up chat after advice
# -----------------------------
else:
    follow_up = st.chat_input("Ask GlowGuide AI a follow-up question...")

    if follow_up:
        st.session_state.messages.append({
            "role": "user",
            "content": follow_up
        })

        with st.chat_message("user"):
            st.markdown(follow_up)

        profile = st.session_state.profile

        follow_up_prompt = f"""
You are GlowGuide AI, a skincare and healthy food assistant.

User profile:
Skin type: {profile["skin_type"]}
Main skin concern: {profile["skin_concern"]}
Sleep hours: {profile["sleep"]}
Water intake: {profile["water"]}
Stress level: {profile["stress"]}
Current skincare products: {profile["products"]}

User follow-up question:
{follow_up}

Rules:
- Answer the follow-up question directly.
- Do not force a full skincare routine.
- Do not use the 6-section format unless the user asks for full advice.
- If the user asks for drinks, suggest drinks only.
- If the user asks for foods, suggest foods only.
- If the user asks for skincare routine, suggest routine only.
- Use the profile only if useful.
- Keep the answer clear, short, and practical.
- Do not explain what the response provides.
- Do not say "this response".
- Do not mention instructions.
- Do not write code.

Answer:
"""

        with st.spinner("GlowGuide AI is typing..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": follow_up_prompt},
                    timeout=300
                )

                if response.status_code == 200:
                    answer = response.json().get("answer", "").strip()
                else:
                    answer = f"Backend error: {response.status_code}"

            except Exception as e:
                answer = f"❌ Error connecting to backend: {e}"

        with st.chat_message("assistant"):
            message_box = st.empty()

            # Split the answer into sentences and show each sentence on its own
            # line. Add a friendly emoji to sentences that don't already include
            # one of the common skin-related emojis.
            import re

            sentences = re.split(r'(?<=[.!?])\s+', answer.strip())
            display_text = ""

            common_emojis = set(list("✨🌸💧🥗🧴⚠️🌙"))

            for sent in sentences:
                s = sent.strip()
                if not s:
                    continue
                # If sentence doesn't already contain a common emoji, append one
                if not any(e in s for e in common_emojis):
                    s = s.rstrip('.!?') + ' ✨'

                display_text += s + "  \n\n"
                message_box.markdown(display_text)
                time.sleep(0.18)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("ℹ️ About")
    st.write("Project: **GlowGuide AI**")
    st.write("Frontend: **Streamlit**")
    st.write("Backend: **FastAPI**")
    st.write("Model: **Hugging Face Qwen**")

    if st.button("Restart Chat"):
        st.session_state.messages = []
        st.session_state.step = 0
        st.session_state.profile = {
            "skin_type": "",
            "skin_concern": "",
            "sleep": "",
            "water": "",
            "stress": "",
            "products": ""
        }
        st.session_state.advice_generated = False
        st.rerun()