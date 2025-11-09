# Guía de Desarrollo - NASA Burro Space Explorer

## 🎯 Arquitectura del Sistema

### 1. **Capa de Datos (models.py)**
Define las estructuras de datos usando Pydantic:
- `Star`: Representa una estrella con sus propiedades
- `Constellation`: Agrupa estrellas en constelaciones
- `ConstellationData`: Datos completos del JSON
- `DonkeyState`: Estado del burro durante la simulación

### 2. **Capa de Grafo (graph_logic.py)**
Gestiona la representación del espacio como un grafo:
- Construcción del grafo con NetworkX
- Identificación de estrellas compartidas
- Detección de hipergigantes
- Preparación de datos para visualización

### 3. **Capa de Algoritmos (algorithms.py)**
Implementa los algoritmos de optimización:
- **DFS con Backtracking**: Maximizar estrellas visitadas
- **Greedy Optimizado**: Minimizar costo de viaje

### 4. **Capa de Simulación (simulation.py)**
Control paso a paso del viaje:
- Ejecución secuencial de pasos
- Actualización de estado del burro
- Gestión de alimentación y energía
- Log de eventos

### 5. **Capa de API (main.py)**
Endpoints REST con FastAPI:
```
POST /api/upload              - Cargar JSON
GET  /api/graph-data          - Obtener datos del grafo
POST /api/calculate-route     - Calcular ruta óptima
POST /api/start-simulation    - Iniciar simulación
GET  /api/simulation/next     - Siguiente paso
GET  /api/simulation/summary  - Resumen de simulación
PUT  /api/star/update-effects - Modificar efectos de estrella
```

### 6. **Capa de Presentación (Frontend)**
Interfaz web interactiva:
- **graph.js**: Visualización con D3.js
- **simulation.js**: Control de simulación
- **ui.js**: Manejo de eventos y UI

## 🔬 Detalles de Implementación

### Algoritmo: Maximizar Estrellas (Punto 2)

```python
def maximize_stars_visited(origin):
    """
    Usa DFS con backtracking y poda agresiva
    
    Complejidad: O(V * E) en el peor caso
    donde V = vértices, E = aristas
    
    Optimizaciones:
    - Poda temprana si el burro moriría
    - Caché de estados visitados
    - Priorización de rutas prometedoras
    """
```

**Criterios de poda:**
1. Si `edad + distancia >= edad_muerte` → Podar
2. Si `energía - costo <= 0` y sin pasto → Podar
3. Si ya se visitó toda la vecindad → Retroceder

### Algoritmo: Minimizar Costo (Punto 3)

```python
def minimize_cost_route(origin):
    """
    Greedy con función de costo personalizada
    
    Costo = distancia + energía_consumida - (ganancia_pasto * peso)
    
    Complejidad: O(V²) donde V = número de vértices
    
    Consideraciones:
    - Cada estrella se visita una sola vez
    - Alimentación automática si energía < 50%
    - Selección del vecino con menor costo viable
    """
```

**Heurística de selección:**
```
Para cada vecino no visitado:
    1. Calcular costo del viaje
    2. Estimar energía tras llegada
    3. Considerar ganancia por alimentación
    4. Seleccionar el de menor costo total
```

### Sistema de Energía

```python
# Ganancia por kg de pasto según salud
rates = {
    'Excelente': 5.0,
    'Buena': 3.0,
    'Mala': 2.0,
    'Moribundo': 1.0,
    'Muerto': 0.0
}

# Actualización de salud según energía
if energy >= 75: health = 'Excelente'
elif energy >= 50: health = 'Buena'
elif energy >= 25: health = 'Mala'
elif energy > 0: health = 'Moribundo'
else: health = 'Muerto'
```

### Gestión de Hipergigantes

```python
if star.hypergiant and donkey.is_alive:
    # Recarga de energía (50% del actual)
    donkey.energy = min(100, donkey.energy * 1.5)
    
    # Duplicar pasto
    donkey.grass *= 2
    
    # Posibilidad de teletransporte
    # (implementado en UI para selección de científico)
```

## 🎨 Personalización

### Agregar Nuevo Algoritmo

1. **Crear función en `algorithms.py`:**
```python
def my_custom_algorithm(self, origin: int):
    # Tu implementación
    route = []
    stats = {}
    return route, stats
```

