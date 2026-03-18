"""
Компоненты для авторизации
"""
import streamlit as st
from demo.api_client import SpaceFlowClient

def render_login_tab(client: SpaceFlowClient):
    """Отрисовка вкладки входа"""
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Пароль", type="password", key="login_password")

    if st.button("Войти", use_container_width=True):
        token = client.login(email, password)
        if token:
            st.session_state.token = token
            user_info = client.get_current_user(token)
            st.session_state.user_info = user_info
            st.session_state.page = "Помещения"
            st.success("✅ Успешный вход!")
            st.rerun()
        else:
            st.error("❌ Неверный email или пароль")

def render_register_tab(client: SpaceFlowClient):
    """Отрисовка вкладки регистрации"""
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Пароль", type="password", key="reg_password")
    full_name = st.text_input("Полное имя", key="reg_full_name")
    phone = st.text_input("Телефон", key="reg_phone")

    if st.button("Зарегистрироваться", use_container_width=True):
        response = client.register(email, password, full_name, phone)
        if response and 'id' in response:
            st.success("✅ Регистрация успешна! Теперь войдите в систему.")
        else:
            error_msg = response.get('detail', 'Ошибка регистрации') if response else 'Ошибка подключения'
            st.error(f"❌ {error_msg}")

def render_auth_page(client: SpaceFlowClient):
    """Главная страница авторизации"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("SpaceFlow API")
        st.markdown("### Демонстрационное приложение")
        st.markdown("---")

        tab1, tab2 = st.tabs(["🔑 Вход", "📝 Регистрация"])

        with tab1:
            st.subheader("Вход в систему")
            render_login_tab(client)

        with tab2:
            st.subheader("Регистрация")
            render_register_tab(client)