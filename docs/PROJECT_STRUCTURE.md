# 🎵 Spotify Music Intelligence Project
## Arquitectura con Claude Code Agents + Skills

---

## 📊 VISIÓN GENERAL

**Objetivo**: Convertir un notebook Colab en una aplicación web completa con análisis musical avanzado.

**Stack**:
- Backend: Python (pandas, scikit-learn, nltk)
- APIs: Spotify Web API, lyrics.ovh
- Frontend: Streamlit
- Deployment: Streamlit Cloud / Railway

**Puntuación**: 10/10 (requiere todo funcionar perfectamente)

---

## 🏗️ ESTRUCTURA DE CARPETAS

```
spotify-music-intelligence/
├── src/
│   ├── __init__.py
│   ├── config.py                    # Credenciales, constantes
│   ├── spotify_api.py               # Integración Spotify
│   ├── lyrics_handler.py            # Integración lyrics.ovh
│   ├── data_processor.py            # Filtrado, limpieza de datos
│   ├── nlp_analyzer.py              # NLP y análisis de letras
│   ├── visualization.py             # Gráficos Plotly/Altair
│   └── utils.py                     # Helper functions
├── notebooks/
│   ├── 01_spotify_exploration.ipynb # Notebook base mejorado
│   └── 02_lyrics_analysis.ipynb     # Análisis de letras
├── app/
│   ├── main.py                      # App principal Streamlit
│   ├── pages/
│   │   ├── 01_Album_Catalogue.py
│   │   ├── 02_Audio_Features.py
│   │   ├── 03_Lyrics_Analysis.py
│   │   └── 04_Artist_Comparison.py
│   └── components/
│       ├── header.py
│       ├── sidebar.py
│       └── metrics.py
├── data/
│   ├── cache/                       # Cache de resultados
│   └── sample/                      # Datos de ejemplo
├── tests/
│   ├── test_spotify.py
│   ├── test_lyrics.py
│   └── test_analysis.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── deployment.md
```

---

## 🤖 ESTRUCTURA DE AGENTES CLAUDE CODE

### **Agent 1: Data Foundation Engineer** ⚙️
**Responsabilidad**: Construir la base de datos y APIs

**Skills necesarios**:
1. `setup_project_structure` - Crear carpetas, archivos base
2. `build_spotify_integration` - Implementar conexión API Spotify
3. `build_lyrics_integration` - Implementar connection lyrics.ovh
4. `create_data_layer` - Cacheo, almacenamiento local

**Prompts clave**:
- "Crea la estructura completa del proyecto con todas las carpetas y archivos base"
- "Implementa la conexión a Spotify API con manejo robusto de errores y rate limiting"
- "Integra lyrics.ovh con fallbacks si la API no responde"
- "Crea un sistema de caché para evitar re-descargar datos"

---

### **Agent 2: Analysis & NLP Specialist** 📊
**Responsabilidad**: Lógica de filtrado, análisis de datos, NLP

**Skills necesarios**:
1. `implement_album_filtering` - Filtrar solo estudios
2. `build_nlp_pipeline` - Procesar letras
3. `create_analysis_functions` - Estadísticas, sentimiento, TF-IDF
4. `generate_embeddings` - Word embeddings, clustering

**Prompts clave**:
- "Implementa el filtrado de álbumes de estudio según requisito 1"
- "Crea un pipeline NLP completo: limpieza, tokenización, stopwords, stemming"
- "Implementa análisis de sentimiento, frecuencia de palabras, TF-IDF"
- "Genera embeddings word2vec y clustering de canciones"

---

### **Agent 3: Visualization Maestro** 🎨
**Responsabilidad**: Gráficos interactivos y visualizaciones

**Skills necesarios**:
1. `create_plotly_charts` - Gráficos Plotly avanzados
2. `create_altair_dashboards` - Dashboards interactivos
3. `build_wordcloud_viz` - Nubes de palabras
4. `create_comparison_visuals` - Comparativas entre artistas

**Prompts clave**:
- "Crea visualizaciones Plotly: nube de palabras, heatmaps, scatter plots"
- "Implementa dashboards Altair interactivos con selección dinámica"
- "Genera comparativas visuales entre artistas (vocabulario, sentimiento, etc)"
- "Crea gráficos temporales de evolución de sonido y letras"

---

### **Agent 4: Frontend & App Builder** 🎯
**Responsabilidad**: Aplicación Streamlit completa

**Skills necesarios**:
1. `build_streamlit_app` - Estructura principal
2. `create_page_components` - Páginas individuales
3. `build_interactive_filters` - Selectores, multiselect, sliders
4. `create_sidebar_navigation` - Navegación modular

