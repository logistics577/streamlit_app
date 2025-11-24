import streamlit as st
import requests
import json

# === CONFIGURATION ===
API_URL = "https://13.50.213.229/sidekick_chat"  # Your API endpoint
USER_ID = "366"                                  # Fixed user ID
NCREDITS = 1                                     # Fixed credits

# Optional: Disable SSL verification if you're using a self-signed certificate
# (Common for IP-based endpoints like yours)
VERIFY_SSL = False  # Set to True if you have a valid certificate

# App title
st.title("🤖Chatbot")

# Initialize session state for chat history and thread_id
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "default_thread"  # You can change or make it dynamic

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input from user
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare payload
    payload = {
        "user_id": USER_ID,
        "thread_id": st.session_state.thread_id,
        "message": prompt,
        "ncredits": NCREDITS
    }

    # Show a spinner while waiting for API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    headers={
                        "accept": "application/json",
                        "Content-Type": "application/json"
                    },
                    json=payload,
                    verify=VERIFY_SSL,        # Handles self-signed cert warning
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    # Adjust this line based on your actual API response structure
                    # Common keys: "response", "message", "reply", "output", etc.
                    assistant_reply = result.get("response") \
                                      or result.get("reply") \
                                      or result.get("message") \
                                      or json.dumps(result)

                    st.markdown(assistant_reply)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
                else:
                    error_msg = f"API Error {response.status_code}: {response.text}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

            except requests.exceptions.SSLError:
                st.error("SSL Error: The certificate is not trusted. Try hosting with a valid domain or enable 'VERIFY_SSL = True' only with valid cert.")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")