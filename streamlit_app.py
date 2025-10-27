import streamlit as st
import os
from openai import OpenAI

# Initialize client using your API key from Streamlit Secrets or environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Page Setup ---
st.set_page_config(page_title="AI Assignment Generator", page_icon="🎓", layout="centered")

st.title("🎓 AI-Powered Assignment Generator")
st.write(
    "This app creates personalized assignments based on your **major** and **difficulty level**. "
    "It uses AI to adapt the topic and complexity to each student."
)

# --- User Inputs ---
majors = ["Management", "Marketing", "Accounting", "Cybersecurity", "Information Systems"]
major = st.selectbox("Select your major:", majors)

difficulty = st.slider("Select difficulty (1 = easiest, 5 = hardest):", 1, 5, 3)

st.markdown("---")

# --- Generate Button ---
if st.button("✨ Generate My Assignment"):
    with st.spinner("Generating your personalized assignment..."):
        prompt = f"""
        You are an experienced instructor designing a Management Information Systems assignment.
        Tailor an assignment for a student majoring in {major}, with a difficulty level of {difficulty}/5
        (1 = beginner, 5 = advanced analysis). The assignment should:
        - Relate to real-world {major.lower()} applications of MIS.
        - Include a context or short scenario.
        - Encourage problem-solving and creativity.
        - End with a specific deliverable (e.g., report, dashboard, or proposal).
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert instructional designer and business educator."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400
            )

            assignment_text = response.choices[0].message.content.strip()

            st.success("✅ Assignment generated!")
            st.markdown("### 📝 Your Personalized Assignment")
            st.markdown(assignment_text)

            # Optional download button
            st.download_button(
                label="⬇️ Download Assignment as Text",
                data=assignment_text,
                file_name=f"{major}_assignment_difficulty_{difficulty}.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

else:
    st.info("Select your major and difficulty, then click **Generate My Assignment**.")