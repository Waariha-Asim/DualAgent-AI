import streamlit as st
import os
import time
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="DualAgent AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium dark theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a0a2e 50%, #0a0a0f 100%);
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(138, 43, 226, 0.4);
        box-shadow: 0 8px 32px rgba(138, 43, 226, 0.15);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #9b59b6, #8e44ad, #6c3483);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #a78bfa;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 300;
        letter-spacing: 2px;
    }
    
    .tagline {
        font-size: 1.1rem;
        color: #8b5cf6;
        text-align: center;
        font-style: italic;
        margin-bottom: 2rem;
        opacity: 0.8;
    }
    
    .badge-writer {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 0.3rem 1rem;
        border-radius: 20px;
        color: white;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .badge-editor {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        padding: 0.3rem 1rem;
        border-radius: 20px;
        color: white;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .workflow-step {
        text-align: center;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin: 0.5rem 0;
    }
    
    .workflow-arrow {
        font-size: 2rem;
        color: #8b5cf6;
        text-align: center;
        margin: -0.5rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5);
    }
    
    .stTextArea > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        color: white !important;
    }
    
    .stTextArea textarea {
        color: white !important;
        font-size: 1rem !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    .css-1d391kg {
        background: rgba(10, 10, 15, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    .stAlert {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px);
    }
    
    h1, h2, h3, h4 {
        color: #e0e0e0 !important;
    }
    
    .improvement-item {
        padding: 0.5rem 1rem;
        margin: 0.3rem 0;
        background: rgba(139, 92, 246, 0.1);
        border-left: 3px solid #8b5cf6;
        border-radius: 5px;
        color: #c4b5d4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generations' not in st.session_state:
    st.session_state.generations = 0
if 'successful_runs' not in st.session_state:
    st.session_state.successful_runs = 0
if 'topics_processed' not in st.session_state:
    st.session_state.topics_processed = []

# System prompts
WRITER_SYSTEM_PROMPT = """You are Writer Agent, a professional content writer. 
Create a clear, informative, logically structured first draft about the user's topic. 
Focus on relevance, useful explanations, examples, and professional writing. 
Your responsibility is only to create the initial draft. 
Do not critique your own work. Write in a natural, engaging style appropriate for the specified content type and tone."""

EDITOR_SYSTEM_PROMPT = """You are Editor/Critic Agent, an expert content editor. 
Review the Writer Agent's draft and produce an improved final version. 
Improve clarity, structure, grammar, accuracy, flow, professional tone, and remove unnecessary repetition. 
Preserve valuable information. 
Also identify the key improvements made. 
Be specific about what you changed and why."""

# Agent functions
def writer_agent(topic, content_type, tone, length):
    """Writer Agent - Creates initial draft"""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    user_prompt = f"""
    Topic: {topic}
    Content Type: {content_type}
    Tone: {tone}
    Length: {length}
    
    Please create a well-structured {content_type.lower()} about the topic above.
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": WRITER_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    
    return response.choices[0].message.content

def editor_agent(draft):
    """Editor Agent - Reviews and improves draft"""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    user_prompt = f"""
    Please review and improve the following draft:
    
    {draft}
    
    Provide:
    1. The improved version
    2. A list of key improvements you made
    
    Format your response as:
    
    IMPROVED_VERSION:
    [Your improved text here]
    
    IMPROVEMENTS:
    - Improvement 1
    - Improvement 2
    - etc.
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": EDITOR_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5,
        max_tokens=2000
    )
    
    result = response.choices[0].message.content
    
    # Parse the response
    if "IMPROVED_VERSION:" in result and "IMPROVEMENTS:" in result:
        parts = result.split("IMPROVEMENTS:")
        improved_text = parts[0].replace("IMPROVED_VERSION:", "").strip()
        improvements = parts[1].strip()
        
        # Clean up improvements
        improvements_list = []
        for line in improvements.split('\n'):
            line = line.strip()
            if line.startswith('-') or line.startswith('•'):
                improvements_list.append(line.lstrip('-• '))
            elif line and not line.startswith('IMPROVEMENTS'):
                improvements_list.append(line)
        
        improvements_text = '\n'.join([f"• {imp}" for imp in improvements_list if imp])
        return improved_text, improvements_text
    else:
        return result, "- Content reviewed and improved"

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="font-size: 2.5rem; background: linear-gradient(135deg, #9b59b6, #8e44ad); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🤖 DualAgent AI
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 Pipeline Status")
    if st.session_state.generations > 0:
        st.markdown("🟢 **Ready**")
    else:
        st.markdown("⏳ **Waiting**")
    
    st.markdown("---")
    
    st.markdown("### 🤖 Agents")
    st.markdown("✍️ **Writer Agent**")
    st.markdown("🧠 **Editor Agent**")
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Technology")
    st.markdown("- Python 3.10+")
    st.markdown("- Streamlit")
    st.markdown("- Groq API")
    st.markdown("- Llama 3.3 70B")
    
    st.markdown("---")
    
    st.markdown("### 📈 Session Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Generations", st.session_state.generations)
    with col2:
        st.metric("Success Rate", f"{st.session_state.successful_runs}/{st.session_state.generations}")
    
    if st.session_state.topics_processed:
        st.markdown("**Recent Topics:**")
        for topic in st.session_state.topics_processed[-3:]:
            st.markdown(f"- {topic[:30]}...")
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Session", use_container_width=True):
        st.session_state.generations = 0
        st.session_state.successful_runs = 0
        st.session_state.topics_processed = []
        st.rerun()

# Main content
st.markdown('<div class="main-title">🤖 DualAgent AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Multi-Agent Writer & Editor</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">"Two specialized AI agents. One refined result."</div>', unsafe_allow_html=True)

# Workflow visualization
st.markdown("### 🔄 Agent Workflow")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown("""
    <div class="workflow-step">
        <h3 style="color: #a78bfa;">✍️</h3>
        <p style="color: #e0e0e0; font-weight: 600;">WRITER</p>
        <p style="color: #9ca3af; font-size: 0.8rem;">Creates draft</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="workflow-arrow">
        ⬇️
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="workflow-step">
        <h3 style="color: #f093fb;">🧠</h3>
        <p style="color: #e0e0e0; font-weight: 600;">EDITOR</p>
        <p style="color: #9ca3af; font-size: 0.8rem;">Reviews & refines</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="workflow-arrow">
        ⬇️
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="workflow-step">
        <h3 style="color: #34d399;">✨</h3>
        <p style="color: #e0e0e0; font-weight: 600;">FINAL</p>
        <p style="color: #9ca3af; font-size: 0.8rem;">Polished result</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Input Section
st.markdown("### 🚀 Start a New Generation")
st.markdown("Enter a topic for the agents to work on.")

col1, col2 = st.columns([2, 1])

with col1:
    topic = st.text_area(
        "Topic",
        placeholder="How Generative AI is transforming software development",
        height=100,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("#### Content Type")
    content_type = st.selectbox(
        "Content Type",
        ["Article", "LinkedIn Post", "Report", "Explainer"],
        label_visibility="collapsed"
    )
    
    st.markdown("#### Tone")
    tone = st.selectbox(
        "Tone",
        ["Professional", "Educational", "Persuasive"],
        label_visibility="collapsed"
    )
    
    st.markdown("#### Length")
    length = st.selectbox(
        "Length",
        ["Short", "Medium", "Detailed"],
        label_visibility="collapsed"
    )

# Generate button
if st.button("🚀 Run Dual-Agent Pipeline", use_container_width=True):
    if not topic or topic.strip() == "":
        st.error("⚠️ Please enter a topic before generating.")
    else:
        try:
            # Check API key
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                st.error("⚠️ Groq API key not found. Please check your .env file.")
                st.stop()
            
            # Update session stats
            st.session_state.generations += 1
            
            # Writer Agent
            with st.spinner("✍️ Writer Agent is drafting..."):
                writer_output = writer_agent(topic, content_type, tone, length)
                st.success("✅ Writer Agent completed")
            
            # Display Writer output
            st.markdown("---")
            st.markdown("### ✍️ Agent 01 — Writer")
            st.markdown('<span class="badge-writer">INITIAL DRAFT</span>', unsafe_allow_html=True)
            
            with st.expander("📄 View Writer's Draft", expanded=True):
                st.markdown(f"""
                <div class="glass-card">
                    <p style="color: #e0e0e0; line-height: 1.8;">{writer_output}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Editor Agent
            with st.spinner("🧠 Editor Agent is reviewing..."):
                editor_output, improvements = editor_agent(writer_output)
                st.success("✅ Editor Agent completed")
            
            # Display Editor output
            st.markdown("### 🧠 Agent 02 — Editor / Critic")
            st.markdown('<span class="badge-editor">REFINED OUTPUT</span>', unsafe_allow_html=True)
            
            with st.expander("📄 View Editor's Final Version", expanded=True):
                st.markdown(f"""
                <div class="glass-card">
                    <p style="color: #e0e0e0; line-height: 1.8;">{editor_output}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Improvements Section
            st.markdown("### 🔍 What Did the Editor Improve?")
            
            cols = st.columns(2)
            improvements_list = improvements.split('\n')
            for i, imp in enumerate(improvements_list):
                if imp.strip():
                    col = cols[i % 2]
                    with col:
                        st.markdown(f"""
                        <div class="improvement-item">
                            ✅ {imp.strip()}
                        </div>
                        """, unsafe_allow_html=True)
            
            # Before/After Comparison
            st.markdown("### 📊 Draft vs Refined")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### ✍️ Writer Agent — Original Draft")
                with st.container():
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 10px; border-left: 3px solid #667eea; max-height: 300px; overflow-y: auto;">
                        <p style="color: #c4b5d4; font-size: 0.9rem; line-height: 1.6;">{writer_output[:500]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### 🧠 Editor Agent — Final Draft")
                with st.container():
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 10px; border-left: 3px solid #f093fb; max-height: 300px; overflow-y: auto;">
                        <p style="color: #c4b5d4; font-size: 0.9rem; line-height: 1.6;">{editor_output[:500]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Update session stats
            st.session_state.successful_runs += 1
            st.session_state.topics_processed.append(topic[:50])
            
            st.markdown("---")
            st.success("✨ Dual-agent pipeline completed successfully!")
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 1rem 0; font-size: 0.8rem;">
    Built with Python, Streamlit, and Groq API • Multi-Agent AI System
</div>
""", unsafe_allow_html=True)