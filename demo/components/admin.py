"""
Административная панель
"""
import streamlit as st
import pandas as pd
from demo.api_client import SpaceFlowClient
from demo.config import BOOKING_STATUS
from demo.utils.helpers import format_datetime

def render_admin_page(client: SpaceFlowClient):
    """Административная панель"""
    st.title("📊 Все бронирования (админ-панель)")

    bookings = client.get_all_bookings(st.session_state.token)

    if not bookings:
        st.info("Нет бронирований")
    else:
        # Фильтры
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox(
                "Фильтр по статусу",
                ["Все"] + list(BOOKING_STATUS.keys())
            )

        # Таблица броней
        data = []
        for b in bookings:
            if status_filter != "Все" and b['status'] != status_filter:
                continue

            user = b.get('user', {})
            room = b.get('room', {})
            data.append({
                "ID": b['id'],
                "Пользователь": user.get('email', 'Неизвестно'),
                "Помещение": room.get('name', 'Неизвестно'),
                "Начало": format_datetime(b['start_time']),
                "Конец": format_datetime(b['end_time']),
                "Статус": b['status']
            })

        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

        st.divider()

        # Действия с бронированием
        st.subheader("Управление бронированием")
        col1, col2, col3 = st.columns(3)

        with col1:
            booking_id = st.number_input("ID бронирования", min_value=1, step=1, value=1)

        with col2:
            if st.button("✅ Подтвердить", use_container_width=True):
                if client.confirm_booking(st.session_state.token, booking_id):
                    st.success(f"Бронирование {booking_id} подтверждено")
                    st.rerun()
                else:
                    st.error("Ошибка при подтверждении")

        with col3:
            if st.button("❌ Отклонить", use_container_width=True):
                if client.reject_booking(st.session_state.token, booking_id):
                    st.success(f"Бронирование {booking_id} отклонено")
                    st.rerun()
                else:
                    st.error("Ошибка при отклонении")

    if st.button("← Назад"):
        st.session_state.page = "Помещения"
        st.rerun()