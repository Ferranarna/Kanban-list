from fastapi import FastAPI
from src.infrastructure.database import engine, Base
from src.infrastructure.adapters.api.routers import project_router, epic_router, task_router

# 1. Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kanban API",
    description="API para gestionar Proyectos, Épicas y Tareas",
    version="1.0.0"
)

# 2. Registrar los routers
app.include_router(project_router.router)
app.include_router(epic_router.router)
app.include_router(task_router.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Kanban. Ve a /docs para ver la documentación."}