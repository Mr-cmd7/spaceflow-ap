"""
SpaceFlow API — демонстрационное приложение на Streamlit
Запуск: streamlit run demo/app.py
"""
import sys
import os
# Добавляем корень проекта в путь поиска модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from demo.config import API_URL, APP_TITLE, APP_ICON, APP_LAYOUT
from demo.api_client import SpaceFlowClient
from demo.components.sidebar import render_sidebar
from demo.components.auth import render_auth_page
from demo.components.rooms import render_rooms_page
from demo.components.bookings import render_create_booking_page, render_my_bookings_page
from demo.components.admin import render_admin_page

# Настройка страницы
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=APP_LAYOUT
)

# Инициализация клиента API
@st.cache_resource
def get_api_client():
    return SpaceFlowClient(API_URL)

client = get_api_client()

# Инициализация состояния сессии
if "token" not in st.session_state:
    st.session_state.token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "page" not in st.session_state:
    st.session_state.page = "Авторизация"
if "selected_room" not in st.session_state:
    st.session_state.selected_room = None

# Отрисовка боковой панели
render_sidebar()

# Отрисовка основной страницы в зависимости от состояния
if st.session_state.page == "Авторизация" or not st.session_state.token:
    render_auth_page(client)
elif st.session_state.page == "Помещения":
    render_rooms_page(client)
elif st.session_state.page == "Создать бронь":
    render_create_booking_page(client)
elif st.session_state.page == "Мои брони":
    render_my_bookings_page(client)
elif st.session_state.page == "Все брони" and st.session_state.user_info.get('role') == 'admin':
    render_admin_page(client)