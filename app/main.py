from fastapi import FastAPI
from app.api import auth, rooms, bookings, admin

app = FastAPI(
    title="SpaceFlow API",
    description="API для бронирования помещений Арт-резиденции Дом Молодёжи",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "SpaceFlow API работает!"}

@app.get("/health")
def health():
    return {"status": "healthy"}