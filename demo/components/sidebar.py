"""
Боковая панель навигации
"""
import streamlit as st
from demo.config import API_URL

def render_sidebar():
    """Отрисовка боковой панели"""
    with st.sidebar:
        # Попытка загрузить локальное изображение, если есть, иначе URL
        try:
            st.image("demo/assets/img/logo.png", width=120)
        except:
            st.image("https://img.icons8.com/fluency/96/astronaut-helmet.png", width=80)

        st.title("Дом молодежи")
        st.divider()

        if st.session_state.token and st.session_state.user_info:
            user = st.session_state.user_info
            st.success(f"👤 {user['full_name']}")
            st.caption(f"Роль: {user['role']}")
            st.caption(f"Email: {user['email']}")
            st.divider()

            # Навигация
            if st.button("🏠 Помещения", use_container_width=True):
                st.session_state.page = "Помещения"
                st.rerun()
            if st.button("📅 Создать бронь", use_container_width=True):
                st.session_state.page = "Создать бронь"
                st.rerun()
            if st.button("📋 Мои брони", use_container_width=True):
                st.session_state.page = "Мои брони"
                st.rerun()

            # Админ-панель
            if user.get('role') == 'admin':
                st.divider()
                st.caption("⚙️ Администрирование")
                if st.button("📊 Все брони", use_container_width=True):
                    st.session_state.page = "Все брони"
                    st.rerun()

            st.divider()
            if st.button("🚪 Выйти", use_container_width=True):
                st.session_state.token = None
                st.session_state.user_info = None
                st.session_state.page = "Авторизация"
                st.rerun()
        else:
            st.info("👈 Войдите в систему")
            if st.button("🔑 Авторизация", use_container_width=True):
                st.session_state.page = "Авторизация"
                st.rerun()

        st.divider()
        st.caption(f"🔗 API: {API_URL}")