# 🎬 PROMPTS MAESTROS para Claude Code Agents
## Proyecto: Spotify Music Intelligence

---

## ⚙️ AGENT 1: DATA FOUNDATION ENGINEER

### PROMPT 1.1: Setup del Proyecto
```
Contexto:
- Estoy creando un proyecto Python de análisis musical
- Objetivo: Análisis de Spotify + letras + visualización
- Stack: Python 3.11+, Streamlit, Plotly, scikit-learn

Tarea:
Crea la estructura COMPLETA del proyecto con TODAS las carpetas y archivos base.

Requisitos:
1. Carpeta structure debe ser:
   src/ → módulos de lógica
   notebooks/ → Jupyter notebooks
   app/ → código Streamlit
   data/ → datos y caché
   tests/ → tests unitarios
   
2. Crea archivos base vacíos pero con docstrings
3. Crea __init__.py donde sea necesario
4. Genera .env.example con variables de entorno
5. Crea .gitignore apropiado

Output esperado:
- Árbol de carpetas completo
- Todos los archivos .py con headers y docstrings
- Nada debe faltar

No olvides:
- Comentarios de cabecera en cada archivo
- Estructura modular y escalable
- Paths relativos correctos
```

### PROMPT 1.2: Integración Spotify API
```
Contexto:
- Tengo credenciales de Spotify API (ID y SECRET)
- Necesito obtener: artistas, álbumes, tracks, audio features
- Rate limit: 15 req/min

Tarea:
Implementa src/spotify_api.py con clase SpotifyHandler

Requisitos OBLIGATORIOS:
1. Clase SpotifyHandler con métodos:
   - get_artist(artist_name) → dict con datos del artista
   - get_artist_albums(artist_id) → list de álbumes
   - get_album_tracks(album_id) → list de tracks
   - get_audio_features(track_id) → features de audio
   - get_multiple_artists(names) → procesamiento batch

2. Manejo de errores:
   - Try-except en TODAS las llamadas
   - Custom exceptions: SpotifyAPIError, RateLimitError
   - Logging detallado

3. Rate limiting:
   - Delays automáticos entre requests
   - Retry logic con exponential backoff
   - Máximo 3 reintentos

4. Validación:
   - Input sanitization
   - Validar IDs antes de usar
   - Return type hints

5. Caching:
   - Opción para cachear resultados en JSON local
   - Cache TTL configurable

Código debe:
- Tener docstrings en toda función
- Usar logging en lugar de print
- Ser testeable (inyectable de dependencias)
- Manejar None/empty gracefully

Output: src/spotify_api.py completamente funcional
```

### PROMPT 1.3: Integración Lyrics.ovh API
```
Contexto:
- API lyrics.ovh es pública y sin autenticación
- Rate limit: ~100 req/min
- Some songs unavailable

Tarea:
Implementa src/lyrics_handler.py con clase LyricsHandler

Requisitos OBLIGATORIOS:
1. Clase LyricsHandler:
   - get_lyrics(artist, song) → str (letras)
   - get_lyrics_batch(list de (artist, song)) → dict
   - get_lyrics_with_fallback(artist, song) → str o None
   
2. Manejo de errores:
   - API timeout? → retry con delay
   - Song not found? → return None (no error)
   - Network error? → logging + retry
   
3. Rate limiting:
   - Delays entre requests
   - Queue para batch processing
   - Fallback a caché si API down
   
4. Caching:
   - Cache local en JSON/pickle
   - Invalidación por fecha
   - Búsqueda fuzzy si exact match falla
   
5. Text cleaning:
   - Normalizar encoding
   - Remover caracteres especiales
   - Lowercase estandarizado

Código debe:
- Ser robusto (no fallar si API falla)
- Loguear everything
- Ser reutilizable
- Tener fallbacks

Output: src/lyrics_handler.py completamente funcional
```

