"""Script para comparar ambos algoritmos"""
import json
from app.graph_logic import SpaceGraph
from app.models import DonkeyState, ConstellationData
from app.algorithms import RouteOptimizer

# Cargar el archivo JSON
with open('data/large_test_constellation.json', 'r', encoding='utf-8') as f:
    data_dict = json.load(f)

# Crear el modelo de datos
data = ConstellationData(**data_dict)

# Crear el grafo
graph = SpaceGraph(data)

# Crear estado inicial del burro
initial_state = DonkeyState(
    energy=data.burroenergiaInicial,
    grass=data.pasto,
    age=data.startAge,
    death_age=data.deathAge,
    current_star_id=12,
    health="Excelente"
)

# Crear optimizador
optimizer = RouteOptimizer(graph, initial_state)

# Ejecutar ambos algoritmos desde estrella 1
print("=" * 70)
print("🔍 COMPARACIÓN DE ALGORITMOS - Origen: Estrella 1")
print("=" * 70)

print("\n📊 ALGORITMO 1: MAXIMIZAR ESTRELLAS VISITADAS (DFS)")
print("-" * 70)
route_max, stats_max = optimizer.maximize_stars_visited(origin=1)
print(f"Ruta ({len(route_max)} estrellas): {route_max}")
print(f"  - Estrellas visitadas: {stats_max['stars_visited']}")
print(f"  - Distancia total: {stats_max['total_distance']:.2f} años luz")
print(f"  - Energía final: {stats_max['final_energy']:.2f}%")
print(f"  - ¿Está vivo?: {stats_max['is_alive']}")

print("\n📊 ALGORITMO 2: MINIMIZAR COSTO (GREEDY)")
print("-" * 70)
route_min, stats_min = optimizer.minimize_cost_route(origin=1)
print(f"Ruta ({len(route_min)} estrellas): {route_min}")
print(f"  - Estrellas visitadas: {stats_min['stars_visited']}")
print(f"  - Distancia total: {stats_min['total_distance']:.2f} años luz")
print(f"  - Energía final: {stats_min['final_energy']:.2f}%")
print(f"  - ¿Está vivo?: {stats_min.get('is_alive', 'N/A')}")

print("\n🔍 COMPARACIÓN:")
print("-" * 70)
print(f"  Diferencia en estrellas: {len(route_max) - len(route_min)}")
print(f"  Diferencia en distancia: {stats_max['total_distance'] - stats_min['total_distance']:.2f} años luz")
print(f"  ¿Son la misma ruta?: {route_max == route_min}")

if route_max == route_min:
    print("\n⚠️  PROBLEMA: Ambos algoritmos generaron la MISMA ruta")
else:
    print("\n✅ Los algoritmos generaron rutas diferentes")
    # Mostrar primeras diferencias
    print("\n📍 Primeras diferencias:")
    for i in range(min(len(route_max), len(route_min))):
        if route_max[i] != route_min[i]:
            print(f"  Posición {i}: Maximize={route_max[i]}, Minimize={route_min[i]}")
            if i >= 5:  # Mostrar solo las primeras 5 diferencias
                break

print("\n" + "=" * 70)