2. **Agregar endpoint en `main.py`:**
```python
@app.post("/api/my-algorithm")
async def my_algorithm(origin: int):
    optimizer = RouteOptimizer(current_graph, initial_state)
    route, stats = optimizer.my_custom_algorithm(origin)
    return JSONResponse({"route": route, "stats": stats})
```

3. **Actualizar UI en `ui.js`:**
```javascript
// Agregar opción al select
<option value="my_algorithm">Mi Algoritmo</option>
```

### Modificar Visualización

**Cambiar colores de constelaciones:**
```python
# En graph_logic.py, método _assign_constellation_colors
colors = ['#color1', '#color2', ...]  # Tus colores
```

**Ajustar tamaño de nodos:**
```javascript
// En graph.js, método render
.attr('r', d => tu_formula(d.radius))
```

## 🧪 Testing

### Pruebas Unitarias

```python
# tests/test_algorithms.py
import pytest
from app.graph_logic import SpaceGraph
from app.algorithms import RouteOptimizer

def test_maximize_stars():
    # Cargar datos de prueba
    # Ejecutar algoritmo
    # Validar resultados
    assert len(route) > 0
    assert stats['stars_visited'] == expected
```

### Pruebas de Integración

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_json():
    with open('data/test.json', 'rb') as f:
        response = client.post('/api/upload', files={'file': f})
    assert response.status_code == 200
```

## 📊 Métricas de Rendimiento

### Complejidad Temporal

| Operación | Complejidad | Notas |
|-----------|-------------|-------|
| Cargar JSON | O(V + E) | V=vértices, E=aristas |
| Construir Grafo | O(V + E) | NetworkX |
| Maximizar Estrellas | O(V!) | Con poda: O(V²E) |
| Minimizar Costo | O(V²) | Greedy |
| Simulación Paso | O(1) | Por paso |
| Visualización | O(V + E) | D3.js |

### Complejidad Espacial

| Estructura | Espacio |
|------------|---------|
| Grafo | O(V + E) |
| Estados visitados | O(V) |
| Log de simulación | O(pasos) |

## 🔧 Optimizaciones Posibles

### 1. Caché de Rutas
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def calculate_route_cached(origin, algorithm):
    # Calcular ruta
    pass
```

### 2. Procesamiento Paralelo
```python
from concurrent.futures import ThreadPoolExecutor

def parallel_route_search(origins):
    with ThreadPoolExecutor() as executor:
        routes = executor.map(calculate_route, origins)
    return list(routes)
```

### 3. Índices Espaciales
```python
from scipy.spatial import KDTree

# Para búsqueda rápida de estrellas cercanas
points = [(star.x, star.y) for star in stars]
kdtree = KDTree(points)
neighbors = kdtree.query_ball_point([x, y], radius)
```

## 🐛 Debugging

### Logs Útiles

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Estado actual: {donkey_state}")
logger.info(f"Ruta calculada: {route}")
logger.warning(f"Energía baja: {energy}%")
logger.error(f"Error al procesar: {error}")
```

### Herramientas

- **FastAPI Docs**: `http://localhost:8000/docs`
- **Chrome DevTools**: Network, Console, Performance
- **NetworkX Visualization**: Para depurar grafo
- **Postman/Insomnia**: Probar endpoints

## 📚 Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [NetworkX Tutorial](https://networkx.org/documentation/stable/tutorial.html)
- [D3.js Examples](https://observablehq.com/@d3/gallery)
- [Pydantic Guide](https://docs.pydantic.dev/)

## 🤝 Contribuir

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -am 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## ❓ FAQ

**P: ¿Por qué NetworkX y no implementar el grafo desde cero?**
R: NetworkX ofrece algoritmos optimizados y bien probados. Para propósitos académicos, se puede reemplazar con implementación propia.

**P: ¿Cómo agregar más constelaciones?**
R: Edita el JSON agregando objetos al array `constellations`.

**P: ¿El burro puede revivir?**
R: No, una vez muerto la simulación termina.

**P: ¿Puedo usar otros algoritmos de pathfinding?**
R: Sí, implementa tu algoritmo en `algorithms.py` siguiendo el patrón existente.
