# 🎵 Spotify Music Intelligence

Sistema de análisis musical universitario con NLP de letras y visualización interactiva.

## Descripción

Proyecto de análisis de música de Spotify que combina:
- **Filtrado de álbumes de estudio** (2 puntos): algoritmo de 4 etapas para identificar exclusivamente álbumes de estudio originales
- **Análisis NLP de letras** (4 puntos): VADER sentiment, TF-IDF, n-gramas, Word2Vec, diversidad léxica
- **Web app interactiva** (4 puntos): Streamlit con 4 páginas, filtros dinámicos y gráficos Plotly/Altair

## Estructura del Proyecto

```
spotify-music-intelligence/
├── src/
│   ├── config.py          # Configuración centralizada (env vars, logging)
│   ├── utils.py           # Utilidades: retry, timing, normalize_text, batch_processor
│   ├── spotify_api.py     # Cliente Spotify con retry y paginación
│   ├── lyrics_handler.py  # Letras: lyrics.ovh + Genius + caché local
│   ├── data_processor.py  # filter_studio_albums(), feature_evolution(), comparativas
│   ├── nlp_analyzer.py    # VADER, TF-IDF, Word2Vec, LyricsAnalyzer
│   └── visualization.py   # Plotly (word cloud, radar, heatmap) + Altair dashboards
│
├── app/
│   ├── main.py                        # Streamlit home page
│   ├── pages/
│   │   ├── 01_Album_Catalogue.py      # Filtrado + timeline + tracks
│   │   ├── 02_Audio_Features.py       # Features + heatmap + evolución
│   │   ├── 03_Lyrics_Analysis.py      # NLP + word cloud + VADER + TF-IDF
│   │   └── 04_Artist_Comparison.py    # Comparativa radar + NLP side-by-side
│   └── components/
│       ├── header.py     # render_header()
│       ├── sidebar.py    # artist_selector(), feature_selector(), date_range_slider()
│       └── metrics.py    # show_metric(), show_metrics_row()
│
├── notebooks/
│   ├── 01_spotify_exploration.ipynb   # Filtrado álbumes + audio features (25+ celdas)
│   └── 02_lyrics_analysis.ipynb       # NLP completo (22+ celdas)
│
├── data/
│   ├── cache/             # Caché JSON de la API y letras
│   └── logs/              # app.log
│
├── tests/
│   ├── test_spotify.py    # Tests SpotifyClient
│   ├── test_analysis.py   # Tests DataProcessor + NLPAnalyzer
│   └── test_lyrics.py     # Tests LyricsHandler
│
├── .env.example           # Template de variables de entorno
├── requirements.txt       # Dependencias Python
└── README.md
```

## Requisitos Previos

- Python 3.11+
- Cuenta de desarrollador en [Spotify for Developers](https://developer.spotify.com/)
- (Opcional) Token de [Genius API](https://genius.com/api-clients) para mejor cobertura de letras

## Instalación

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd spotify-music-intelligence

# 2. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar credenciales
cp .env.example .env
# Editar .env con tu SPOTIFY_CLIENT_ID y SPOTIFY_CLIENT_SECRET
```

## Configuración

Crea un archivo `.env` en la raíz del proyecto:

```env
SPOTIFY_CLIENT_ID=tu_client_id_aqui
SPOTIFY_CLIENT_SECRET=tu_client_secret_aqui
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback

# Opcionales para mejor cobertura de letras
GENIUS_API_TOKEN=tu_genius_token_aqui

# Configuración de la app
LOG_LEVEL=INFO
CACHE_TTL=3600
```

### Cómo obtener credenciales de Spotify

1. Ir a [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Crear una nueva aplicación
3. Copiar `Client ID` y `Client Secret`
4. Añadir `http://localhost:8888/callback` como Redirect URI

## Ejecución

### Web App (Streamlit)

```bash
streamlit run app/main.py
```

La app se abrirá en `http://localhost:8501`

### Notebooks

```bash
jupyter notebook notebooks/
```

- `01_spotify_exploration.ipynb`: Filtrado de álbumes y audio features
- `02_lyrics_analysis.ipynb`: NLP completo de letras

### Tests

```bash
pytest tests/ -v
pytest tests/ --cov=src --cov-report=html
```

## Funcionalidades

### Página 1: Album Catalogue
- Búsqueda de artistas en Spotify
- **Filtrado automático de álbumes de estudio** (excluye live, compilations, remasters, EPs)
- Timeline interactivo de lanzamientos
- Distribución de tracks por álbum
- Log de álbumes excluidos (auditable)

### Página 2: Audio Features
- Carga de todas las pistas de la discografía de estudio
- Filtro por rango de años
- Gráfico de evolución temporal de features
- Scatter plot interactivo (cualquier feature vs cualquier feature)
- Heatmap features × año
- Estadísticas descriptivas completas

### Página 3: Lyrics Analysis
- Obtención de letras via lyrics.ovh (sin API key) + Genius (opcional)
- VADER sentiment por canción + timeline temporal
- Word cloud interactivo (Plotly)
- Top palabras por frecuencia
- TF-IDF keywords
- Gauge de diversidad léxica
- N-gramas (bigramas más frecuentes)

### Página 4: Artist Comparison
- Comparación de hasta 3 artistas simultáneamente
- Radar chart de audio features
- Boxplot de distribuciones
- Overlay de evolución temporal
- Tabla comparativa NLP

## Algoritmo de Filtrado (Requisito 1)

La función `filter_studio_albums()` en `src/data_processor.py` aplica:

1. **Tipo**: Solo `album_type == 'album'` → excluye singles, compilaciones
2. **Keywords**: Excluye si el título contiene: *live, compilation, reissue, deluxe, edition, remix, instrumental, remaster, greatest hits,* etc.
3. **EPs**: Excluye álbumes con < 5 pistas
4. **Deduplicación**: Normaliza nombres (elimina sufijos de remaster) y conserva la versión más antigua

```python
from src.data_processor import filter_studio_albums, DataProcessor

albums_df = DataProcessor.albums_to_df(raw_albums)
studio_df, log = filter_studio_albums(albums_df)
```

## Pipeline NLP (Requisito 2)

```python
from src.nlp_analyzer import LyricsAnalyzer

analyzer = LyricsAnalyzer()

# VADER sentiment
features = analyzer.extract_features(lyrics_text)
# → sentiment_score, vader_detail, top_ngrams, word_freq, diversity_ratio

# TF-IDF keywords
keywords = analyzer.tfidf_keywords(lyrics_list, top_n=20)

# Word2Vec embeddings
embedding = analyzer.get_embeddings(text, vector_size=50)

# Comparativa entre artistas
comparison = analyzer.compare_artists(lyrics_1, lyrics_2, "Artist A", "Artist B")
```

## Tecnologías

| Categoría | Tecnología |
|-----------|-----------|
| API Datos | Spotipy (Spotify Web API) |
| Letras | lyrics.ovh, Genius API |
| NLP | NLTK, VADER, scikit-learn, gensim |
| Visualización | Plotly, Altair, Matplotlib, wordcloud |
| Web App | Streamlit |
| Datos | pandas, numpy |

## Fuentes de Datos

- **Spotify Web API**: metadatos de artistas, álbumes, pistas y audio features
- **lyrics.ovh**: letras de canciones (gratuito, sin API key)
- **Genius API**: letras adicionales (requiere token, opcional)
