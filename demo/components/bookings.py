"""
Компоненты для работы с бронированиями
"""
import streamlit as st
from datetime import datetime, timedelta
from demo.api_client import SpaceFlowClient
from demo.config import BOOKING_STATUS
from demo.utils.helpers import format_datetime, format_date, format_time, get_status_icon

def render_create_booking_page(client: SpaceFlowClient):
    """Страница создания бронирования"""
    st.title("📅 Создание бронирования")

    # Если помещение не выбрано, показываем список для выбора
    if 'selected_room' not in st.session_state or st.session_state.selected_room is None:
        rooms = client.get_rooms(st.session_state.token)
        if not rooms:
            st.warning("Нет доступных помещений")
            if st.button("← Назад"):
                st.session_state.page = "Помещения"
                st.rerun()
            return

        room_options = {room['name']: room for room in rooms}
        selected_name = st.selectbox("Выберите помещение", options=list(room_options.keys()), key="room_selector")

        if selected_name:
            st.session_state.selected_room = room_options[selected_name]
            st.rerun()
        return

    # Если помещение выбрано — показываем форму
    room = st.session_state.selected_room
    st.info(f"**Выбрано помещение:** {room['name']}")

    # Создаём колонки для формы
    col1, col2 = st.columns(2)

    with col1:
        # Виджеты для выбора даты и времени (с явными ключами)
        # По умолчанию предлагаем завтрашний день, но пользователь может выбрать любой
        default_start = datetime.now() + timedelta(days=1)
        default_end = default_start + timedelta(hours=2)

        start_date = st.date_input(
            "Дата начала",
            value=default_start.date(),
            key="start_date"
        )
        start_time = st.time_input(
            "Время начала",
            value=default_start.time(),
            key="start_time"
        )

        end_date = st.date_input(
            "Дата окончания",
            value=default_end.date(),
            key="end_date"
        )
        end_time = st.time_input(
            "Время окончания",
            value=default_end.time(),
            key="end_time"
        )

    with col2:
        purpose = st.text_area(
            "Цель мероприятия",
            placeholder="Например: Встреча команды",
            key="purpose"
        )
        participants = st.number_input(
            "Количество участников",
            min_value=1,
            max_value=room['capacity'],
            value=5,
            key="participants"
        )

        # Объединяем дату и время в единые объекты datetime
        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(end_date, end_time)

        st.markdown("---")
        st.markdown(f"**С:** {start_datetime.strftime('%d.%m.%Y %H:%M')}")
        st.markdown(f"**По:** {end_datetime.strftime('%d.%m.%Y %H:%M')}")

    # Кнопки действий
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Назад", use_container_width=True):
            del st.session_state.selected_room
            st.session_state.page = "Помещения"
            st.rerun()

    with col2:
        if st.button("✅ Забронировать", use_container_width=True, type="primary"):
            # Отладочный вывод (можно будет увидеть в интерфейсе)
            with st.expander("Отладка (данные запроса)"):
                st.write("**start_datetime:**", start_datetime)
                st.write("**end_datetime:**", end_datetime)
                st.write("**start_datetime ISO:**", start_datetime.isoformat())
                st.write("**end_datetime ISO:**", end_datetime.isoformat())
                st.write("**room_id:**", room['id'])
                st.write("**purpose:**", purpose)
                st.write("**participants:**", participants)

            # Отправка запроса
            response = client.create_booking(
                st.session_state.token,
                room['id'],
                start_datetime,
                end_datetime,
                purpose,
                participants
            )

            # Обработка ответа
            if response and 'id' in response:
                st.success("✅ Бронирование создано! Ожидает подтверждения.")
                del st.session_state.selected_room
                st.session_state.page = "Мои брони"
                st.rerun()
            elif response and 'detail' in response:
                # Если сервер вернул сообщение об ошибке
                error_msg = response['detail']
                if 'занято' in error_msg.lower():
                    st.error("❌ Это время уже занято")
                else:
                    st.error(f"❌ Ошибка сервера: {error_msg}")
            else:
                st.error("❌ Неизвестная ошибка при создании бронирования")

def render_my_bookings_page(client: SpaceFlowClient):
    """Страница со списком своих бронирований"""
    st.title("📋 Мои бронирования")

    bookings = client.get_my_bookings(st.session_state.token)

    if not bookings:
        st.info("У вас пока нет бронирований")
    else:
        for booking in bookings:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

                with col1:
                    st.markdown(f"**{booking['room_name']}**")
                    st.caption(f"ID: {booking['id']}")

                with col2:
                    st.markdown(f"📅 {format_date(booking['start_time'])}")
                    st.markdown(f"⏰ {format_time(booking['start_time'])} - {format_time(booking['end_time'])}")

                with col3:
                    status = booking['status']
                    st.markdown(f"**Статус:** {get_status_icon(status, BOOKING_STATUS)}")

                with col4:
                    if status in ['pending', 'confirmed']:
                        if st.button("🚫 Отменить", key=f"cancel_{booking['id']}"):
                            success, error_msg = client.cancel_booking_with_details(st.session_state.token, booking['id'])
                            if success:
                                st.success("Бронирование отменено")
                                st.rerun()
                            else:
                                st.error(f"❌ {error_msg}")

    if st.button("← Назад"):
        st.session_state.page = "Помещения"
        st.rerun()