**Prompts clave**:
- "Crea la app Streamlit con sidebar, páginas multipage y navegación"
- "Implementa página 1: catálogo de álbumes con filtros dinámicos"
- "Implementa página 2: análisis de features de audio con gráficos interactivos"
- "Implementa página 3: análisis de letras con todas las visualizaciones"
- "Implementa página 4: comparación de artistas lado a lado"

---

### **Agent 5: Notebook & Documentation** 📖
**Responsabilidad**: Notebooks y documentación académica

**Skills necesarios**:
1. `enhance_colab_notebook` - Mejorar notebook base
2. `create_academic_comments` - Comentarios para memoria
3. `generate_deployment_guide` - Instrucciones de despliegue
4. `create_requirements_files` - requirements.txt, setup.py

**Prompts clave**:
- "Convierte el notebook Radiohead en una solución modular y escalable"
- "Agrega explicaciones detalladas de cada sección"
- "Genera comentarios académicos para una memoria de 15 páginas"
- "Crea instrucciones paso a paso para desplegar en Streamlit Cloud, Railway y HF Spaces"

---

## 🔄 FLUJO DE EJECUCIÓN

```
START
  ↓
[Agent 1] Setup → Crea estructura, carpetas, archivos base
  ↓
[Agent 1] APIs → Implementa Spotify + lyrics.ovh
  ↓
[Agent 2] Análisis → Filtrado, procesamiento de datos, NLP
  ↓
[Agent 3] Visualización → Gráficos y dashboards
  ↓
[Agent 4] Frontend → App Streamlit
  ↓
[Agent 5] Documentación → Notebooks, memoria, guías
  ↓
FINAL: App funcional + documentación + guías de deploy
```

---

## 📋 PROMPTS ORDENADOS POR PRIORIDAD

### FASE 1: Fundación (Agent 1)
```
1. "Crea la estructura completa del proyecto Python siguiendo esta organización..."
2. "Implementa spotify_api.py con métodos para obtener artista, álbumes, tracks"
3. "Implementa lyrics_handler.py integrando lyrics.ovh con reintentos"
4. "Crea config.py con variables de entorno y constantes"
```

### FASE 2: Análisis (Agent 2)
```
5. "Implementa album_filter() que solo devuelva álbumes de estudio según criterios"
6. "Crea data_processor.py para limpieza y validación de datos"
7. "Implementa nlp_analyzer.py con pipeline completo de procesamiento de letras"
8. "Crea analysis functions: sentimiento, TF-IDF, n-gramas, embeddings"
```

### FASE 3: Visualización (Agent 3)
```
9. "Crea visualization.py con funciones para Plotly: nubes, heatmaps, scatter"
10. "Implementa dashboards Altair interactivos"
11. "Genera gráficos de comparación entre artistas"
12. "Crea gráficos temporales de evolución musical"
```

### FASE 4: App (Agent 4)
```
13. "Crea app Streamlit con estructura multipage"
14. "Implementa página Album Catalogue con tabla interactiva"
15. "Implementa página Audio Features con gráficos dinámicos"
16. "Implementa página Lyrics Analysis con visualizaciones"
17. "Implementa página Artist Comparison con selección múltiple"
18. "Integra sidebar con navegación y selectores globales"
```

### FASE 5: Documentación (Agent 5)
```
19. "Convierte el notebook Spotify en versión mejorada y modular"
20. "Crea notebook de análisis de letras"
21. "Genera comentarios académicos para memoria"
22. "Crea deployment.md con instrucciones para 4 plataformas"
23. "Genera requirements.txt final"
```

---

## 🎯 METRICAS DE EXITO

✅ **Agent 1**: APIs funcionando, sin errores de rate limit
✅ **Agent 2**: Filtrado correcto (solo estudios), análisis NLP sin bugs
✅ **Agent 3**: 10+ visualizaciones interactivas, responsive
✅ **Agent 4**: App sin crashes, carga <2seg, código limpio
✅ **Agent 5**: Documentación clara, despliegue funcional

---

## 💡 TIPS IMPORTANTES

1. **Rate Limiting**: Implementar delays y caché para evitar bloqueos
2. **Error Handling**: Try-except en todas las API calls
3. **Testing**: Crear tests unitarios para cada módulo
4. **Modularidad**: Cada skill debe producir código reutilizable
5. **Documentación**: Docstrings en todas las funciones
6. **Validación**: Validar entrada de usuarios en UI

---

## 🚀 PRÓXIMOS PASOS

1. Crear archivo de prompts maestro (ver sección siguiente)
2. Ejecutar agentes en secuencia
3. Revisar outputs de cada agente
4. Integrar y testear
5. Desplegar
