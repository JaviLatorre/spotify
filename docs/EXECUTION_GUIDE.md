# 🚀 GUÍA DE EJECUCIÓN: Claude Code Agents para Spotify Project

## Cómo funcionan los Agents con Claude Code

**Claude Code** es un terminal inteligente que ejecuta comandos y código bajo tu supervisión.

Para este proyecto usaremos **5 agentes especializados** (roles simulados) que harán parte del trabajo cada uno.

---

## 📋 SETUP INICIAL (5 min)

### 1. Abre Claude Code
```
Si estás en claude.ai → busca "Claude Code" en tools/extensions
Si tienes el Desktop App → ya está integrado
```

### 2. Clona o crea el repo
```bash
mkdir spotify-music-intelligence
cd spotify-music-intelligence
git init
```

### 3. Descarga mis archivos
```bash
# Los archivos PROJECT_STRUCTURE.md y MASTER_PROMPTS.md 
# guardalos en la raíz del proyecto
```

---

## 🎯 EJECUCIÓN POR FASES

### FASE 1: Data Foundation (Agent 1)

**Objetivo**: Crear estructura base + APIs funcionando  
**Tiempo**: 2-3 horas  
**Archivos generados**: src/, config.py, spotify_api.py, lyrics_handler.py

#### Paso 1: Prompt de Setup
```
Abre Claude Code y pega EXACTAMENTE esto:

---INICIO---

Actúa como un ingeniero de datos Python especializado en APIs.

Necesito crear un proyecto profesional para análisis musical con Spotify.

Por favor, crea la estructura COMPLETA del proyecto siguiendo esta organización:

```
spotify-music-intelligence/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── spotify_api.py
│   ├── lyrics_handler.py
│   ├── data_processor.py
│   ├── nlp_analyzer.py
│   ├── visualization.py
│   └── utils.py
├── notebooks/
│   ├── 01_spotify_exploration.ipynb
│   └── 02_lyrics_analysis.ipynb
├── app/
│   ├── main.py
│   └── pages/
│       ├── 01_Album_Catalogue.py
│       ├── 02_Audio_Features.py
│       ├── 03_Lyrics_Analysis.py
│       └── 04_Artist_Comparison.py
├── data/
│   ├── cache/
│   └── sample/
├── tests/
│   ├── test_spotify.py
│   ├── test_lyrics.py
│   └── test_analysis.py
├── requirements.txt
├── .env.example
├── README.md
└── deployment.md
```

Requisitos:
1. Crear TODAS las carpetas
2. Crear todos los archivos .py con docstrings de cabecera
3. Crear __init__.py en carpetas que lo necesitan
4. .env.example con variables de entorno
5. .gitignore apropiado

Output esperado:
- Árbol completo funcional
- Todos los archivos listos
- Nada debe faltar

---FIN---
```

**Qué hacer cuando termine:**
- ✅ Verifica que creó todas las carpetas: `ls -la src/`
- ✅ Verifica que los .py tienen docstrings
- ✅ Commit a git: `git add . && git commit -m "Project structure"`

---

#### Paso 2: Implementar Spotify API
```
Abre Claude Code y pega:

---INICIO---

Eres un experto en APIs REST e integración con Spotify.

Necesito implementar src/spotify_api.py

REQUISITOS OBLIGATORIOS:

1. Clase SpotifyHandler con:
   - __init__(client_id, client_secret)
   - get_artist(artist_name) → dict con datos del artista
   - get_artist_albums(artist_id) → list de álbumes
   - get_album_tracks(album_id) → list de tracks con features
   - get_audio_features(track_id) → dict de features
   - get_multiple_artists(names: list) → batch processing

2. Manejo de errores:
   - Try-except en CADA request
   - Custom exceptions: SpotifyAPIError, RateLimitError
   - Logging detallado con logging module

3. Rate limiting:
   - Delays automáticos (0.5s entre requests)
   - Retry con exponential backoff (max 3 reintentos)
   - Cache en JSON local para evitar re-descargas

4. Type hints en TODAS las funciones

5. Docstrings completos (Google style)

Código debe ser:
- Production-ready
- Testeable
- Sin print() (solo logging)
- Modular

Output: src/spotify_api.py completamente funcional

---FIN---
```

