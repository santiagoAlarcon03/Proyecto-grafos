# NASA Burro Space Explorer 🚀🫏

Sistema de navegación interestelar para el burro explorador de la NASA.

## 📋 Descripción

Este proyecto implementa un sistema completo que permite calcular y simular rutas óptimas entre estrellas de diferentes constelaciones, considerando múltiples restricciones como energía, tiempo de vida, alimentación y estado de salud del explorador.

## 🎯 Funcionalidades Principales

### ✅ Punto 1: Visualización del Grafo Estelar
- Carga automática de archivo JSON con datos de constelaciones
- Representación gráfica en tablero de coordenadas (escalable, mínimo 200x200 um)
- Colores únicos por constelación
- Identificación de estrellas compartidas (color rojo)
- Resaltado de estrellas hipergigantes

### ✅ Punto 2: Maximizar Estrellas Visitadas
- Algoritmo DFS modificado con backtracking
- Cálculo de ruta que permite conocer la mayor cantidad de estrellas antes de morir
- Consideración de:
  - Estado de salud inicial
  - Energía (burroenergía)
  - Pasto disponible
  - Tiempo de vida

### ✅ Punto 3: Minimizar Costo
- Algoritmo greedy optimizado
- Ruta que maximiza estrellas visitadas con menor gasto
- Gestión inteligente de alimentación (cuando energía < 50%)
- Ganancia de energía variable según estado de salud:
  - Excelente: 5% por kg de pasto
  - Buena: 3% por kg de pasto
  - Mala: 2% por kg de pasto
- Restricción: cada estrella se visita solo UNA vez

### ✨ Funcionalidades Adicionales

#### Simulación Paso a Paso
- Control manual del avance del viaje
- Visualización en tiempo real de la posición del burro
- Actualización dinámica del estado (energía, salud, pasto, edad)

#### Sistema de Investigación
- Efectos de investigación modificables por el científico
- Ganancia/pérdida de tiempo de vida por experimentos
- Consumo de energía por actividades investigativas

#### Estrellas Hipergigantes
- Máximo 2 por constelación
- Recarga del 50% de energía actual
- Duplicación de pasto en bodega
- Capacidad de teletransporte entre galaxias

#### Sistema de Muerte
- Sonido de muerte del burro
- Alertas visuales
- Registro en log de simulación

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI**: Framework web moderno y rápido
- **NetworkX**: Gestión y análisis de grafos
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI

### Frontend
- **HTML5 + Tailwind CSS**: Interfaz responsive
- **JavaScript (Vanilla)**: Lógica de UI
- **D3.js**: Visualización interactiva del grafo

## 📁 Estructura del Proyecto

```
Grafos/
├── app/
│   ├── main.py                 # Servidor FastAPI
│   ├── models.py               # Modelos Pydantic
│   ├── graph_logic.py          # Lógica del grafo (NetworkX)
│   ├── algorithms.py           # Algoritmos de optimización
│   ├── simulation.py           # Motor de simulación
│   ├── utils.py                # Funciones auxiliares
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css      # Estilos personalizados
│   │   └── js/
│   │       ├── graph.js        # Visualización D3.js
│   │       ├── simulation.js   # Control de simulación
│   │       └── ui.js           # Manejo de UI
│   └── templates/
│       └── index.html          # Página principal
├── data/
│   └── constellations_example.json  # Archivo de ejemplo
├── requirements.txt            # Dependencias Python
└── README.md                   # Documentación
```

## 🚀 Instalación y Ejecución

### 1. Instalar Dependencias

```powershell
pip install -r requirements.txt
```

### 2. Ejecutar el Servidor

```powershell
cd app
python main.py
```

O con uvicorn directamente:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Abrir en el Navegador

```
http://localhost:8000
```

## 📖 Guía de Uso

