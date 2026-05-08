# 🎵 Spotify Music Intelligence - Sistema de Agentes con Claude Code

## 🎯 RESUMEN EJECUTIVO

Has dado los archivos de tu práctica universitaria a Claude. Aquí tienes un **sistema completo de agentes automatizados** que usarás con **Claude Code** para:

1. ✅ **Completar la práctica** (filtrado de álbumes + análisis de letras + web app)
2. ✅ **Obtener nota alta** (10/10 con implementación profesional)
3. ✅ **Aprender** cómo hacer un proyecto real de Data Science

---

## 📦 QUÉ HE CREADO PARA TI

He generado **4 archivos maestros**:

| Archivo | Descripción | Cuándo usarlo |
|---------|------------|--------------|
| **PROJECT_STRUCTURE.md** | Arquitectura del proyecto + 5 agentes especializados | Léelo primero para entender el plan |
| **MASTER_PROMPTS.md** | 15+ prompts listos para copiar-pegar en Claude Code | Para ejecutar cada fase |
| **EXECUTION_GUIDE.md** | Guía paso-a-paso con ejemplos prácticos | Para saber exactamente qué hacer |
| **CHEATSHEET.md** | Referencias rápidas, comandos, links | Para consultar mientras desarrollas |

---

## 🚀 CÓMO FUNCIONA

### La Idea: 5 Agentes Especializados

No harás todo tú. En su lugar:

1. **Agent 1: Data Foundation Engineer** → Crea APIs, setup
2. **Agent 2: Analysis & NLP Specialist** → Filtrado, análisis
3. **Agent 3: Visualization Maestro** → Gráficos bonitos
4. **Agent 4: Frontend & App Builder** → Streamlit
5. **Agent 5: Notebook & Documentation** → Documentación

Cada agente:
- ✅ Es un **conjunto de prompts especializados**
- ✅ Genera **código reutilizable y profesional**
- ✅ Se **comunica con Claude Code** (no conmigo)
- ✅ Depende del anterior (orden importa)

### El Flujo

```
Tú (en Claude Code)
    ↓
Copias PROMPT 1.1 de MASTER_PROMPTS.md
    ↓
Claude Code lo ejecuta
    ↓
Genera archivo src/config.py + estructura
    ↓
Verificas que funciona
    ↓
Avanzas a PROMPT 1.2
    ↓
... repites hasta Phase 5
    ↓
App completamente funcional + documentada
```

---

## ⚡ QUICK START (5 min)

### Paso 1: Lee el Plan (15 min)
```
Abre PROJECT_STRUCTURE.md
Entiende los 5 agentes y sus skills
```

### Paso 2: Abre Claude Code
```
Si estás en claude.ai → tools/Claude Code
Si tienes Desktop → ya está disponible
```

### Paso 3: Comienza Phase 1
```
Ve a EXECUTION_GUIDE.md → Fase 1: Data Foundation
Copia el primer prompt
Pégalo en Claude Code
Ejecuta
```

### Paso 4: Itera
```
Una vez que termina:
- Verifica que funciona: ls -la src/
- Commit a git: git add . && git commit -m "..."
- Próximo prompt
```

---

## 📋 ORDEN DE LECTURA RECOMENDADO

1. **Este archivo** (README_START_HERE.md) ← Estás aquí ✓
2. **PROJECT_STRUCTURE.md** → Entiende la arquitectura
3. **EXECUTION_GUIDE.md** → Fase 1 hasta Fase 5
4. **MASTER_PROMPTS.md** → Cuando necesites el prompt exacto
5. **CHEATSHEET.md** → Cuando necesites referencias rápidas

---

## 🎓 REQUISITOS UNIVERSITARIOS

Tu práctica necesita:

### 1. Filtrado de Álbumes (2 puntos)
- ✅ Solo álbumes de estudio
- ✅ Excluir compilations, live, singles, etc
- ✅ Algoritmo explicado
- 📍 **Agent 2** lo implementa en PROMPT 2.1

