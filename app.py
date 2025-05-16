import streamlit as st
from openai import OpenAI

# Set your OpenAI key (make sure it's stored securely in secrets)
client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="InstaCaption Copilot", page_icon="📸")

# --- Header
st.title("📸 InstaCaption Copilot")
st.subheader("Write killer Instagram captions in 3 clicks")
st.markdown("Turn any idea into scroll-stopping captions — just type, choose a vibe, and boom.")

# --- Input Section
user_input = st.text_area("What's your post about?", placeholder="E.g. Morning run done!")

tone = st.selectbox("Choose a vibe:", ["Funny", "Motivational", "Luxury", "Minimalist", "Sassy"])

if st.button("✨ Generate Captions"):
    if not user_input.strip():
        st.warning("Please enter an idea or topic first.")
    else:
        # Prompt Template
        prompt = f"""
        You are an Instagram caption assistant.
        Write 3 unique Instagram captions for the following idea:
        “{user_input}”
        Use the {tone} style. Each caption should be short (under 220 characters), attention-grabbing, and written like it belongs in a real IG post. 
        Add 2–3 relevant emojis. Optional: include 3-5 niche hashtags.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You're an assistant that writes Instagram captions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=300,
            )

            captions = response.choices[0].message.content.strip().split("\n")
            st.markdown("### ✍️ Your Captions")
            for i, cap in enumerate(captions):
                if cap.strip():
                    st.markdown(f"""
                    <div style='padding: 1rem; background-color: #f5f5f5; border-radius: 8px; margin-bottom: 0.5rem; font-size: 1rem; line-height: 1.6'>
                    {cap.strip()}
                    </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
