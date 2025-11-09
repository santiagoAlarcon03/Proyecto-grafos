# 🚀 Guía Rápida - NASA Burro Space Explorer

## ⚡ Inicio Rápido (5 minutos)

### 1️⃣ Instalación
```powershell
# Instalar dependencias
pip install -r requirements.txt
```

### 2️⃣ Ejecución
```powershell
# Opción 1: Script automático (recomendado)
.\start_server.ps1

# Opción 2: Comando directo
python app/main.py

# Opción 3: Con uvicorn
uvicorn app.main:app --reload
```

### 3️⃣ Abrir navegador
```
http://localhost:8000
```

## 📋 Uso Básico

### Paso 1: Cargar Datos
1. Click en botón de carga
2. Seleccionar `data/constellations_example.json`
3. Click "Cargar Archivo"
4. ✅ El grafo aparece automáticamente

### Paso 2: Calcular Ruta
1. Click en una estrella del grafo (auto-completa ID)
2. O escribir ID manualmente
3. Elegir algoritmo:
   - **Maximizar Estrellas**: Más estrellas visitadas
   - **Minimizar Costo**: Menor gasto de recursos
4. Click "Calcular Ruta"
5. ✅ Ruta resaltada en verde

### Paso 3: Simular Viaje
1. Click "Iniciar Viaje"
2. Click "Siguiente Paso" repetidamente
3. Observar:
   - 🫏 Posición del burro (verde)
   - ⚡ Barra de energía
   - 📊 Estadísticas actualizadas
   - 📝 Log de eventos

## 🎯 Funcionalidades Clave

### Interacción con el Grafo
- **Click**: Seleccionar estrella origen
- **Hover**: Ver información detallada
- **Scroll**: Zoom in/out
- **Drag**: Mover vista

### Tipos de Estrellas
- 🔴 **Roja**: Compartida entre constelaciones
- ⭐ **Dorada**: Hipergigante (recarga energía)
- 🟢 **Verde**: Posición actual del burro

### Estados de Salud
| Energía | Estado | Color |
|---------|--------|-------|
| 75-100% | Excelente | 🟢 Verde |
| 50-74% | Buena | 🔵 Azul |
| 25-49% | Mala | 🟡 Amarillo |
| 1-24% | Moribundo | 🟠 Naranja |
| 0% | Muerto | 🔴 Rojo |

## 🔍 Algoritmos

### Maximizar Estrellas (Punto 2)
- Objetivo: Visitar máximo número de estrellas
- Considera: Energía, tiempo de vida, pasto
- Usa: DFS con backtracking

### Minimizar Costo (Punto 3)
- Objetivo: Máximo estrellas con mínimo gasto
- Restricción: Cada estrella solo 1 vez
- Considera: Distancia + consumo - ganancia pasto
- Usa: Algoritmo greedy optimizado

## 📊 Interpretación de Resultados

### Panel de Estado
```
Salud: Excelente          ← Estado actual
Burroenergía: 87.5%       ← Nivel de energía
Pasto: 245.3 kg           ← Alimento disponible
Tiempo: 125/3567 años luz ← Edad actual/muerte
Estrellas: 5              ← Visitadas
```

### Log de Eventos
```
[10:30:15] 🚀 Viaje iniciado en Alpha1
[10:30:16] 🌟 Viajando de Alpha1 a Beta23 (120 años luz)
[10:30:17] 🔬 Investigación consumió 2% energía
[10:30:18] 🌾 Comió 3kg de pasto, ganó 15% energía
[10:30:19] ⭐ ¡Hipergigante! Energía recargada
```

## ⚠️ Consideraciones Importantes

### Sistema de Alimentación
- Burro come automáticamente si energía < 50%
- Ganancia depende del estado de salud:
  - Excelente: 5% por kg
  - Buena: 3% por kg
  - Mala: 2% por kg

### Hipergigantes
- Máximo 2 por constelación
- Beneficios:
  - Recarga 50% de energía actual
  - Duplica pasto en bodega
  - Permite teletransporte (opcional)

### Muerte del Burro
Ocurre cuando:
- Edad ≥ Edad de muerte
- Energía = 0
- ⚠️ Reproduce sonido de alerta

## 🛠️ Solución de Problemas

### El grafo no aparece
✅ **Solución**: Verificar formato JSON en consola (F12)

### "Estrella no existe"
✅ **Solución**: Usar IDs que aparecen en el grafo cargado

### Simulación no avanza
✅ **Solución**: 
1. Calcular ruta primero
2. Verificar que burro no esté muerto
3. Reiniciar si es necesario

### Error al calcular ruta
✅ **Solución**:
1. Verificar que hay suficiente energía/pasto inicial
2. Comprobar que el grafo está conectado
3. Probar con otro ID de origen

## 📁 Estructura de Archivos

```
Grafos/
├── app/              ← Backend (Python/FastAPI)
├── data/             ← Archivos JSON
├── tests/            ← Pruebas
├── requirements.txt  ← Dependencias
├── README.md         ← Documentación completa
└── start_server.ps1  ← Script de inicio
```

## 🔗 Enlaces Útiles

- **API Docs**: http://localhost:8000/docs
- **README Completo**: `README.md`
- **Guía Desarrollo**: `DEVELOPMENT.md`

## 💡 Tips Pro

1. **Exportar resultados**: Click derecho en log → Copiar
2. **Probar múltiples rutas**: Cambiar ID origen y comparar
3. **Modificar JSON**: Editar `data/constellations_example.json`
4. **Debug**: Abrir consola del navegador (F12)

## 📞 Soporte

- Ver documentación completa en `README.md`
- Revisar código en `app/`
- Ejecutar tests: `python tests/test_algorithms.py`

## 🎓 Para Evaluación Académica

### Punto 1: ✅ Visualización
- Grafo con coordenadas a escala
- Colores únicos por constelación
- Estrellas compartidas en rojo

### Punto 2: ✅ Maximizar Estrellas
- Algoritmo DFS con backtracking
- Consideración de todos los parámetros
- Cálculo solo con valores iniciales

### Punto 3: ✅ Minimizar Costo
- Algoritmo greedy optimizado
- Gestión automática de alimentación
- Cada estrella visitada una vez
- Simulación paso a paso

### Extras: ✅
- Efectos de investigación modificables
- Sistema de hipergigantes
- Sonido de muerte
- Interfaz web completa

---

¡Listo para explorar el espacio! 🚀🫏✨