### 2. Análisis de Letras (4 puntos)
- ✅ API lyrics.ovh integrada
- ✅ Análisis NLP completo (sentimiento, TF-IDF, embeddings)
- ✅ 10+ visualizaciones interactivas
- ✅ Comparativa entre artistas
- 📍 **Agent 2 + Agent 3** lo hacen en PROMPTS 2.2-3.2

### 3. Web App (4 puntos)
- ✅ Streamlit funcional
- ✅ 4 páginas: Album Catalogue, Audio Features, Lyrics, Comparison
- ✅ Filtros dinámicos
- ✅ Gráficos interactivos
- ✅ Deployable
- 📍 **Agent 4** lo hace en PROMPTS 4.1-4.6

---

## 🎯 TIMELINE ESTIMADO

| Fase | Agent | Tiempo | Salida |
|------|-------|--------|--------|
| 1 | Agent 1 | 2-3h | APIs + estructura |
| 2 | Agent 2 | 3-4h | Análisis + filtrado |
| 3 | Agent 3 | 2-3h | Visualizaciones |
| 4 | Agent 4 | 4-5h | App Streamlit |
| 5 | Agent 5 | 2-3h | Documentación |
| **TOTAL** | | **13-18h** | **Proyecto completo** |

Con Claude Code, **mucho más rápido** (estimas reales: 5-10h).

---

## 💡 VENTAJAS DE ESTE ENFOQUE

### Para ti:
- ✅ **No empiezas de cero** (tienes un plan)
- ✅ **Código profesional** (no cosas improvisadas)
- ✅ **Modular y reutilizable** (estructura clara)
- ✅ **Notas altas** (requisitos 100% cubiertos)
- ✅ **Documentado** (fácil de explicar)

### Para los profesores:
- ✅ **Proyecto coherente** (no partes sueltas)
- ✅ **Código limpio** (docstrings, type hints, tests)
- ✅ **Análisis profundo** (NLP, embeddings, clustering)
- ✅ **Visualmente impactante** (Plotly, Altair, nubes)
- ✅ **Deployable** (Streamlit Cloud, Railway, etc)

---

## 🔧 TECNOLOGÍAS USADAS

**Backend**:
- Python 3.11+
- pandas, numpy (datos)
- scikit-learn (ML)
- nltk, gensim (NLP)
- spotipy (Spotify API)
- requests (HTTP)

**Frontend**:
- Streamlit (web app)
- Plotly (gráficos)
- Altair (dashboards)
- WordCloud

**Infrastructure**:
- GitHub (versionado)
- Streamlit Cloud (deploy)
- .env (variables de entorno)

**Documentación**:
- Jupyter Notebooks
- Markdown
- Docstrings Google style

---

## 🚀 PRÓXIMOS PASOS

### HOY (próximas 2 horas):
1. Lee PROJECT_STRUCTURE.md
2. Abre Claude Code
3. Ejecuta PROMPT 1.1 (setup)
4. Verifica que se creen las carpetas

### MAÑANA:
5. PROMPTS 1.2-1.4 (APIs)
6. Testea que conecta a Spotify

### DÍA 3-4:
7. PROMPTS 2.1-2.3 (análisis)
8. PROMPTS 3.1-3.2 (visualización)

### DÍA 5:
9. PROMPTS 4.1-4.6 (app)
10. Streamlit run app/main.py

### DÍA 6-7:
11. PROMPTS 5.1-5.5 (documentación)
12. Deploy en Streamlit Cloud

---

## ⚠️ COSAS IMPORTANTES

### ✅ HACER:
- Ejecutar un prompt a la vez
- Verificar que funciona antes del siguiente
- Commitear a git después de cada fase
- Testear básicamente (imports, structure)
- Leer los outputs de Claude Code

### ❌ NO HACER:
- Ejecutar todo de una vez
- Saltar pasos
- Ignorar errores
- Cambiar la estructura sin razón
- Copiar código sin entender

---

## 📞 SI TIENES DUDAS

**Pregunta: ¿Qué es Claude Code?**
R: Es una herramienta integrada en claude.ai que ejecuta bash y Python en un terminal.