### Paso 1: Cargar Archivo JSON
1. Click en "Seleccionar archivo"
2. Elegir archivo JSON con formato válido
3. Click en "Cargar Archivo"
4. El grafo se visualizará automáticamente

### Paso 2: Calcular Ruta
1. Ingresar ID de estrella origen
2. Seleccionar algoritmo:
   - **Maximizar Estrellas**: Visita más estrellas (Punto 2)
   - **Minimizar Costo**: Optimiza recursos (Punto 3)
3. Click en "Calcular Ruta"
4. La ruta se resaltará en el grafo

### Paso 3: Simular Viaje
1. Click en "Iniciar Viaje"
2. Usar "Siguiente Paso" para avanzar
3. Observar cambios en estado del burro
4. Ver log de eventos en tiempo real

### Características Interactivas
- **Click en estrella**: Auto-completa ID de origen
- **Hover en estrella**: Ver información detallada
- **Zoom**: Scroll del mouse en el grafo
- **Pan**: Arrastrar el grafo

## 📄 Formato del Archivo JSON

```json
{
  "constellations": [
    {
      "name": "Nombre de la Constelación",
      "starts": [
        {
          "id": 1,
          "label": "Nombre Estrella",
          "linkedTo": [
            {"starId": 2, "distance": 120}
          ],
          "radius": 0.5,
          "timeToEat": 2,
          "amountOfEnergy": 1.5,
          "coordenates": {"x": 25, "y": 34},
          "hypergiant": false,
          "lifeYearsGained": 0,
          "lifeYearsLost": 0
        }
      ]
    }
  ],
  "burroenergiaInicial": 100,
  "estadoSalud": "Excelente",
  "pasto": 300,
  "number": 123,
  "startAge": 12,
  "deathAge": 3567
}
```

## 🔍 Algoritmos Implementados

### Punto 2: DFS con Backtracking
```python
def maximize_stars_visited(origin):
    - Explora todas las rutas posibles
    - Poda ramas que conducen a muerte prematura
    - Retorna ruta con mayor cantidad de estrellas
```

### Punto 3: Greedy Optimizado
```python
def minimize_cost_route(origin):
    - Selección voraz del siguiente nodo
    - Considera costo = distancia + energía - ganancia_pasto
    - Visita cada estrella solo una vez
```

## 🎨 Características de Visualización

- **Colores por Constelación**: Cada constelación tiene color único
- **Estrellas Compartidas**: Resaltadas en rojo
- **Hipergigantes**: Borde dorado pulsante
- **Posición del Burro**: Marcador verde animado
- **Ruta Calculada**: Resaltada en verde

## 🧪 Casos de Prueba

Se incluye archivo `constellations_example.json` con:
- 2 constelaciones
- 15 estrellas totales
- 1 estrella compartida (ID 3)
- 2 estrellas hipergigantes

## 📊 Estados de Salud

| Energía | Estado | Ganancia por kg |
|---------|--------|-----------------|
| 75-100% | Excelente | 5% |
| 50-74% | Buena | 3% |
| 25-49% | Mala | 2% |
| 1-24% | Moribundo | 1% |
| 0% | Muerto | 0% |

## 🐛 Solución de Problemas

### El grafo no se visualiza
- Verificar formato del JSON
- Revisar consola del navegador (F12)
- Asegurar que todas las dependencias estén instaladas

### Error al calcular ruta
- Verificar que el ID de estrella existe
- Comprobar que el grafo esté conectado
- Revisar que haya suficiente energía/pasto

### Simulación no avanza
- Verificar que se haya calculado una ruta primero
- Comprobar que el burro no esté muerto

## 👥 Autores

Santiago Alarcón - Universidad Nacional de Colombia
Estructuras de Datos - Grafos

## 📝 Licencia

Proyecto académico - Universidad Nacional de Colombia

## 🙏 Agradecimientos

- NASA (inspiración temática)
- Burros espaciales (motivación)
- Comunidad D3.js
- FastAPI Framework
