import streamlit as st
import ollama  # Assuming ollama is installed and configured locally

# App title and description
st.subheader("Shell Command Explainer & Generator")
st.markdown("""
A helper app for sysadmins shell commands. Choose between:
- **Explain Command**: Explanation of any shell command in English.
- **Generate Command**: Describe and app will generate the command.
""")

# Mode selection
mode = st.radio("Select mode:", ["Explain Command", "Generate Command"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to get explanation from local Ollama model
def get_command_explanation(command):
    prompt = f"""
    Explain the following shell command in simple, plain English suitable for a junior sysadmin.
    Break down each part of the command and describe what it does.
    
    Command: {command}
    
    Explanation:
    """
    
    response = ollama.generate(
        model='deepseek-r1:7b',
        prompt=prompt,
        options={'temperature': 0.3}  # Lower temp for more factual responses
    )
    return response['response']

# Function to generate command from description
def generate_command_from_description(description):
    prompt = f"""
    Based on the following description, provide the most appropriate shell command.
    Include only the command itself, no additional explanation.
    
    Description: {description}
    
    Command:
    """
    
    response = ollama.generate(
        model='deepseek-r1:7b',
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
            explanation = get_command_explanation(prompt)
            st.markdown(explanation)
            st.session_state.messages.append({"role": "assistant", "content": explanation})
        else:  # Generate Command
            command = generate_command_from_description(prompt)
            st.code(command, language="bash")
            st.session_state.messages.append({"role": "assistant", "content": f"```bash\n{command}\n```"})

# Sidebar with examples
with st.sidebar:
    st.header("Steps:")
    
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
    st.markdown("This app uses deepseek-r1:7b running locally via Ollama")
    st.caption("Created by PB")