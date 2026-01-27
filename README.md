# 🗄️ Kanban-List Backend (FastAPI + Hexagonal Architecture)

Este es el núcleo (Backend) de la aplicación **Kanban-List**, una herramienta diseñada para la gestión eficiente de tareas. El proyecto ha sido desarrollado siguiendo principios de **Arquitectura Hexagonal (Ports & Adapters)** para garantizar un código mantenible, testeable y desacoplado de la infraestructura.

---

## 🚀 Tecnologías Principales

* **Lenguaje:** Python 3.12+
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Asíncrono y de alto rendimiento)
* **Gestor de Paquetes:** [uv](https://github.com/astral-sh/uv) (Extremadamente rápido, reemplazo de pip/poetry)
* **Base de Datos:** MySQL 8.0 (Encapsulada en Docker)
* **ORM:** SQLAlchemy 2.0
* **Entorno:** WSL2 (Ubuntu) sobre Windows

---

## 🏗️ Arquitectura del Proyecto

El proyecto implementa **Arquitectura Hexagonal**, dividiendo la responsabilidad en tres capas principales:

1.  **Domain:** Contiene los modelos de negocio puros (Entidades) y las reglas de negocio. No depende de ninguna librería externa.
2.  **Application:** Contiene los casos de uso (Lógica de la aplicación) y define las interfaces (puertos) para los repositorios.
3.  **Infrastructure:** Implementaciones técnicas (Adaptadores). Aquí reside la configuración de MySQL, los repositorios de SQLAlchemy y los controladores de la API (FastAPI).

---

## 🛠️ Configuración del Entorno

### Requisitos Previos
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) con integración WSL2 activa.
* [uv](https://astral.sh/uv/) instalado en tu instancia de Ubuntu (WSL).

### Instalación rápida

1.  **Clonar el repositorio:**
    ```bash
    git clone git@github.com:tu-usuario/Kanban-list.git
    cd Kanban-list
    ```

2.  **Levantar la Infraestructura (Docker):**
    Este comando inicia la base de datos MySQL en el puerto **3307** para evitar conflictos con instalaciones locales.
    ```bash
    make up
    ```

3.  **Instalar dependencias:**
    `uv` creará automáticamente un entorno virtual y sincronizará las librerías necesarias.
    ```bash
    uv sync
    ```

4.  **Ejecutar la aplicación:**
    ```bash
    make run
    ```
    La API estará disponible en `http://localhost:8000`.

---

## 📖 Documentación de la API

Una vez que el servidor esté corriendo, puedes acceder a la documentación interactiva generada automáticamente por FastAPI:

* **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📦 Comandos del Makefile

Para agilizar el desarrollo, se incluyen los siguientes comandos:

| Comando | Descripción |
| :--- | :--- |
| `make up` | Levanta el contenedor de MySQL en segundo plano. |
| `make down` | Detiene y elimina los contenedores de la base de datos. |
| `make run` | Inicia el servidor FastAPI con Hot-Reload activo. |
| `make logs` | Visualiza los logs de la base de datos en tiempo real. |

---

## 📧 Contacto y Portfolio

Este proyecto forma parte de mi portfolio personal. Si tienes alguna duda o quieres contactar conmigo:
* **Nombre:** Ferran Arnaus Garcia
* **GitHub:** [@Ferranarna](https://github.com/Ferranarna)
* **Correo:** ferran.arnaus.garcia23@gmail.com