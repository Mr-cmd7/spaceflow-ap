"""
Компоненты для работы с помещениями
"""
import streamlit as st
from demo.api_client import SpaceFlowClient

def render_rooms_page(client: SpaceFlowClient):
    """Страница со списком помещений"""
    st.title("🏢 Доступные помещения")

    rooms = client.get_rooms(st.session_state.token)

    if not rooms:
        st.info("Помещения не найдены")
    else:
        cols = st.columns(3)
        for i, room in enumerate(rooms):
            with cols[i % 3]:
                with st.container(border=True):
                    st.subheader(room['name'])
                    st.caption(f"ID: {room['id']}")
                    st.markdown(f"**Вместимость:** {room['capacity']} чел.")
                    if room.get('description'):
                        st.markdown(f"**Описание:** {room['description']}")
                    if room.get('equipment'):
                        st.markdown(f"**Оборудование:** {room['equipment']}")
                    if st.button(f"Выбрать", key=f"select_{room['id']}"):
                        st.session_state.selected_room = room
                        st.session_state.page = "Создать бронь"
                        st.rerun()