from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

def main():
    
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro") 
    chat = model.start_chat(history=[])

    
    st.set_page_config(page_title="Chatbot")
    st.header("CollegeMitr")

    
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    
    def get_gemini_response(question):
        try:
            response = chat.send_message(question, stream=True)
            return response
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return []

    
    input_text = st.text_input("What can I help you with? ", key="input")
    submit = st.button("Ask")

    if submit and input_text:
        response = get_gemini_response(input_text)
        
        
        st.session_state['chat_history'].append(("You", input_text))

        
        st.subheader("This is what I found related to your search:")
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))

    
    st.subheader("Chat History:")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

if __name__ == "__main__":
    main()