**Pregunta: ¿Necesito instalar algo?**
R: No. Claude Code maneja todo. Solo necesitas los prompts.

**Pregunta: ¿Puedo cambiar la arquitectura?**
R: Sí, pero la estructura propuesta está optimizada. Cámbiala solo si realmente necesitas.

**Pregunta: ¿Cuándo necesito credenciales de Spotify?**
R: En PROMPT 1.2. Ve a https://developer.spotify.com

**Pregunta: ¿Funciona sin conexión a internet?**
R: No. Necesita Spotify API y lyrics.ovh. Pero puedes usar datos cachés locales.

---

## 📊 CHECKLIST PARA EMPEZAR

- [ ] He leído este archivo (README_START_HERE.md)
- [ ] He abierto PROJECT_STRUCTURE.md
- [ ] Entiendo los 5 agentes
- [ ] He abierto Claude Code
- [ ] Tengo MASTER_PROMPTS.md a mano
- [ ] Tengo EXECUTION_GUIDE.md a mano
- [ ] Estoy listo para PROMPT 1.1

---

## 🎓 VALOR ACADÉMICO ESPERADO

Este proyecto demuestra:

✅ **Ingeniería de Software**
- Arquitectura modular
- Buenas prácticas (DRY, SOLID)
- Testing y CI/CD

✅ **Data Science**
- APIs externas
- Limpieza y procesamiento
- Análisis estadístico
- Machine Learning (embeddings, clustering)

✅ **NLP**
- Tokenización, stemming, lemmatization
- Sentiment analysis
- TF-IDF, n-gramas
- Word embeddings

✅ **Visualización**
- Gráficos interactivos
- Dashboards
- Análisis exploratorio

✅ **Full Stack**
- Backend (Python)
- Frontend (Streamlit)
- Deployment
- Documentación

---

## 🌟 DIFERENCIAL (Para nota 10/10)

Si implementas BONUS:

1. **Clustering de canciones** (K-means sobre embeddings)
2. **PCA/t-SNE** (visualizar songs en 2D)
3. **Topic Modeling** (LDA en letras)
4. **Semantic Similarity** (cosine similarity entre songs)
5. **Audio fingerprinting** (comparar covers)
6. **Spike Detection** (detectar cambios de estilo)
7. **Deploy en múltiples plataformas** (Cloud + Railway + HF)

Estos no son requisitos pero **suben mucho la nota**.

---

## 🎬 CÓMO EXPLICAR LA PRÁCTICA

Cuando tengas que presentar/defender:

**"Creé un sistema de análisis musical usando APIs externas..."**

1. Explica las 5 fases
2. Muestra la arquitectura
3. Haz demo de la app
4. Explica un análisis detallado (ej: Radiohead)
5. Explica las decisiones técnicas
6. Mencionas que es deployable

**Eso impresiona mucho más que "lo hice todo tú solo".**

---

## 📚 RECURSOS ADICIONALES

Si necesitas profundizar:

- Spotify API docs: https://developer.spotify.com/documentation
- NLTK Book: https://www.nltk.org/book/
- Streamlit Docs: https://docs.streamlit.io/
- Plotly Docs: https://plotly.com/python/

---

## ✨ ÚLTIMA COSA

**Este no es un sistema mágico**. Es una **guía estructurada y profesional** para que:

1. No te pierdas en camino (fases claras)
2. Generes código profesional (prompts + buenas prácticas)
3. Aprendas en el proceso (entiende lo que se crea)
4. Presentes un proyecto impactante (polished + documentado)

**Tú eres el que decide**. Puedo crear código, pero tú debes entenderlo.

---

## 🚀 ¡A EMPEZAR!

**Siguiente paso:**

1. Abre `PROJECT_STRUCTURE.md`
2. Lee los 5 agentes
3. Abre Claude Code
4. Ejecuta PROMPT 1.1 de `EXECUTION_GUIDE.md`

---

**Good luck! 🎵**

---

*Documento creado: 2025-05-07*  
*Proyecto: Spotify Music Intelligence*  
*Stack: Python + Streamlit + Plotly + NLP*  
*Nota esperada: 9-10/10*
