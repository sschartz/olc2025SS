import os
import traceback
import streamlit as st

st.set_page_config(page_title="AI Assignment Generator", page_icon="🎓", layout="centered")
st.title("🎓 AI-Powered Assignment Generator")

# --- Detect OpenAI availability safely ---
openai_ok = True
client = None
err_msg = None

try:
    from openai import OpenAI
except Exception as e:
    openai_ok = False
    err_msg = f"OpenAI package not available: {e}"

api_key = os.getenv("OPENAI_API_KEY")

if openai_ok and api_key:
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        openai_ok = False
        err_msg = f"OpenAI client init failed: {e}"

# --- Status badges ---
st.caption(
    f"OpenAI package: {'✅ found' if 'OpenAI' in globals() else '❌ missing'}  ·  "
    f"API key env: {'✅ set' if api_key else '❌ missing'}"
)
if err_msg:
    st.warning(err_msg)

# --- Inputs ---
majors = ["Management", "Marketing", "Accounting", "Cybersecurity", "Information Systems"]
major = st.selectbox("Select your major:", majors)
difficulty = st.slider("Select difficulty (1 = easiest, 5 = hardest):", 1, 5, 3)
st.markdown("---")

# --- Generate button ---
if st.button("✨ Generate My Assignment"):
    # If we can't use OpenAI, fall back to demo text so the app never crashes
    if not (client and api_key):
        st.info("Running in demo mode (no OpenAI).")
        assignment_text = f"""
**Assignment Title:** Information Systems in {major}

**Difficulty Level:** {difficulty}/5

**Scenario:**  
You are a consultant analyzing how technology supports strategic decisions in a {major.lower()} context.  
Identify one organization where MIS improved efficiency or decision-making.

**Deliverable:**  
Write a 300–500 word report including:
- One challenge related to MIS in {major.lower()}.
- One opportunity to enhance {major.lower()} outcomes.
"""
        st.success("✅ Assignment generated (demo mode).")
        st.markdown("### 📝 Your Personalized Assignment")
        st.markdown(assignment_text)
    else:
        with st.spinner("Generating your personalized assignment with OpenAI..."):
            try:
                prompt = f"""
                You are an experienced instructor designing a Management Information Systems assignment.
                Tailor an assignment for a student majoring in {major}, with a difficulty level of {difficulty}/5
                (1 = beginner, 5 = advanced analysis). The assignment should:
                - Relate to real-world {major.lower()} applications of MIS.
                - Include a context or short scenario.
                - Encourage problem-solving and creativity.
                - End with a specific deliverable (e.g., report, dashboard, or proposal).
                """
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an expert instructional designer and business educator."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=400
                )
                assignment_text = resp.choices[0].message.content.strip()
                st.success("✅ Assignment generated!")
                st.markdown("### 📝 Your Personalized Assignment")
                st.markdown(assignment_text)
                st.download_button(
                    "⬇️ Download Assignment as Text",
                    data=assignment_text,
                    file_name=f"{major}_assignment_difficulty_{difficulty}.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error("OpenAI call failed. Showing details for troubleshooting:")
                st.code("".join(traceback.format_exc()))
else:
    st.info("Select your major and difficulty, then click **Generate My Assignment**.")