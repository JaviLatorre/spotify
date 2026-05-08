# 📚 CHEAT SHEET - Spotify Music Intelligence Project

---

## 🔗 ENLACES CLAVE

### APIs y Documentación
- **Spotify API**: https://developer.spotify.com/documentation/web-api
- **Spotify Auth**: https://accounts.spotify.com/authorize
- **Lyrics.ovh API**: https://api.lyrics.ovh/v1/{artist}/{song}
- **Audio Features Ref**: https://developer.spotify.com/documentation/web-api/reference/get-audio-features

### Librerías
- **Spotipy**: https://spotipy.readthedocs.io/
- **Streamlit**: https://docs.streamlit.io/
- **Plotly**: https://plotly.com/python/
- **NLTK**: https://www.nltk.org/
- **Scikit-learn**: https://scikit-learn.org/

### Deployment
- **Streamlit Cloud**: https://streamlit.io/cloud
- **Railway**: https://railway.app
- **HuggingFace Spaces**: https://huggingface.co/spaces
- **Render**: https://render.com

---

## ⚡ COMANDOS RÁPIDOS

### Setup Inicial
```bash
# Crear proyecto
mkdir spotify-music-intelligence && cd spotify-music-intelligence
git init

# Crear venv
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instalar deps
pip install -r requirements.txt
```

### Testing
```bash
# Verifica estructura
find . -type f -name "*.py" | grep -E "src|app" | wc -l

# Importes básicos
python -c "from src import spotify_api, lyrics_handler; print('OK')"

# Lint
flake8 src/ app/ --max-line-length=120

# Tests
pytest tests/
```

### Ejecutar App
```bash
# Dev mode
streamlit run app/main.py --logger.level=debug

# Production
streamlit run app/main.py --logger.level=warning
```

### Git
```bash
git add .
git commit -m "Feature: descriptive message"
git push origin main
```

---

## 📝 ESTRUCTURA DE CARPETAS (Quick Ref)

```
spotify-music-intelligence/
├── src/
│   ├── config.py           ← Variables de entorno
│   ├── spotify_api.py      ← Integración Spotify
│   ├── lyrics_handler.py   ← Integración lyrics.ovh
│   ├── data_processor.py   ← Limpieza y filtrado
│   ├── nlp_analyzer.py     ← Análisis NLP
│   ├── visualization.py    ← Gráficos Plotly/Altair
│   └── utils.py            ← Helpers
├── app/
│   ├── main.py             ← App principal
│   ├── pages/
│   │   ├── 01_Album_Catalogue.py
│   │   ├── 02_Audio_Features.py
│   │   ├── 03_Lyrics_Analysis.py
│   │   └── 04_Artist_Comparison.py
│   └── components/
│       ├── header.py
│       ├── sidebar.py
│       └── metrics.py
├── notebooks/
│   ├── 01_spotify_exploration.ipynb
│   └── 02_lyrics_analysis.ipynb
├── data/
│   ├── cache/
│   └── sample/
├── tests/
│   ├── test_spotify.py
│   ├── test_lyrics.py
│   └── test_analysis.py
└── requirements.txt
```

---

## 🎯 REQUISITOS CRÍTICOS (Checklist)

### 1. Filtrado de Álbumes (2 puntos) ✅
- [ ] Solo álbumes de estudio
- [ ] Excluir compilations, live, singles, EPs
- [ ] Explicación clara del algoritmo
- [ ] Validación con Wikipedia

### 2. Análisis de Letras (4 puntos) ✅
- [ ] API lyrics.ovh integrada
- [ ] Análisis NLP completo
- [ ] Visualizaciones modernas (10+ tipos)
- [ ] Comparativa entre artistas

### 3. Web App (4 puntos) ✅
- [ ] Streamlit funcional
- [ ] 4 páginas principales
- [ ] Filtros dinámicos
- [ ] Gráficos interactivos
- [ ] Deployable

---

## 🎨 TIPOS DE GRÁFICOS A IMPLEMENTAR

**Mínimo requerido**:
1. ☐ Nube de palabras
2. ☐ Palabras más frecuentes (bar chart)
3. ☐ Evolución temporal (line)
4. ☐ Comparativa de artistas (radar)
5. ☐ Heatmap de features

**Bonus (para nota alta)**:
6. ☐ Sentiment timeline
7. ☐ Scatter plot de songs
8. ☐ Clustering de canciones
9. ☐ PCA/t-SNE de embeddings
10. ☐ Comparativa de vocabulario

---

## 📊 FEATURES DE AUDIO (Spotify)

```python
features = {
    'danceability': float,     # 0-1 (qué bailarín)
    'energy': float,           # 0-1 (intensidad)
    'key': int,                # -1 to 11
    'loudness': float,         # dB
    'mode': int,               # 0=minor, 1=major
    'speechiness': float,      # % de palabras habladas
    'acousticness': float,     # 0-1 (acústico)
    'instrumentalness': float, # 0-1 (sin voces)
    'liveness': float,         # 0-1 (sonido en vivo)
    'valence': float,          # 0-1 (sentimiento positivo)
    'tempo': float,            # BPM
    'duration_ms': int,        # milisegundos
    'time_signature': float,   # 3/4, 4/4, etc
}
```

---

## 🔐 VARIABLES DE ENTORNO (.env)

```
# Spotify API
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here

# App config
DEBUG=false
LOG_LEVEL=INFO
CACHE_TTL=3600

# Optional
LYRICS_API_TIMEOUT=10
LYRICS_API_RETRIES=3
```

---

## 💾 CACHÉ ESTRATEGIA

