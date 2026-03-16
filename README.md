# Contrataciones VE — Plataforma Abierta Anticorrupción

Prototipo open-source de transparencia de contratación pública para Venezuela.
Basado en estándares OCDS (Open Contracting Data Standard).

**Autor:** Jesús Alexander León Cordero — Tech Lead | MSc. Ciencias de la Computación
**Licencia código:** [MIT](LICENSE) | **Licencia datos:** [CC BY 4.0](LICENSE-CC-BY-4.0)
**Fecha:** 2026

## Stack
- Backend: Python 3.12 + FastAPI
- Frontend: Next.js 14 (App Router) + TypeScript
- Base de datos: Supabase (PostgreSQL)

## Inicio rápido

### Requisitos
- Python 3.12+
- Node.js 20+
- Cuenta en Supabase (supabase.com)
- Docker (opcional)

### 1. Clonar y configurar variables de entorno

```bash
git clone https://github.com/tu-usuario/contrataciones-ve
cd contrataciones-ve

# Backend
cp backend/.env.example backend/.env
# Editar backend/.env con tus credenciales de Supabase

# Frontend
cp frontend/.env.local.example frontend/.env.local
# Editar frontend/.env.local con la URL del backend
```

### 2. Inicializar la base de datos

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Crear tablas (migraciones Alembic)
alembic upgrade head

# Cargar datos de demostración
python -m app.seed.seed_data
```

### 3. Backend

```bash
cd backend
# (el venv ya fue activado en el paso 2)
uvicorn app.main:app --reload --port 8000
```

API disponible en: http://localhost:8000
Docs interactivos: http://localhost:8000/docs

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

App disponible en: http://localhost:3000

### 5. Con Docker

```bash
docker-compose up --build
```

## Publicar en GitHub y activar CI/CD

### 1. Subir el monorepo a GitHub

```bash
git init
git add .
git commit -m "feat: inicializar monorepo contrataciones-ve"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/contrataciones-ve.git
git push -u origin main
```

Si ya tienes remoto configurado, solo necesitas:

```bash
git add .
git commit -m "chore: actualizar proyecto"
git push
```

### 2. Configurar GitHub Actions

El repositorio incluye workflows en `.github/workflows/`:

- `backend-ci.yml` (lint/import-check backend)
- `frontend-ci.yml` (lint/build frontend)
- `deploy.yml` (plantilla de despliegue)

### 3. Configurar Secrets (si usarás deploy)

En GitHub: `Settings -> Secrets and variables -> Actions`

Secrets sugeridos:

- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SECRET_KEY`
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`
- `RENDER_DEPLOY_HOOK_URL` (si usas Render)

### 4. Estrategia recomendada de despliegue

- Frontend: Vercel (conectado al repo)
- Backend: Render/Railway/Fly.io
- Base de datos: Supabase

### 5. Configuración de Render para este monorepo (backend)

Si Render muestra un error como:

error: invalid local: resolve : lstat /opt/render/project/src/backend/backend: no such file or directory

significa que se está duplicando la carpeta backend en la configuración del servicio.

Usa solo una de estas dos configuraciones (no mezclar):

Opción A (recomendada para este repo):
- Root Directory: backend
- Dockerfile Path: ./Dockerfile
- Docker Build Context Directory: .

Opción B:
- Root Directory: (vacío)
- Dockerfile Path: backend/Dockerfile
- Docker Build Context Directory: backend

Importante:
- No uses Root Directory=backend junto con Dockerfile Path=backend/Dockerfile.
- No uses Root Directory=backend junto con Docker Build Context Directory=backend.
- Cualquiera de esas combinaciones termina en backend/backend y rompe el build.

Con eso, cada push a `main` ejecuta CI automáticamente.

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /api/v1/processes | Listado de procesos de contratación |
| GET | /api/v1/contracts | Listado de contratos |
| GET | /api/v1/suppliers | Listado de proveedores |
| GET | /api/v1/risk/alerts | Alertas de riesgo |
| GET | /api/v1/download/contracts.csv | Descarga masiva CSV |
| GET | /api/v1/download/ocds/releases.json | Exportación OCDS |

## Documentación
Ver `/docs` en el backend para la especificación OpenAPI completa.