### PROMPT 1.4: Config y Utils
```
Contexto:
- Necesito centralizar configuración
- Env vars para credenciales
- Constantes del proyecto

Tarea:
Implementa:
1. src/config.py con:
   - Variables de entorno (Spotify credentials)
   - Constantes del proyecto (timeouts, retries, batch sizes)
   - Paths de datos
   - Configuración de logging
   - Feature flags para debug
   
2. src/utils.py con:
   - normalize_text() → limpia y normaliza strings
   - batch_processor() → procesa listas en chunks
   - safe_json_load/dump() → JSON seguro
   - Logger factory
   - Decoradores: retry, timing, cache
   
Output: Ambos archivos completamente funcionales
```

---

## 📊 AGENT 2: ANALYSIS & NLP SPECIALIST

### PROMPT 2.1: Filtrado de Álbumes de Estudio
```
Contexto:
- Spotify API devuelve TODOS los tipos de álbum
- Necesito SOLO álbumes de estudio
- Tipos a excluir: single, compilation, live, EP, remix, reissue, deluxe
- Requisito académico crítico (2 puntos)

Tarea:
Implementa src/data_processor.py con función filter_studio_albums()

Requisitos OBLIGATORIOS:
1. Criterios de filtrado:
   - album_type == "album" (Spotify API)
   - Excluir por palabras clave en nombre:
     "live", "compilation", "reissue", "deluxe", "edition", "remix"
   - Excluir remasterizaciones duplicadas (mismo nombre + año)
   - Excluir EPs (menos de 5 tracks usualmente)
   - Lógica fuzzy para typos

2. Referencia Wikipedia:
   - Radiohead: OK Computer, Kid A, etc = SOLO estos
   - The Beatles: estudio releases = SOLO estos
   
3. Heurísticas inteligentes:
   - Si nombre contiene "remaster" pero es diferente año → considerar
   - Si nombre es igual pero release_date diferentes → deduplicar
   - Si track_count < 4 → probablemente EP → excluir
   
4. Output:
   - DataFrame limpio con solo estudios
   - Log detallado de qué se excluyó y por qué
   - Score de confianza del filtrado

5. Validación:
   - Cross-check con datos públicos (Wikipedia, AllMusic)
   - Ejemplos visuales de qué se excluyó

Output:
- Función filter_studio_albums(albums_df) → clean_df
- Función explain_filtering(albums_df) → report con detalles
- Tests con casos conocidos (Radiohead, Beatles, etc)

Aclaración importante:
Este es uno de los requisitos críticos. Debe ser PERFECTO.
Incluye documentación de cada decisión de filtrado.
```

### PROMPT 2.2: Pipeline NLP para Letras
```
Contexto:
- Tengo letras de canciones (strings)
- Necesito análisis NLP completo
- Idiomas: principalmente inglés (puede haber español)

Tarea:
Implementa src/nlp_analyzer.py con clase LyricsAnalyzer

Requisitos:
1. Limpieza de texto:
   - Remover metadata (verse, chorus, bridge labels)
   - Normalizar whitespace
   - Convertir a lowercase
   - Remover caracteres especiales (mantener palabras)
   
2. Tokenización:
   - Word tokens
   - Sentence tokens
   - Lemmatization/stemming
   
3. Stopwords:
   - Remover inglés
   - Opción para remover español
   - Mantener palabras "interesantes"
   
4. Análisis básico:
   - Palabra más frecuente
   - Longitud promedio de canción
   - Diversidad léxica (unique words / total words)
   - Vocabulary size
   
5. Análisis avanzado:
   - Sentiment analysis (VADER o TextBlob)
   - TF-IDF por canción/artista
   - N-gramas (1-2 gramas más comunes)
   - Word embeddings (word2vec con gensim)
   
6. Funciones públicas:
   - analyze_single_lyrics(text) → dict de métricas
   - analyze_artist_lyrics(list de lyrics) → dict agregado
   - compare_artists(artist1_lyrics, artist2_lyrics) → dict
   - get_common_themes(lyrics) → list de temas
   
Output:
- Clase LyricsAnalyzer completamente funcional
- Métodos bien documentados
- Ejemplos de uso

Librerías sugeridas:
- nltk (tokenization, stopwords, sentiment)
- gensim (embeddings)
- sklearn (TF-IDF)
```

