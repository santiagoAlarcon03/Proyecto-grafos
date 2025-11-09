# 📖 Índice de Documentación
## NASA Burro Space Explorer 🚀🫏

---

## 🎯 ¿Por dónde empezar?

### 👨‍🎓 Si eres ESTUDIANTE o NUEVO USUARIO
➡️ Comienza aquí: **[QUICKSTART.md](QUICKSTART.md)**
- Guía rápida de 5 minutos
- Pasos básicos de uso
- Casos de uso simples

### 👨‍💼 Si eres EVALUADOR o INSTRUCTOR
➡️ Lee esto primero: **[RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)**
- Vista general completa
- Cumplimiento de requisitos
- Métricas del proyecto

### 🔧 Si vas a INSTALAR el proyecto
➡️ Sigue esta guía: **[INSTALL.md](INSTALL.md)**
- Requisitos del sistema
- Instalación paso a paso
- Solución de problemas

### 👨‍💻 Si eres DESARROLLADOR
➡️ Consulta: **[DEVELOPMENT.md](DEVELOPMENT.md)**
- Arquitectura técnica
- Detalles de implementación
- Guía de extensión

### 📚 Para DOCUMENTACIÓN COMPLETA
➡️ Ver: **[README.md](README.md)**
- Descripción detallada
- Todas las funcionalidades
- Ejemplos completos

---

## 📁 Estructura de la Documentación

### Documentos Principales

| Archivo | Propósito | Audiencia | Tiempo de lectura |
|---------|-----------|-----------|-------------------|
| **[QUICKSTART.md](QUICKSTART.md)** | Inicio rápido | Usuarios nuevos | 5 min |
| **[INSTALL.md](INSTALL.md)** | Instalación | Todos | 10 min |
| **[README.md](README.md)** | Documentación completa | Todos | 20 min |
| **[DEVELOPMENT.md](DEVELOPMENT.md)** | Guía técnica | Desarrolladores | 30 min |
| **[RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)** | Vista ejecutiva | Evaluadores | 10 min |

---

## 🗂️ Contenido por Tema

