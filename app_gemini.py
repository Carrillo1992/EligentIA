import time
import os
import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY=''
genai.configure(api_key=GOOGLE_API_KEY)

def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

context = [
    {
        "role": "model",
        "parts": [{"text": """
            Eres FIRMSBot, un servicio automatizado de preguntas sobre incendios con la API de la NASA, FIRMS.
            Primero saludas al usuario confirmando el servicio que ofreces, luego preguntas si quiere saber de una región específica o de todo el mundo,
            luego preguntas desde qué fecha quiere saber la información.
            Si te pregunta por un pais o region especifica, responde con los incendios mas importantes.
        """}],
    },
    {
        "role": "model",
        "parts": [{"text": """
            Recuerda que puedes hacer preguntas claras y específicas para ayudar al cliente a tomar decisiones.
            Por ejemplo, puedes preguntar "¿Qué información te gustaría saber? ¿Te gustaría información de una región específica?".
            También puedes ofrecer opciones adicionales, como "Últimos incendios registrados".
            Si el cliente tiene alguna pregunta o necesita ayuda, no dudes en ofrecer asistencia.
            Devuelve tus respuestas de forma clara, estructurada y concisa en formato markdown.
            Usa emoticonos para darle un toque más amigable a la conversación.
            Si no existe la opción que el cliente está buscando, puedes decir "Lo siento, pero podrías repetir la pregunta".
        """}],
    },
]
st.set_page_config(
    page_title="Firewatch🔥",
    layout="wide",
    page_icon="🔥",
)

local_css("style/style.css")

selected = option_menu("Menu",
                    options=["Informe", "Chatbot"],
                    icons=["house" "globe"],
                    default_index=0,
                    orientation="horizontal",
                    styles={"container": {"width": "100%","border": "1px ridge  ","background-color": "#DF760B","primaryColor": "#DF760B"},
                                "icon": {"color": "#F8CD47", "font-size": "20px"}})
if selected == 'Informe':
    st.components.v1.iframe('https://app.fabric.microsoft.com/reportEmbed?reportId=52ab961c-a425-4e27-8dcc-3aeb69b890b4&autoAuth=true&ctid=fff29b6d-f524-4b67-91bd-0189cef1a710', height=1024) 

if selected == 'Chatbot':
    new_chat_id = f'{time.time()}'
    MODEL_ROLE = 'model'
    AI_AVATAR_ICON = '✨'

    
    if 'chat_id' not in st.session_state:
        st.session_state.chat_id = new_chat_id
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'gemini_history' not in st.session_state:
        
        st.session_state.gemini_history = context
    if 'model' not in st.session_state:
        st.session_state.model = genai.GenerativeModel('gemini-pro')
    if 'chat' not in st.session_state:
        st.session_state.chat = st.session_state.model.start_chat(
            history=st.session_state.gemini_history
        )

    
    st.write('# Firewatch Bot 🔥🔥🔥')

    for message in st.session_state.messages:
        with st.chat_message(
            name=message['role'],
            avatar=message.get('avatar'),
        ):
            st.markdown(message['content'])

    if prompt := st.chat_input('Su consulta aquí...'):
        with st.chat_message('user'):
            st.markdown(prompt)
            st.session_state.messages.append({
                'role': 'user',
                'content': prompt,
            })
            st.session_state.gemini_history.append({
                'role': 'user',
                'parts': [{'text': prompt}]
            })
        response = st.session_state.chat.send_message(
            prompt,
            stream=True,
        )
        with st.chat_message(name=MODEL_ROLE, avatar=AI_AVATAR_ICON):
            message_placeholder = st.empty()
            full_response = ''
            for chunk in response:
                for ch in chunk.text.split(' '):
                    full_response += ch + ' '
                    time.sleep(0.05) 
                    message_placeholder.write(full_response + '▌')
            message_placeholder.write(full_response)
        st.session_state.messages.append({
            'role': MODEL_ROLE,
            'content': full_response,
            'avatar': AI_AVATAR_ICON,
        })
        st.session_state.gemini_history.append({
            'role': 'model',
            'parts': [{'text': full_response}]
        })
        st.session_state.chat.history = st.session_state.gemini_history