```
datos/
├── cache/
│   ├── artists_{artist_name}.json      # Artists metadata
│   ├── albums_{artist_name}.json       # Albums list
│   ├── tracks_{album_id}.json          # Tracks + features
│   ├── lyrics_{artist}_{song}.json     # Letras
│   └── analysis_{artist_name}.json     # Análisis guardados
└── sample/
    ├── radiohead_tracks.csv
    └── radiohead_lyrics.json
```

Estrategia:
- TTL: 24 horas por defecto
- Invalidar manual si es necesario
- Fallback a caché si API falla

---

## 🧪 TESTS BÁSICOS

```python
# test_spotify.py
def test_get_artist():
    handler = SpotifyHandler(client_id, secret)
    artist = handler.get_artist("Radiohead")
    assert artist['name'] == "Radiohead"
    
def test_album_filtering():
    albums = [...]
    filtered = filter_studio_albums(pd.DataFrame(albums))
    assert len(filtered) == 6  # Radiohead studio albums

# test_lyrics.py
def test_get_lyrics():
    handler = LyricsHandler()
    lyrics = handler.get_lyrics("Radiohead", "Creep")
    assert "creep" in lyrics.lower()
    
def test_lyrics_robustness():
    handler = LyricsHandler()
    lyrics = handler.get_lyrics("InvalidArtist", "InvalidSong")
    assert lyrics is None  # No crash
```

---

## 🚀 DEPLOYMENT CHECKLIST

### Pre-deploy
- [ ] .env.example creado
- [ ] requirements.txt actualizado
- [ ] Código sin print() statements
- [ ] Logging configurado
- [ ] Tests pasando
- [ ] README.md actualizado

### Streamlit Cloud
```bash
# 1. Push a GitHub
git push origin main

# 2. Ve a https://streamlit.io/cloud
# 3. "New app" → selecciona repo
# 4. En Settings → Secrets → Agrega SPOTIFY_CLIENT_ID y SECRET
# 5. Deploy automático
```

### Railway
```bash
# 1. railway login
# 2. railway init
# 3. railway up
# 4. Variables en dashboard
```

### HF Spaces
```
# 1. Nuevo Space
# 2. Conecta GitHub
# 3. Selecciona "Streamlit" runtime
# 4. Variables en Settings
```

---

## 🐛 DEBUGGING

### "ModuleNotFoundError"
```python
import sys
sys.path.insert(0, '/path/to/project')
```

### "API Rate Limit"
- Aumentar delays en config.py
- Usar caché más agresivamente
- Procesar en batch (max 5 artistas)

### "Streamlit Session State Issues"
```python
# Reiniciar app
streamlit run app/main.py --logger.level=debug --client.reruns=false
```

### "Lyrics API Timeout"
- Usa `lyrics_handler.get_lyrics_with_fallback()`
- Fallback a caché o None
- No crashes

---

## 📚 TIPOS DE ANÁLISIS NLP

```python
# Básico
- word_frequency()
- unique_word_count()
- avg_word_length()

# Intermedio
- sentiment_score()          # VADER
- tfidf_analysis()          # sklearn
- ngram_extraction()        # nltk (1-2 gramas)

# Avanzado
- word_embeddings()         # word2vec (gensim)
- clustering_songs()        # KMeans sobre embeddings
- semantic_similarity()     # cosine similarity
- topic_modeling()          # LDA (bonus)
```

---

## 🎓 SECCIONES PARA LA MEMORIA

```
1. Introducción (2 págs)
   - Contexto: análisis musical
   - Importancia de datos en música
   - Objetivos

2. Metodología (4 págs)
   - Fuentes: Spotify API, lyrics.ovh
   - Filtrado de álbumes
   - Pipeline NLP
   - Visualizaciones

3. Resultados (5 págs)
   - Análisis de ejemplo (Radiohead)
   - Insights principales
   - Validación del filtrado
   - Gráficos y figuras

4. Conclusiones (2 págs)
   - Qué aprendimos
   - Limitaciones
   - Trabajo futuro

5. Apéndice (código snippets)
```

---

## ⚠️ ERRORES COMUNES A EVITAR

❌ No hacer:
- Usar print() en lugar de logging
- Hardcodear credenciales
- API calls sin error handling
- No cachear resultados
- Visualizaciones feas/sin interacción
- App sin docstrings
- Requirements sin versiones
- Deploy sin .env configurado

✅ Hacer:
- Logging en todo
- Variables de entorno
- Try-except en APIs
- Caché local agresivo
- Gráficos Plotly/Altair
- Docstrings Google style
- requirements.txt específico
- Testing básico

---

## 🎯 MINI GOALS POR DÍA

**Día 1**: Setup + APIs (Fase 1)
**Día 2**: Análisis + NLP (Fase 2)
**Día 3**: Visualizaciones (Fase 3)
**Día 4**: App Streamlit (Fase 4)
**Día 5**: Documentación + Deploy (Fase 5)

---

## 📞 PREGUNTAS FRECUENTES RÁPIDAS

**¿Puedo usar otra API de letras?**
No, requisitos especifican lyrics.ovh

**¿Puedo usar solo CSV local?**
No, necesita APIs externas integradas

**¿Cuántos artistas analizar?**
Min 2-3, idealmente 5+

**¿Notebooks son obligatorios?**
Sí, requiere 2 notebooks comentados

**¿Cuál es la nota máxima?**
10/10 si cumples todo + bonus (embeddings, clustering, etc)

---

## 🚀 PRÓXIMO PASO

1. Lee `PROJECT_STRUCTURE.md` (arquitectura general)
2. Lee `MASTER_PROMPTS.md` (prompts específicos)
3. Sigue `EXECUTION_GUIDE.md` (paso a paso)
4. **Abre Claude Code y comienza por PROMPT 1.1**

---

**¡A por los 10 puntos! 🎵**