**Qué hacer cuando termine:**
- ✅ Mira el código generado: `cat src/spotify_api.py | head -50`
- ✅ Verifica que tiene docstrings y type hints
- ✅ Commit: `git add src/spotify_api.py && git commit -m "Add Spotify API handler"`

---

#### Paso 3: Implementar Lyrics API
```
Abre Claude Code y pega:

---INICIO---

Eres un experto en web scraping y manejo de APIs públicas.

Necesito implementar src/lyrics_handler.py para obtener letras de lyrics.ovh

REQUISITOS OBLIGATORIOS:

1. Clase LyricsHandler:
   - __init__()
   - get_lyrics(artist: str, song: str) → str (letras o None)
   - get_lyrics_batch(songs: list[tuple]) → dict
   - get_lyrics_with_fallback(artist, song) → str

2. Características:
   - API: https://api.lyrics.ovh/v1/{artist}/{song}
   - Manejo de errores robusto (la API falla a menudo)
   - Retry automático con delays
   - Caché local en JSON

3. Text cleaning:
   - Remover caracteres especiales manteniendo palabras
   - Normalizar whitespace
   - Encoding correcto

4. Rate limiting:
   - Delays entre requests (0.5-1s)
   - No blockear la app si la API falla

5. Logging detallado

Output: src/lyrics_handler.py completamente funcional

IMPORTANTE: Debe ser ROBUSTO. La API lyrics.ovh falla frecuentemente.

---FIN---
```

**Verificación:**
- ✅ Test básico en Claude Code:
  ```python
  from src.lyrics_handler import LyricsHandler
  handler = LyricsHandler()
  lyrics = handler.get_lyrics("Radiohead", "Creep")
  print(lyrics[:100] if lyrics else "Not found")
  ```

---

#### Paso 4: Config y Utils
```
Abre Claude Code:

---INICIO---

Implementa:

1. src/config.py con:
   - SPOTIFY_CLIENT_ID (env var)
   - SPOTIFY_CLIENT_SECRET (env var)
   - Timeouts, retries, batch sizes
   - Paths de datos
   - Logging config

2. src/utils.py con:
   - normalize_text(text) → str
   - batch_processor(items, batch_size) → generator
   - safe_json_load(path) → dict
   - safe_json_dump(data, path) → None
   - retry decorator
   - timing decorator
   - get_logger(name) → logger

Código limpio, docstrings, type hints.

---FIN---
```

---

### FASE 2: Analysis & NLP (Agent 2)

**Objetivo**: Análisis de datos + procesamiento de letras  
**Tiempo**: 3-4 horas  
**Archivos**: data_processor.py, nlp_analyzer.py

#### Paso 5: Album Filtering
```
Abre Claude Code:

---INICIO---

Eres un experto en análisis de datos y filtrado inteligente.

Necesito filtrar SOLO álbumes de estudio de Spotify.

CONTEXTO:
- Spotify devuelve: album, single, compilation, live, EP, remix, etc
- Solo quiero álbumes de ESTUDIO
- Esto es un requisito crítico (2 puntos de la práctica)

REQUISITOS OBLIGATORIOS:

1. Función filter_studio_albums(albums_df) → pd.DataFrame

2. Criterios:
   - album_type == "album" (Spotify API field)
   - Excluir por palabras clave: "live", "compilation", "reissue", 
     "deluxe", "edition", "remix", "instrumental"
   - Excluir duplicados (mismo nombre, año diferente)
   - Excluir EPs (< 5 tracks usualmente)

3. Heurísticas:
   - Si nombre contiene "remaster" + año diferente → CONSIDERAR (no excluir)
   - Si mismo nombre + año = DEDUPLICAR
   - track_count < 4 → probablemente no es estudio
   
4. Output:
   - DataFrame limpio
   - Log detallado de qué se excluyó
   - Report de confianza

5. Validación:
   - Test con Radiohead, Beatles, otros artistas conocidos
   - Comparar con Wikipedia

Ejemplo:
- Radiohead: "OK Computer", "Kid A", "In Rainbows" = Sí
- Radiohead: "OK Computer - Remastered 2009", "Greatest Hits" = No

---FIN---
```

---

