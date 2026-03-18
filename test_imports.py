print("Проверка импортов...")

try:
    from app.core.config import settings
    print("✅ config.py OK")
except Exception as e:
    print(f"❌ config.py error: {e}")

try:
    from app.core.database import engine, SessionLocal, Base, get_db
    print("✅ database.py OK")
except Exception as e:
    print(f"❌ database.py error: {e}")

try:
    from app.core.security import verify_password, get_password_hash, create_access_token, decode_token
    print("✅ security.py OK")
except Exception as e:
    print(f"❌ security.py error: {e}")

try:
    from app.core.deps import get_current_user, get_current_active_user, require_role
    print("✅ deps.py OK")
except Exception as e:
    print(f"❌ deps.py error: {e}")

print("Проверка завершена!")