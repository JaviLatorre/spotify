# 🚀 Guía de Deployment

Instrucciones para desplegar la web app en múltiples plataformas.

---

## Streamlit Community Cloud (Recomendado — Gratuito)

### Requisitos
- Repositorio público en GitHub
- Cuenta en [share.streamlit.io](https://share.streamlit.io)

### Pasos

1. **Subir código a GitHub**
   ```bash
   git add .
   git commit -m "feat: complete spotify music intelligence app"
   git push origin main
   ```

2. **Configurar secrets en Streamlit Cloud**
   - Ir a [share.streamlit.io](https://share.streamlit.io) → New app
   - Seleccionar el repositorio y rama
   - En *Advanced settings* → *Secrets*, añadir:
   ```toml
   SPOTIFY_CLIENT_ID = "tu_client_id"
   SPOTIFY_CLIENT_SECRET = "tu_client_secret"
   GENIUS_API_TOKEN = "tu_genius_token"
   ```

3. **Configurar archivo de entrada**
   - Main file path: `app/main.py`
   - Python version: 3.11

4. **Deploy**
   - Clic en "Deploy!"
   - URL pública: `https://<app-name>.streamlit.app`

### Troubleshooting
- **ModuleNotFoundError**: Verificar que todos los paquetes estén en `requirements.txt`
- **Credenciales no cargadas**: Los secrets de Streamlit Cloud se mapean a variables de entorno
- **Timeout en NLTK**: La primera ejecución descarga datos NLTK; puede tardar 30-60s

---

## Railway

### Requisitos
- Cuenta en [railway.app](https://railway.app)
- CLI de Railway instalada: `npm install -g @railway/cli`

### Pasos

1. **Login y creación de proyecto**
   ```bash
   railway login
   railway init
   ```

2. **Crear `Procfile` en la raíz**
   ```
   web: streamlit run app/main.py --server.port $PORT --server.address 0.0.0.0
   ```

3. **Configurar variables de entorno**
   ```bash
   railway variables set SPOTIFY_CLIENT_ID=tu_client_id
   railway variables set SPOTIFY_CLIENT_SECRET=tu_client_secret
   railway variables set GENIUS_API_TOKEN=tu_token
   ```

4. **Deploy**
   ```bash
   railway up
   ```

### Variables de entorno requeridas
| Variable | Descripción |
|----------|-------------|
| `SPOTIFY_CLIENT_ID` | Client ID de Spotify Developer |
| `SPOTIFY_CLIENT_SECRET` | Client Secret de Spotify |
| `GENIUS_API_TOKEN` | Token de Genius API (opcional) |
| `PORT` | Puerto (Railway lo setea automáticamente) |

---

## Hugging Face Spaces

### Pasos

1. **Crear Space**
   - Ir a [huggingface.co/spaces](https://huggingface.co/spaces) → New Space
   - SDK: Streamlit
   - Visibilidad: Public

2. **Subir archivos via Git**
   ```bash
   git remote add hf https://huggingface.co/spaces/<username>/<space-name>
   git push hf main
   ```

3. **Configurar secrets**
   - En el Space → Settings → Variables and secrets
   - Añadir `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, etc.

4. **Archivo de configuración** (crear `README.md` en la raíz con frontmatter):
   ```yaml
   ---
   title: Spotify Music Intelligence
   emoji: 🎵
   colorFrom: green
   colorTo: black
   sdk: streamlit
   sdk_version: 1.32.0
   app_file: app/main.py
   pinned: false
   ---
   ```

---

## Render

### Pasos

1. **Conectar repositorio GitHub**
   - [render.com](https://render.com) → New → Web Service
   - Conectar con GitHub, seleccionar repositorio

2. **Configuración del servicio**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app/main.py --server.port $PORT --server.address 0.0.0.0`
   - Environment: Python 3

3. **Variables de entorno**
   - En el dashboard: Environment → Add Environment Variable
   - `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `GENIUS_API_TOKEN`

4. **Deploy**
   - Clic en "Create Web Service"
   - URL: `https://<app-name>.onrender.com`

### Notas
- Plan gratuito de Render hace "spin down" tras 15 min de inactividad
- Primera carga puede tardar 30-60 segundos

---

## Ejecución Local (Desarrollo)

```bash
# 1. Activar entorno virtual
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# 2. Variables de entorno
cp .env.example .env
# Editar .env con credenciales reales

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar app
streamlit run app/main.py

# 5. Ejecutar notebooks
jupyter notebook notebooks/

# 6. Tests
pytest tests/ -v
```

---

## Checklist Pre-Deploy

- [ ] `.env` configurado con credenciales válidas (NO subir al repositorio)
- [ ] `.gitignore` incluye `.env` y `data/cache/`
- [ ] `requirements.txt` actualizado con todas las dependencias
- [ ] `streamlit run app/main.py` funciona sin errores localmente
- [ ] Tests pasan: `pytest tests/`
- [ ] NLTK data descargada (se hace automáticamente en primera ejecución)