### PROMPT 2.3: Análisis de Features de Audio
```
Contexto:
- Tengo features de Spotify para cada track
- Necesito análisis a nivel artista/álbum
- Features: danceability, energy, valence, tempo, etc

Tarea:
Implementa src/data_processor.py con funciones de análisis

Requisitos:
1. Funciones de agregación:
   - average_features(tracks_df) → dict
   - feature_evolution_by_year(tracks_df) → time series
   - album_audio_signature(album_df) → caracterización
   
2. Comparativas:
   - compare_artists_features(artist1, artist2) → dict
   - feature_clustering(tracks_df) → grupos similares
   
3. Detección de cambios:
   - detect_style_shift(artist_timeline) → qué cambió
   - significant_features(tracks_df) → qué destaca
   
Output:
- Funciones lisas y reusables
- Return type hints
- Documentación
```

---

## 🎨 AGENT 3: VISUALIZATION MAESTRO

### PROMPT 3.1: Gráficos con Plotly
```
Contexto:
- Necesito visualizaciones interactivas y profesionales
- Stack: Plotly (preferido) + Streamlit
- Audiencia: estudiantes + profesores (nivel académico)

Tarea:
Implementa src/visualization.py con funciones Plotly

Requisitos:
1. Nube de palabras (wordcloud):
   - plot_word_cloud(lyrics_dict) → HTML interactive
   - Tamaño proporcional a frecuencia
   - Colores bonitos
   
2. Palabras más comunes:
   - plot_top_words_bar(lyrics_dict, top_n=20) → plotly bar chart
   - Ordenadas por frecuencia
   - Selección interactiva
   
3. Heatmap de frecuencia:
   - plot_word_frequency_heatmap(artists_lyrics) → heatmap
   - Filas: palabras, Columnas: artistas
   - Colores intensos
   
4. Scatter plot de songs:
   - plot_song_scatter(tracks_df, x_feature, y_feature) → scatter
   - Color por album/year
   - Tamaño por duration
   - Hover con info
   
5. Timeline evolution:
   - plot_feature_timeline(artist_tracks) → line chart
   - Líneas para cada feature
   - Rangeslider para zoom
   
6. Heatmap temporal:
   - plot_heatmap_by_year_feature(tracks_df) → heatmap
   - Años vs features
   - Valores = promedio
   
7. Sentiment evolution:
   - plot_sentiment_timeline(lyrics_by_year) → area chart
   - Positivo/negativo/neutral
   - Stacked
   
8. Comparison radar:
   - plot_artist_comparison_radar(artist1, artist2) → radar chart
   - Radios: features de audio + NLP
   
Output:
- Todas las funciones en src/visualization.py
- Parámetro theme configurable
- Responsive y bonito
- Exportable a HTML

Librerías:
- plotly.graph_objects
- plotly.express
- wordcloud
```

### PROMPT 3.2: Dashboards con Altair
```
Contexto:
- Necesito dashboards interactivos
- Altair es perfecto para selectores dinámicos
- Varias visualizaciones en una pantalla

Tarea:
Implementa src/visualization.py con dashboards Altair

Requisitos:
1. Dashboard 1: Análisis de Álbumes
   - Tabla de álbumes filtrable
   - Selector de artista
   - Sort por year/name/track count
   
2. Dashboard 2: Análisis de Letras
   - Top N words table
   - Selector de artista
   - Filtro por palabra clave
   
3. Dashboard 3: Comparativa de Artistas
   - Side-by-side feature comparison
   - Multiselect de artistas (max 3)
   - Toggle entre features
   
Output:
- Todas las funciones de Altair en visualization.py
- Interactivas y responsive
- Integrable en Streamlit

Librerías:
- altair
- vega-lite json spec
```

---

## 🎯 AGENT 4: FRONTEND & APP BUILDER

