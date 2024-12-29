import streamlit as st
from transformers import pipeline

# Set the page configuration at the very beginning
st.set_page_config(page_title="Free AI Agent", page_icon="🤖")

# Load a text-generation model from Hugging Face
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="gpt2")  # GPT-2 is free and widely used

text_generator = load_model()

# Streamlit app setup
st.title("Free AI Agent 🤖")
st.write("This AI agent is powered by a free open-source model!")

# Conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("Ask me anything:")

if st.button("Submit"):
    if user_input.strip():
        # Add user input to conversation history
        st.session_state.history.append({"role": "user", "content": user_input})
        
        # Generate a response
        prompt = "\n".join([f"User: {msg['content']}" for msg in st.session_state.history if msg["role"] == "user"])
        response = text_generator(prompt, max_length=150, num_return_sequences=1)[0]["generated_text"]
        
        # Save AI response to history
        st.session_state.history.append({"role": "bot", "content": response[len(prompt):].strip()})
    else:
        st.warning("Please enter a question or command!")

# Display conversation history
st.write("### Conversation History")
for chat in st.session_state.history:
    if chat["role"] == "user":
        st.write(f"**You:** {chat['content']}")
    elif chat["role"] == "bot":
        st.write(f"**AI:** {chat['content']}")

# Footer
st.markdown("---")
st.markdown("**Powered by Hugging Face and Streamlit**")
st.markdown("**Author: Engr Shabir Orakzai**")
