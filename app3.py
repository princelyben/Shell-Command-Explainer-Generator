import streamlit as st
import ollama
import re

# App title and description
st.subheader(":violet[Shell Command Explainer & Generator]")
st.markdown("""
A helper app for sysadmins with shell commands. Choose between:
- **Explain Command**: Get a plain English explanation of any shell command.
- **Generate Command**: Describe what you want to do and get the command.
""")

# Mode selection
mode = st.radio("Select mode:", ["Explain Command", "Generate Command"])

# Toggle for showing reasoning (visible in both modes)
show_reasoning = st.toggle("Show detailed reasoning", value=False,
                         help="Toggle on to see the detailed reasoning between <think> tags")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to process content based on toggle state
def process_content(content):
    if not show_reasoning:
        # Remove content between <think> tags
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
    return content.strip()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(process_content(message["content"]), unsafe_allow_html=True)

# Function to get explanation from local Ollama model
def get_command_explanation(command):
    prompt = f"""
    Explain the following shell command in simple, plain English suitable for a junior sysadmin.
    First provide a clear explanation of what the command does.
    Then include detailed technical reasoning between <think> and </think> tags.
    
    Command: {command}
    
    Explanation:
    """
    
    response = ollama.generate(
        model='deepseek-r1:1.5b',
        prompt=prompt,
        options={'temperature': 0.3}
    )
    return response['response']

# Function to generate command from description
def generate_command_from_description(description):
    prompt = f"""
    Based on the following description, provide the most appropriate shell command.
    First provide just the command itself.
    Then include detailed reasoning about why this command works between <think> and </think> tags.
    
    Description: {description}
    
    Response:
    """
    
    response = ollama.generate(
        model='deepseek-r1:1.5b',
        prompt=prompt,
        options={'temperature': 0.3}
    )
    return response['response']

# Chat input and processing
if prompt := st.chat_input("Your input here..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response based on mode
    with st.chat_message("assistant"):
        if mode == "Explain Command":
            response = get_command_explanation(prompt)
        else:
            response = generate_command_from_description(prompt)
        
        processed_response = process_content(response)
        st.markdown(processed_response, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with examples
with st.sidebar:
    st.header(":violet[Steps:]")
    
    if mode == "Explain Command":
        st.markdown("""
        Try explaining commands like:
        - `find /var/log -name "*.log" -mtime +30 -exec rm {} \;`
        - `awk -F':' '{print $1}' /etc/passwd | sort`
        - `tar -czvf backup.tar.gz --exclude="*.tmp" /home/user`
        """)
    else:
        st.markdown("""
        Try asking for commands like:
        - "How do I find files larger than 1GB?"
        - "Show me all running processes sorted by memory usage"
        - "Create a compressed backup excluding temporary files"
        """)
    
    st.markdown("---")
    st.markdown("This app uses deepseek-r1:1.5b running locally via Ollama.")
    st.caption(":blue[Created by PB]")