### 🚀 Instalación y Configuración
1. [Requisitos del sistema](INSTALL.md#-requisitos-del-sistema)
2. [Instalación básica](INSTALL.md#-instalación-paso-a-paso)
3. [Instalación con entorno virtual](INSTALL.md#método-2-con-entorno-virtual-mejor-práctica)
4. [Verificación de instalación](INSTALL.md#-verificación-de-instalación)
5. [Solución de problemas](INSTALL.md#-solución-de-problemas)

### 📖 Uso del Sistema
1. [Inicio rápido](QUICKSTART.md#-inicio-rápido-5-minutos)
2. [Carga de datos](QUICKSTART.md#paso-1-cargar-datos)
3. [Cálculo de rutas](QUICKSTART.md#paso-2-calcular-ruta)
4. [Simulación](QUICKSTART.md#paso-3-simular-viaje)
5. [Interpretación de resultados](QUICKSTART.md#-interpretación-de-resultados)

### 🎯 Funcionalidades
1. [Visualización del grafo](README.md#-punto-1-visualización-del-grafo-estelar)
2. [Maximizar estrellas (Punto 2)](README.md#-punto-2-maximizar-estrellas-visitadas)
3. [Minimizar costo (Punto 3)](README.md#-punto-3-minimizar-costo)
4. [Sistema de hipergigantes](README.md#estrellas-hipergigantes)
5. [Efectos de investigación](README.md#sistema-de-investigación)

### 👨‍💻 Desarrollo
1. [Arquitectura del sistema](DEVELOPMENT.md#-arquitectura-del-sistema)
2. [Algoritmos implementados](DEVELOPMENT.md#-detalles-de-implementación)
3. [Personalización](DEVELOPMENT.md#-personalización)
4. [Testing](DEVELOPMENT.md#-testing)
5. [Optimizaciones](DEVELOPMENT.md#-optimizaciones-posibles)

### 📊 Evaluación Académica
1. [Cumplimiento de requisitos](RESUMEN_EJECUTIVO.md#-cumplimiento-de-requisitos)
2. [Aspectos académicos](RESUMEN_EJECUTIVO.md#-aspectos-académicos-destacados)
3. [Métricas de código](RESUMEN_EJECUTIVO.md#-métricas-de-código)
4. [Tests implementados](RESUMEN_EJECUTIVO.md#-testing-y-validación)

---

## 🔍 Búsqueda Rápida

### ¿Cómo hacer...?

**¿Cómo instalar el proyecto?**
→ [INSTALL.md](INSTALL.md#-instalación-paso-a-paso)

**¿Cómo cargar un archivo JSON?**
→ [QUICKSTART.md](QUICKSTART.md#paso-1-cargar-datos)

**¿Cómo calcular una ruta?**
→ [QUICKSTART.md](QUICKSTART.md#paso-2-calcular-ruta)

**¿Cómo funciona el algoritmo del Punto 2?**
→ [DEVELOPMENT.md](DEVELOPMENT.md#algoritmo-maximizar-estrellas-punto-2)

**¿Cómo funciona el algoritmo del Punto 3?**
→ [DEVELOPMENT.md](DEVELOPMENT.md#algoritmo-minimizar-costo-punto-3)

**¿Cómo ejecutar los tests?**
→ [DEVELOPMENT.md](DEVELOPMENT.md#-testing)

**¿Cómo modificar la visualización?**
→ [DEVELOPMENT.md](DEVELOPMENT.md#modificar-visualización)

**¿Cómo agregar un nuevo algoritmo?**
→ [DEVELOPMENT.md](DEVELOPMENT.md#agregar-nuevo-algoritmo)

### Problemas Comunes

**El grafo no se visualiza**
→ [QUICKSTART.md](QUICKSTART.md#el-grafo-no-aparece)

**Error al calcular ruta**
→ [QUICKSTART.md](QUICKSTART.md#error-al-calcular-ruta)

**Error de instalación**
→ [INSTALL.md](INSTALL.md#-solución-de-problemas)

**El servidor no inicia**
→ [INSTALL.md](INSTALL.md#error-address-already-in-use)

---

## 📂 Archivos del Proyecto

### Código Fuente
```
app/
├── main.py              # Servidor FastAPI (API REST)
├── models.py            # Modelos de datos (Pydantic)
├── graph_logic.py       # Lógica del grafo (NetworkX)
├── algorithms.py        # Algoritmos de optimización
├── simulation.py        # Motor de simulación
├── utils.py             # Utilidades
├── static/
│   ├── css/styles.css   # Estilos
│   └── js/
│       ├── graph.js     # Visualización (D3.js)
│       ├── simulation.js # Control simulación
│       └── ui.js        # Interfaz de usuario
└── templates/
    └── index.html       # Página principal
```

### Datos y Tests
```
data/
└── constellations_example.json  # Archivo de ejemplo

tests/
├── __init__.py
└── test_algorithms.py          # Suite de tests
```

### Documentación
```
├── INDEX.md                    # Este archivo (índice)
├── README.md                   # Documentación completa
├── QUICKSTART.md               # Inicio rápido
├── INSTALL.md                  # Instalación
├── DEVELOPMENT.md              # Guía de desarrollo
└── RESUMEN_EJECUTIVO.md        # Resumen ejecutivo
```

### Configuración
```
├── requirements.txt            # Dependencias Python
├── start_server.ps1           # Script de inicio (Windows)
├── .gitignore                 # Git ignore
└── main.py                    # Entry point
```

---

## 🎓 Rutas de Aprendizaje

### Ruta 1: Usuario Final (30 min)
1. Leer [QUICKSTART.md](QUICKSTART.md) (5 min)
2. Instalar según [INSTALL.md](INSTALL.md) (10 min)
3. Probar funcionalidades básicas (10 min)
4. Experimentar con diferentes rutas (5 min)

### Ruta 2: Evaluador (45 min)
1. Leer [RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md) (10 min)
2. Instalar y ejecutar (10 min)
3. Revisar cumplimiento de requisitos (15 min)
4. Probar casos de uso (10 min)

### Ruta 3: Desarrollador (2 horas)
1. Leer [README.md](README.md) (20 min)
2. Leer [DEVELOPMENT.md](DEVELOPMENT.md) (30 min)
3. Revisar código fuente (40 min)
4. Ejecutar tests (10 min)
5. Experimentar con modificaciones (20 min)

### Ruta 4: Contribuidor (3 horas)
1. Completar Ruta 3 (2 horas)
2. Entender arquitectura completa (30 min)
3. Identificar área de mejora (15 min)
4. Planificar contribución (15 min)

---

## 🏷️ Etiquetas por Sección

### Por Dificultad
- 🟢 **Básico**: QUICKSTART.md, INSTALL.md
- 🟡 **Intermedio**: README.md, RESUMEN_EJECUTIVO.md
- 🔴 **Avanzado**: DEVELOPMENT.md

### Por Rol
- 👨‍🎓 **Estudiante**: QUICKSTART.md, README.md
- 👨‍🏫 **Instructor**: RESUMEN_EJECUTIVO.md, DEVELOPMENT.md
- 👨‍💻 **Desarrollador**: DEVELOPMENT.md, código fuente
- 🔧 **Usuario técnico**: INSTALL.md, QUICKSTART.md

### Por Tiempo
- ⚡ **5 min**: QUICKSTART.md
- ⏱️ **10 min**: INSTALL.md, RESUMEN_EJECUTIVO.md
- ⏰ **20 min**: README.md
- 🕐 **30+ min**: DEVELOPMENT.md

---

## 📞 Referencias Rápidas

### Comandos Importantes
```powershell
# Instalar
pip install -r requirements.txt

# Ejecutar
python app/main.py

# Tests
python tests/test_algorithms.py

# Verificar dependencias
python -c "import fastapi, uvicorn, networkx, pydantic"
```

### URLs Importantes
- **Aplicación**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc

### Archivos Clave
- **JSON ejemplo**: `data/constellations_example.json`
- **Entry point**: `app/main.py`
- **Algoritmos**: `app/algorithms.py`
- **Visualización**: `app/static/js/graph.js`

---

## 🆘 Ayuda y Soporte

### Antes de Preguntar
1. ✅ Revisa [QUICKSTART.md](QUICKSTART.md)
2. ✅ Consulta [solución de problemas](INSTALL.md#-solución-de-problemas)
3. ✅ Verifica [FAQ](DEVELOPMENT.md#-faq)
4. ✅ Ejecuta [tests](tests/test_algorithms.py)

### Estructura de Reporte de Errores
```
1. ¿Qué estabas intentando hacer?
2. ¿Qué pasó?
3. ¿Qué esperabas que pasara?
4. ¿Qué dice la consola/log?
5. ¿Has probado soluciones del INSTALL.md?
```

---

## 🎯 Objetivos de Aprendizaje

Al completar este proyecto, habrás aprendido sobre:

✅ **Estructuras de Datos**
- Grafos no dirigidos
- Diccionarios y mapeos
- Conjuntos (sets)

✅ **Algoritmos**
- DFS con backtracking
- Algoritmos greedy
- Dijkstra (camino más corto)

✅ **Desarrollo Web**
- Backend con FastAPI
- Frontend con JavaScript
- Visualización con D3.js

✅ **Ingeniería de Software**
- Arquitectura limpia
- Testing automatizado
- Documentación técnica

---

## 📅 Actualizaciones

**Versión Actual**: 1.0.0  
**Última Actualización**: 7 de Noviembre, 2025  
**Estado**: ✅ Completo y Funcional

---

## 📜 Licencia

Proyecto académico - Universidad Nacional de Colombia  
Estructuras de Datos - Grafos

---

**¡Bienvenido al proyecto NASA Burro Space Explorer!** 🚀🫏

Elige tu ruta de documentación arriba y comienza tu exploración espacial.

---