### PROMPT 4.1: Estructura Principal Streamlit
```
Contexto:
- App Streamlit multipage
- 4 páginas + sidebar
- Interfaz limpia y profesional

Tarea:
Crea app/main.py con estructura base

Requisitos:
1. Configuración:
   - Título: "🎵 Spotify Music Intelligence"
   - Layout: wide
   - Sidebar con logo
   
2. Estructura multipage:
   - Home/Dashboard
   - 1. Album Catalogue
   - 2. Audio Features Analysis
   - 3. Lyrics Analysis
   - 4. Artist Comparison
   
3. Navegación:
   - Sidebar con selectbox/radio
   - Links a cada página
   
4. Global state:
   - Caché de datos descargados
   - Artista seleccionado globalmente
   
5. Error handling:
   - Try-except en todo
   - Mensajes de error amigables
   - Retry buttons

Output:
- app/main.py completamente funcional
- Importa las otras páginas
- Clean code
```

### PROMPT 4.2-4.5: Páginas Individuales
```
PÁGINA 1: Album Catalogue

Requisitos:
1. Sidebar:
   - Input: Artist name
   - Botón: "Load Albums"
   
2. Contenido:
   - Métrica: Total albums (studio only)
   - Tabla interactiva con columnas:
     * Album name
     * Release date
     * Track count
     * Studio? (sí/no)
   - Ordenable y filtrable
   
3. Visualización:
   - Timeline de lanzamientos
   - Distribución de tracks por álbum
   
Output: app/pages/01_Album_Catalogue.py

---

PÁGINA 2: Audio Features Analysis

Requisitos:
1. Sidebar:
   - Multiselect: Seleccionar features a visualizar
   - Slider: Rango de años
   
2. Contenido:
   - Métrica: Total songs analyzed
   - Gráfico 1: Evolución temporal de features
   - Gráfico 2: Scatter plot (2 features seleccionables)
   - Gráfico 3: Heatmap de features por año
   - Tabla: Estadísticas de features
   
Output: app/pages/02_Audio_Features.py

---

PÁGINA 3: Lyrics Analysis

Requisitos:
1. Sidebar:
   - Artista selection
   - Top N words slider
   
2. Contenido:
   - Métrica: Total lyrics processed
   - Nube de palabras
   - Top words bar chart
   - Sentiment timeline
   - Diversidad léxica por artista
   - Tabla de análisis por canción
   
Output: app/pages/03_Lyrics_Analysis.py

---

PÁGINA 4: Artist Comparison

Requisitos:
1. Sidebar:
   - Multiselect: Max 3 artistas
   
2. Contenido:
   - Radar chart de features
   - Tablas comparativas (audio + lyrics)
   - Side-by-side lyrics analysis
   - Comparativa de evolución
   
Output: app/pages/04_Artist_Comparison.py
```

### PROMPT 4.6: Componentes Reutilizables
```
Tarea:
Crea app/components/ con componentes Streamlit reutilizables

Requisitos:
1. app/components/header.py:
   - render_header() → con logo, título, descripción
   
2. app/components/sidebar.py:
   - render_artist_selector() → selectbox con artistas
   - render_date_range() → slider de fechas
   - render_feature_selector() → multiselect de features
   
3. app/components/metrics.py:
   - show_metric(label, value, icon) → métrica con estilo
   - show_metrics_row(metrics) → fila de métricas
   
Output:
- Todos los componentes en app/components/
- Reutilizable y limpio
```

---

## 📖 AGENT 5: NOTEBOOK & DOCUMENTATION

### PROMPT 5.1: Notebook Mejorado
```
Contexto:
- Tengo notebook Spotify_simple_Radiohead.ipynb
- Debo convertirlo en versión mejorada, modular y comentada
- Requisito académico

Tarea:
Crea notebooks/01_spotify_exploration.ipynb

Requisitos:
1. Estructura:
   - 1. Setup & Data Loading
   - 2. Artist & Album Analysis
   - 3. Audio Features Overview
   - 4. Studio Album Filtering (con explicación detallada)
   - 5. Temporal Evolution Analysis
   - 6. Conclusions
   
2. Contenido:
   - Importar de src/ (usar local modules)
   - Ejemplos prácticos con datos reales
   - Explicaciones de cada paso
   - Visualizaciones claras
   
3. Comentarios académicos:
   - Por qué cada análisis es importante
   - Qué interpretamos de los datos
   - Limitaciones del análisis
   - Mejoras futuras

Output:
- Notebook completo y funcional
- Reproducible (sin errores)
- 20-30 celdas
- Explicaciones en markdown
```