#### Paso 6: NLP Pipeline
```
Abre Claude Code:

---INICIO---

Eres un experto en NLP y procesamiento de texto.

Necesito un pipeline NLP completo para análisis de letras.

Implementa src/nlp_analyzer.py

REQUISITOS:

1. Clase LyricsAnalyzer:
   - clean_text(text) → str limpio
   - tokenize(text) → list de tokens
   - extract_features(lyrics_text) → dict:
     * word_freq: dict
     * unique_words: int
     * avg_word_length: float
     * diversity_ratio: float (unique/total)
     * sentiment_score: float (-1 a 1)
     * top_ngrams: list (1-2 gramas)
     * tfidf_matrix: sparse matrix
   
2. Análisis por artista:
   - analyze_artist_lyrics(artist_lyrics_list) → dict agregado
   - compare_artists(artist1_lyrics, artist2_lyrics) → dict
   
3. Técnicas a usar:
   - VADER para sentiment (via nltk)
   - TF-IDF (sklearn)
   - Word2Vec embeddings (gensim)
   - N-gramas (nltk)
   - Stopwords en inglés/español
   
4. Funciones auxiliares:
   - extract_themes(text) → list de temas
   - calculate_lexical_diversity(text) → float
   - detect_language(text) → str

Output: src/nlp_analyzer.py completamente funcional

Usa librerías:
- nltk
- sklearn
- gensim
- textblob or vader_sentiment

---FIN---
```

---

#### Paso 7: Audio Features Analysis
```
Abre Claude Code:

---INICIO---

Implementa análisis de features de audio de Spotify.

En src/data_processor.py agregar funciones:

1. aggregate_features(tracks_df) → dict:
   - Promedio de cada feature
   - Desviación estándar
   - Min/Max

2. feature_evolution(tracks_df) → dict:
   - Features por año (timeline)
   - Detección de cambios significativos

3. compare_artists(artist1_tracks, artist2_tracks) → dict:
   - Features comparativas
   - Diferencias estadísticas

4. Detect style shift:
   - Detectar cuándo cambió el sonido
   - Qué features cambiaron

Output: Funciones en src/data_processor.py

---FIN---
```

---

### FASE 3: Visualización (Agent 3)

**Objetivo**: Gráficos interactivos  
**Tiempo**: 2-3 horas  
**Archivos**: visualization.py

#### Paso 8: Gráficos Plotly
```
Abre Claude Code:

---INICIO---

Eres un experto en visualización de datos con Plotly.

Necesito crear gráficos profesionales e interactivos.

Implementa en src/visualization.py:

1. plot_word_cloud(lyrics_dict) → HTML/Plotly
   - Nube de palabras interactiva
   - Colores bonitos (usar Viridis)

2. plot_top_words_bar(word_freq, top_n=20) → Plotly bar
   - Ordenado por frecuencia
   - Hover con count

3. plot_sentiment_timeline(lyrics_by_year) → Plotly area
   - Positive/negative/neutral stacked
   - Rangeslider

4. plot_feature_scatter(tracks_df, x, y) → Plotly scatter
   - Color por año o álbum
   - Tamaño por duration
   - Hover con info

5. plot_feature_evolution(tracks_df) → Plotly line
   - Línea para cada feature
   - Rangeslider

6. plot_artist_comparison_radar(artist1, artist2) → Plotly radar
   - Features de audio
   - Métricas de NLP

Output: src/visualization.py con todas las funciones

Requisitos:
- Responsive
- Dark/light theme support
- Exportable a HTML
- Type hints
- Docstrings

---FIN---
```

---

#### Paso 9: Dashboards Altair
```
Abre Claude Code:

---INICIO---

Implementa dashboards interactivos con Altair.

En src/visualization.py agregar:

1. create_album_dashboard(albums_df) → altair chart
   - Tabla filtrable
   - Selector de artista
   - Ordenable

2. create_lyrics_dashboard(artist_lyrics) → altair chart
   - Top words table
   - Word frequency bar
   - Sentiment line

3. create_comparison_dashboard(artists_data) → altair chart
   - Side-by-side feature comparison
   - Radar charts

Output: Funciones altair en src/visualization.py

---FIN---
```

---

### FASE 4: Frontend (Agent 4)

