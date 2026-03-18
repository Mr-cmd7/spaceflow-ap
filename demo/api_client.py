"""
Клиент для взаимодействия с SpaceFlow API
"""
import requests
import streamlit as st
from datetime import datetime
from typing import Optional, Dict, Any, List


class SpaceFlowClient:
    """Клиент для работы с API SpaceFlow"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Обработка ответа от API"""
        try:
            return response.json() if response.content else {}
        except:
            return {}

    def _request(self, method: str, endpoint: str, token: Optional[str] = None,
                 json: Optional[Dict] = None) -> Optional[requests.Response]:
        """Базовый метод для выполнения запросов"""
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        url = f"{self.base_url}{endpoint}"

        try:
            if method == "GET":
                return self.session.get(url, headers=headers)
            elif method == "POST":
                return self.session.post(url, headers=headers, json=json)
            elif method == "PUT":
                return self.session.put(url, headers=headers, json=json)
            else:
                st.error(f"Неподдерживаемый метод: {method}")
                return None
        except requests.exceptions.ConnectionError:
            st.error("❌ Не удалось подключиться к серверу. Убедитесь, что бэкенд запущен.")
            return None

    # ===== Аутентификация =====

    def register(self, email: str, password: str, full_name: str, phone: str = "") -> Dict:
        """Регистрация нового пользователя"""
        response = self._request("POST", "/auth/register", json={
            "email": email,
            "password": password,
            "full_name": full_name,
            "phone": phone
        })
        return self._handle_response(response) if response else {}

    def login(self, email: str, password: str) -> Optional[str]:
        """Вход в систему, получение токена"""
        response = self._request("POST", "/auth/login", json={
            "email": email,
            "password": password
        })
        if response and response.status_code == 200:
            data = self._handle_response(response)
            return data.get("access_token")
        return None

    def get_current_user(self, token: str) -> Dict:
        """Получение информации о текущем пользователе"""
        response = self._request("GET", "/auth/me", token=token)
        return self._handle_response(response) if response else {}

    # ===== Помещения =====

    def get_rooms(self, token: str) -> List[Dict]:
        """Получение списка помещений"""
        response = self._request("GET", "/rooms/", token=token)
        if response and response.status_code == 200:
            return self._handle_response(response)
        return []

    # ===== Бронирования =====

    def create_booking(self, token: str, room_id: int, start_time: datetime,
                       end_time: datetime, purpose: str, participants: int) -> Dict:
        """Создание бронирования"""
        response = self._request("POST", "/bookings/", token=token, json={
            "room_id": room_id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "purpose": purpose,
            "participants_count": participants
        })
        return self._handle_response(response) if response else {}

    def get_my_bookings(self, token: str) -> List[Dict]:
        """Получение списка своих бронирований"""
        response = self._request("GET", "/bookings/my", token=token)
        if response and response.status_code == 200:
            return self._handle_response(response)
        return []

    def cancel_booking(self, token: str, booking_id: int) -> bool:
        """Отмена бронирования"""
        response = self._request("PUT", f"/bookings/{booking_id}/cancel", token=token)
        return response is not None and response.status_code == 200

    def cancel_booking_with_details(self, token: str, booking_id: int) -> tuple[bool, str]:
        """
        Отмена бронирования с возвратом статуса и сообщения об ошибке.
        Возвращает (True, "") при успехе, (False, сообщение_об_ошибке) при неудаче.
        """
        response = self._request("PUT", f"/bookings/{booking_id}/cancel", token=token)
        if response is None:
            return False, "Нет ответа от сервера (возможно, сервер не запущен)"
        if response.status_code == 200:
            return True, ""
        try:
            error_detail = response.json().get("detail", f"Ошибка {response.status_code}")
        except:
            error_detail = f"Ошибка {response.status_code}"
        return False, error_detail

    # ===== Администрирование =====

    def get_all_bookings(self, token: str) -> List[Dict]:
        """Получение всех бронирований (только для админа)"""
        response = self._request("GET", "/admin/bookings", token=token)
        if response and response.status_code == 200:
            return self._handle_response(response)
        return []

    def confirm_booking(self, token: str, booking_id: int) -> bool:
        """Подтверждение бронирования (только для админа)"""
        response = self._request("PUT", f"/admin/bookings/{booking_id}/confirm", token=token)
        return response is not None and response.status_code == 200

    def reject_booking(self, token: str, booking_id: int) -> bool:
        """Отклонение бронирования (только для админа)"""
        response = self._request("PUT", f"/admin/bookings/{booking_id}/reject", token=token)
        return response is not None and response.status_code == 200