### PROMPT 5.2: Notebook de Letras
```
Tarea:
Crea notebooks/02_lyrics_analysis.ipynb

Requisitos:
1. Estructura:
   - 1. Fetching Lyrics
   - 2. Text Cleaning & Preprocessing
   - 3. Basic Statistics
   - 4. Advanced NLP Analysis
   - 5. Sentiment & Themes
   - 6. Comparison Between Artists
   
2. Visualizaciones:
   - Nubes de palabras
   - Gráficos de frecuencia
   - Evolución temporal de sentimiento
   
Output:
- Notebook completo
- Reproducible
- 20-25 celdas
```

### PROMPT 5.3: Comentarios para Memoria
```
Contexto:
- Debo escribir una memoria académica
- ~15 páginas
- Incluye: introducción, metodología, resultados, conclusiones

Tarea:
Genera comentarios/textos para cada sección

Requisitos:
1. Introducción:
   - Contexto: análisis musical con datos
   - Importancia de Spotify + NLP
   - Objetivos del proyecto

2. Metodología:
   - Fuentes de datos (Spotify API, lyrics.ovh)
   - Algoritmos de filtrado
   - Pipeline NLP
   - Visualizaciones

3. Resultados:
   - Insights de Radiohead (ejemplo)
   - Validación del filtrado
   - Ejemplos de análisis

4. Conclusiones:
   - Qué aprendimos
   - Limitaciones
   - Trabajo futuro

Output:
- Textos listos para copy-paste
- Tono académico
- Cada sección comentada
```

### PROMPT 5.4: Guía de Despliegue
```
Tarea:
Crea deployment.md con instrucciones para 4 plataformas

Requisitos:
Para cada plataforma (Streamlit Cloud, Railway, HF Spaces, Render):
1. Requisitos previos
2. Pasos de configuración
3. Variables de entorno
4. Deploy commands
5. Troubleshooting

Output:
- deployment.md con todas las instrucciones
- Step-by-step
- Screenshots sugeridas
```

### PROMPT 5.5: Requirements y Setup
```
Tarea:
Genera requirements.txt final y setup.py

Requisitos:
1. requirements.txt:
   - Todas las librerías del proyecto
   - Versiones específicas (compatible)
   - Categorías: core, viz, nlp, dev
   
2. setup.py:
   - Metadata del proyecto
   - Dependencias
   - Entry points

Output:
- requirements.txt
- setup.py
- .env.example con variables
```

---

## 🚀 ORDEN DE EJECUCIÓN RECOMENDADO

**Día 1: Fundación**
- PROMPT 1.1 → Setup
- PROMPT 1.2 → Spotify API
- PROMPT 1.3 → Lyrics API
- PROMPT 1.4 → Config & Utils

**Día 2: Análisis**
- PROMPT 2.1 → Album Filtering
- PROMPT 2.2 → NLP Pipeline
- PROMPT 2.3 → Audio Analysis

**Día 3: Visualización**
- PROMPT 3.1 → Plotly
- PROMPT 3.2 → Altair

**Día 4: App**
- PROMPT 4.1 → Main structure
- PROMPT 4.2-4.5 → Páginas
- PROMPT 4.6 → Componentes

**Día 5: Documentación**
- PROMPT 5.1-5.5 → Notebooks + deployment

---

## 📝 TIPS PARA EJECUTAR CON CLAUDE CODE

1. **Copiar un prompt a la vez** en Claude Code
2. **Verificar que compila** antes del siguiente
3. **Testear funciones** básicamente
4. **Revisar comentarios** son suficientes
5. **Pedir refactoring** si es necesario

---

## ✅ CHECKLIST FINAL

- [ ] Agent 1: Setup + APIs funcionando
- [ ] Agent 2: Filtrado correcto, análisis NLP funcionando
- [ ] Agent 3: Visualizaciones renderizando bien
- [ ] Agent 4: App Streamlit sin crashes
- [ ] Agent 5: Documentación completa
- [ ] Tests: Pasar basic tests
- [ ] Integration: Todo junto funcionando
- [ ] Deploy: En 1+ plataforma