**Objetivo**: App Streamlit funcional  
**Tiempo**: 4-5 horas  
**Archivos**: app/main.py, app/pages/*, app/components/*

#### Paso 10: Main App Structure
```
Abre Claude Code:

---INICIO---

Eres un experto en Streamlit.

Necesito crear una app multipage profesional.

Implementa app/main.py con:

1. Config:
   - st.set_page_config(page_title="🎵 Spotify Music Intelligence", layout="wide")
   - Sidebar logo/title
   
2. Navegación multipage:
   - st.sidebar con links a páginas
   - Session state para artista seleccionado
   
3. Home page:
   - Título y descripción
   - Instrucciones
   - Stats generales

4. Structure:
   - Importar páginas: pages/01_*, pages/02_*, etc
   - Caché de datos
   - Error handling

Output: app/main.py funcional

Usar:
- @st.cache_resource para caching
- st.session_state para estado global
- Try-except y st.error() para errores

---FIN---
```

---

#### Paso 11: Pages 1-4
```
Abre Claude Code. Para CADA página:

PÁGINA 1: Album Catalogue
---
Implementa app/pages/01_Album_Catalogue.py

Requisitos:
1. Sidebar:
   - Input text: artist name
   - Button: Load Albums
   
2. Contenido:
   - Métrica: "Studio Albums: N"
   - Tabla con columnas: Name, Release Date, Track Count
   - Sorteable y filtrable
   - Gráfico: Timeline de lanzamientos
   
3. Features:
   - @st.cache_data para caching
   - Manejo de errores
   - Loading state

Output: app/pages/01_Album_Catalogue.py
---

PÁGINA 2: Audio Features Analysis
---
Implementa app/pages/02_Audio_Features.py

Requisitos:
1. Sidebar:
   - Multiselect: features (energy, danceability, etc)
   - Slider: year range
   
2. Contenido:
   - Métrica: "Total Tracks: N"
   - 3 Gráficos:
     * Feature evolution timeline
     * Feature scatter plot
     * Heatmap features x year
   - Tabla de estadísticas

Output: app/pages/02_Audio_Features.py
---

PÁGINA 3: Lyrics Analysis
---
Implementa app/pages/03_Lyrics_Analysis.py

Requisitos:
1. Sidebar:
   - Artist selector
   - Top N words slider

2. Contenido:
   - Métrica: "Lyrics Processed: N songs"
   - Nube de palabras
   - Top words bar chart
   - Sentiment timeline
   - Lexical diversity metric
   - Tabla: análisis por canción

Output: app/pages/03_Lyrics_Analysis.py
---

PÁGINA 4: Artist Comparison
---
Implementa app/pages/04_Artist_Comparison.py

Requisitos:
1. Sidebar:
   - Multiselect: artistas (max 3)

2. Contenido:
   - Radar chart de features
   - Tabla comparativa de stats
   - Side-by-side lyrics analysis
   - Feature evolution overlay

Output: app/pages/04_Artist_Comparison.py
---
```

---

#### Paso 12: Components
```
Abre Claude Code:

---INICIO---

Implementa componentes reutilizables.

app/components/header.py:
- render_header() → muestra título, descripción

app/components/sidebar.py:
- artist_selector() → selectbox con artistas
- feature_selector() → multiselect features
- date_range_slider() → slider range

app/components/metrics.py:
- show_metric(label, value) → métrica styled
- show_metrics_row(list de métricas)

Output: Componentes funcionales

---FIN---
```

---

### FASE 5: Documentación (Agent 5)

**Objetivo**: Notebooks + documentación  
**Tiempo**: 2-3 horas

#### Paso 13: Notebook Spotify
```
Abre Claude Code:

---INICIO---

Crea notebook: notebooks/01_spotify_exploration.ipynb

Requisitos:
1. Secciones:
   - 1. Setup & imports
   - 2. Load Spotify data
   - 3. Explore datasets
   - 4. Album filtering (con explicación detallada)
   - 5. Audio features analysis
   - 6. Temporal evolution
   - 7. Conclusions

2. Características:
   - Usa src/ modules
   - Ejemplos con Radiohead
   - Muchos comentarios explicativos
   - 25-30 celdas
   - Visualizaciones claras

Output: Notebook reproducible

---FIN---
```

---

#### Paso 14: Notebook Lyrics
```
Abre Claude Code:

---INICIO---

Crea notebook: notebooks/02_lyrics_analysis.ipynb

Requisitos:
1. Secciones:
   - 1. Fetch lyrics
   - 2. Text preprocessing
   - 3. Basic statistics
   - 4. NLP analysis (sentiment, TF-IDF, etc)
   - 5. Comparaciones
   - 6. Conclusions

2. Visualizaciones y análisis completo

Output: Notebook reproducible

---FIN---
```

---

#### Paso 15: Documentación
```
Abre Claude Code:

---INICIO---

Genera:

1. requirements.txt:
   - pandas, numpy
   - spotipy o spotify-api
   - streamlit, plotly, altair
   - nltk, gensim, sklearn
   - python-dotenv
   - requests, beautifulsoup4
   
   Versiones específicas y compatibles

2. .env.example:
   - SPOTIFY_CLIENT_ID=xxx
   - SPOTIFY_CLIENT_SECRET=xxx
   - DEBUG=false
   
3. README.md:
   - Descripción del proyecto
   - Requisitos
   - Instalación
   - Uso (cómo ejecutar la app)
   - Estructura
   - Contribuciones

4. deployment.md:
   Para Streamlit Cloud, Railway, HF Spaces:
   - Pasos de setup
   - Variables de entorno
   - Comandos de deploy
   - Troubleshooting

Output: Todos los archivos

---FIN---
```

---

## 🧪 TESTING & VERIFICACIÓN

Después de CADA fase, ejecuta en Claude Code:

```bash
# Verifica importes
python -c "from src import config, utils"
python -c "from src.spotify_api import SpotifyHandler"
python -c "from src.lyrics_handler import LyricsHandler"

# Verifica estructura
find . -name "*.py" | wc -l  # Debería ser ~25+

# Lint básico
python -m py_compile src/*.py

# Test app
streamlit run app/main.py --logger.level=debug
```

---

## 🚀 DESPLIEGUE FINAL

Una vez todo funciona:

### En Streamlit Cloud (recomendado):
```bash
git push origin main
# Va a streamlit.io → nuevo app → conecta repo
# Variables de entorno en Settings
```

### En Railway:
```bash
railway link
railway up
```

### En HF Spaces:
```
Crea nuevo Space
Conecta GitHub repo
Variables en Settings
```

---

## 📊 CHECKLIST FINAL

- [ ] Fase 1: Setup + APIs ✅
- [ ] Fase 2: Análisis datos ✅
- [ ] Fase 3: Visualizaciones ✅
- [ ] Fase 4: App Streamlit ✅
- [ ] Fase 5: Documentación ✅
- [ ] Testing: Todo funciona ✅
- [ ] Deploy: En 1+ plataforma ✅
- [ ] Memoria académica escrita ✅

---

## 💡 TROUBLESHOOTING

**Problema**: "ModuleNotFoundError: No module named 'src'"
**Solución**: 
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
# o en .env o en Claude Code context
```

**Problema**: "Spotify API rate limit"
**Solución**: Aument delays en config.py

**Problema**: "Lyrics API timeout"
**Solución**: Usa fallback a caché local

**Problema**: "Streamlit session state issues"
**Solución**: Re-inicia la app con `streamlit run --logger.level=debug`

---

## 📞 PREGUNTAS FRECUENTES

**P: ¿Puedo ejecutar todo de una vez?**
A: No. Hazlo fase por fase. Cada agente depende del anterior.

**P: ¿Cuánto tiempo toma?**
A: ~15-20 horas totales. Con Claude Code: ~5-10 horas (agentes son rápidos).

**P: ¿Necesito credenciales de Spotify?**
A: Sí. Ve a https://developer.spotify.com → register app → copia client ID y secret

**P: ¿Funciona sin internet?**
A: No. Necesita APIs externas. Pero puedes usar datos cachés locales.

**P: ¿Cuál es la nota final?**
A: Si cumples TODOS los requisitos: 9-10/10. Es un proyecto solid.

---

## 🎓 VALOR ACADÉMICO

Este proyecto demuestra:
✅ Integración de APIs externas  
✅ Procesamiento y limpieza de datos  
✅ Análisis estadístico y NLP  
✅ Visualización de datos  
✅ Web development (Streamlit)  
✅ Buenas prácticas (modularidad, testing, documentación)  

**Es un proyecto professional-grade**. Los profesores lo notarán.
