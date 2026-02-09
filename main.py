from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.database import engine, Base
from src.infrastructure.adapters.api.routers import project_router, epic_router, task_router

# 1. Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kanban API",
    description="API para gestionar Proyectos, Épicas y Tareas",
    version="1.0.0"
)

# --- 2. CONFIGURACIÓN DE CORS ---
# Aquí definimos quién tiene permiso para llamar a la API
origins = [
    "http://localhost:5173",    # Puerto por defecto de Vite (React)
    "http://127.0.0.1:5173",   # A veces el navegador usa la IP en lugar de localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Lista de invitados
    allow_credentials=True,
    allow_methods=["*"],        # Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],        # Permitir todas las cabeceras
)

# 2. Registrar los routers
app.include_router(project_router.router)
app.include_router(epic_router.router)
app.include_router(task_router.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Kanban. Ve a /docs para ver la documentación."}