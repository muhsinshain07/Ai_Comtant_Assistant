import os

from dotenv import load_dotenv
import streamlit as st
from groq import Groq, AuthenticationError

# Load environment variables from .env file if present
load_dotenv()


st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered",
)


CONTENT_TYPES = [
    "Social media post",
    "Blog introduction",
    "Product announcement",
    "Advertisement",
    "Video script",
    "Email newsletter",
]

PLATFORMS = [
    "LinkedIn",
    "Instagram",
    "Facebook",
    "X / Twitter",
    "YouTube",
    "Email",
]

TONES = [
    "Professional",
    "Friendly",
    "Casual",
    "Inspirational",
    "Humorous",
    "Persuasive",
]


def get_groq_api_key(custom_key: str = None):
    """Read the API key from custom input, Streamlit secrets, or an environment variable."""
    if custom_key and custom_key.strip():
        return custom_key.strip()

    # Check environment variable (loaded from .env or system environment)
    env_key = os.getenv("GROQ_API_KEY")
    if env_key and not env_key.startswith("gsk_your_free_groq_api_key"):
        return env_key.strip()

    # Check Streamlit secrets safely
    try:
        if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
            secret_key = st.secrets["GROQ_API_KEY"]
            if secret_key and not secret_key.startswith("gsk_your_free_groq_api_key"):
                return secret_key.strip()
    except Exception:
        pass

    return None


def generate_content(content_type, platform, topic, audience, tone, api_key=None, model="llama-3.3-70b-versatile"):
    """Generate a caption and hashtags with Groq."""
    key = api_key or get_groq_api_key()
    if not key:
        raise ValueError(
            "Groq API Key is missing. Please enter your API key in the sidebar or add GROQ_API_KEY to a .env file."
        )

    client = Groq(api_key=key)

    prompt = f"""
Create one complete piece of content using these requirements:

- Content type: {content_type}
- Platform: {platform}
- Topic: {topic}
- Target audience: {audience}
- Tone: {tone}

Return the answer using exactly this structure:

CAPTION:
[Write the complete, ready-to-publish post or script. Match the platform and tone.]

HASHTAGS:
[Provide 8 to 12 relevant hashtags on one line, each beginning with #.]

Do not add explanations before or after this structure.
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert social media and content marketing writer.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=900,
        )
        return response.choices[0].message.content
    except AuthenticationError:
        raise ValueError("Invalid Groq API key. Please verify your API key and try again.")


# Sidebar for API configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    detected_key = get_groq_api_key()
    user_api_key = st.text_input(
        "Groq API Key",
        value=detected_key if detected_key else "",
        type="password",
        placeholder="gsk_...",
        help="Paste your Groq API key here or define GROQ_API_KEY in your .env file.",
    )
    if not user_api_key:
        st.info("💡 Don't have a Groq key? Get a free one at [Groq Console](https://console.groq.com/keys).")

    selected_model = st.selectbox(
        "Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
        ],
        index=0,
        help="Llama 3.3 70B produces high quality content; 8B is ultra-fast.",
    )

st.title("✍️ AI Content Assistant")
st.write("Create a ready-to-publish post with a caption and relevant hashtags.")

with st.form("content_form"):
    content_type = st.selectbox("Content type", CONTENT_TYPES)
    platform = st.selectbox("Platform", PLATFORMS)
    topic = st.text_input(
        "Topic",
        placeholder="Example: Benefits of remote work for small businesses",
    )
    audience = st.text_input(
        "Target audience",
        placeholder="Example: Startup founders and small business owners",
    )
    tone = st.selectbox("Tone", TONES)
    generate_button = st.form_submit_button("Generate content", type="primary")


if generate_button:
    if not topic.strip() or not audience.strip():
        st.warning("Please enter both a topic and a target audience.")
    else:
        with st.spinner("Writing your content..."):
            try:
                generated_content = generate_content(
                    content_type=content_type,
                    platform=platform,
                    topic=topic.strip(),
                    audience=audience.strip(),
                    tone=tone,
                    api_key=user_api_key,
                    model=selected_model,
                )
                st.session_state["generated_content"] = generated_content
            except ValueError as error:
                st.error(str(error))
            except Exception as error:
                st.error(f"Could not generate content. Please try again. Details: {error}")


if st.session_state.get("generated_content"):
    st.divider()
    st.subheader("Your content")
    st.markdown(st.session_state["generated_content"])
    st.download_button(
        label="Download content as a text file",
        data=st.session_state["generated_content"],
        file_name="generated_content.txt",
        mime="text/plain",
    )


# Allow running directly with `python app.py`
if __name__ == "__main__":
    import streamlit.runtime
    if not streamlit.runtime.exists():
        import sys
        from streamlit.web import cli as stcli
        sys.argv = ["streamlit", "run", __file__]
        sys.exit(stcli.main())
