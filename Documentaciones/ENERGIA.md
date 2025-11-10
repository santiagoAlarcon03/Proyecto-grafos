# ⚡ Sistema de Consumo de Energía del Burro

## 📊 Mecánicas de Energía

El burro explorador de la NASA consume energía de **dos formas diferentes** durante su viaje interestelar:

### 1. 🚀 Consumo por Viaje (Distancia)
- **Fórmula:** `Energía consumida = Distancia × Factor de consumo`
- **Factor predeterminado:** `1.0` (1% de energía por año luz)
- **Ejemplo:** Si la distancia entre Estrella A y Estrella B es 5.2 años luz, el burro consumirá **5.2%** de energía en el viaje

#### Cómo ajustar la dificultad:
Puedes modificar el factor de consumo en `app/simulation.py`:
```python
class DonkeySimulation:
    # Ajusta este valor para cambiar la dificultad
    ENERGY_CONSUMPTION_PER_LIGHT_YEAR = 1.0
```

**Opciones sugeridas:**
- `0.5` - Fácil (0.5% por año luz)
- `1.0` - Normal (1% por año luz) ✅ **Por defecto**
- `1.5` - Difícil (1.5% por año luz)
- `2.0` - Muy difícil (2% por año luz)

### 2. 🔬 Consumo por Investigación
- **Definido en:** Cada estrella tiene su propio valor `amountOfEnergy`
- **Varía según:** Las características de cada estrella en el JSON
- **Ejemplo:** Una estrella con `"amountOfEnergy": 10.0` consumirá **10%** de energía

### 📈 Consumo Total por Paso
```
Energía Total Consumida = (Distancia × Factor) + Investigación
```

**Ejemplo completo:**
- Distancia: 8 años luz → Consume 8%
- Investigación: 15% → Consume 15%
- **Total consumido: 23%** 🔴

## 🍃 Recuperación de Energía

### Comer Pasto
El burro puede comer pasto para recuperar energía:
- Se activa automáticamente cuando energía < 50%
- La tasa de ganancia depende del estado de salud:
  - **Excelente:** 5% por kg
  - **Buena:** 3% por kg
  - **Mala:** 2% por kg
  - **Moribundo:** 1% por kg

### ⭐ Estrellas Hipergigantes
- Recargan energía al **150%** del valor actual (máx. 100%)
- Duplican el pasto disponible
- ¡Úsalas estratégicamente!

## 💀 Condiciones de Muerte

El burro puede morir de tres formas:

1. **Energía ≤ 0%** durante el viaje
2. **Energía ≤ 0%** después de investigación
3. **Edad ≥ Edad de muerte**

## 🎯 Estrategias Recomendadas

### ✅ Para Sobrevivir Viajes Largos:
1. Lleva suficiente pasto inicial
2. Planifica rutas con estrellas hipergigantes
3. Evita estrellas con alta `amountOfEnergy` si tu energía está baja
4. Considera el algoritmo "minimizar costo" para distancias cortas

### ✅ Para Maximizar Estrellas Visitadas:
1. Calcula el consumo total estimado de tu ruta
2. Asegúrate de tener energía suficiente: `Energía Inicial > Consumo Total`
3. Usa el algoritmo "maximizar estrellas" pero verifica la viabilidad

## 📊 Cálculo de Viabilidad de Ruta

Antes de iniciar el viaje, puedes estimar si el burro sobrevivirá:

```
Energía Requerida = Σ(distancias × factor) + Σ(investigaciones)
Energía Disponible = Energía Inicial + (Pasto × Tasa de ganancia)

Si Energía Disponible ≥ Energía Requerida → Ruta viable ✅
Si Energía Disponible < Energía Requerida → Ruta inviable ❌
```

## 🔧 Archivo de Configuración (JSON)

Ejemplo de valores relevantes en tu archivo JSON:

```json
{
  "burroenergiaInicial": 80.0,    // Energía inicial (0-100%)
  "estadoSalud": "Excelente",     // Afecta recuperación de energía
  "pasto": 50.0,                  // Kg de pasto inicial
  "startAge": 0,
  "deathAge": 100,
  "constellations": [
    {
      "starts": [
        {
          "amountOfEnergy": 10.0, // Energía consumida en investigación
          "linkedTo": [
            {
              "distance": 5.2     // Distancia en años luz
            }
          ]
        }
      ]
    }
  ]
}
```

## 🎮 Flujo de Simulación

Por cada paso:
1. 🚀 **Viaje:** Consumir energía por distancia
2. ⚠️ **Check:** ¿Murió en el viaje?
3. 🏁 **Llegada:** Registrar estrella visitada
4. 🔬 **Investigación:** Consumir energía adicional
5. ⏱️ **Efectos:** Aplicar ganancia/pérdida de vida
6. 🍃 **Comer:** Si energía < 50% y hay pasto
7. 💚 **Actualizar:** Estado de salud
8. ⭐ **Bonus:** Si es hipergigante, recargar
9. ⚠️ **Check:** ¿Murió después de investigación?
10. ➡️ **Siguiente paso**

---

**Última actualización:** Noviembre 2025  
**Versión:** 1.0  
**Proyecto:** NASA Burro Space Explorer 🚀🫏
