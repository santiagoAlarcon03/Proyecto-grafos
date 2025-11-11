"""Script para probar Dijkstra con destino"""
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
    current_star_id=1,
    health="Excelente"
)

# Crear optimizador
optimizer = RouteOptimizer(graph, initial_state)

print("=" * 80)
print("🔍 PRUEBA DE DIJKSTRA CON DESTINO")
print("=" * 80)

# Probar con destino
origin = 1
destination = 22

print(f"\n📍 Origen: Estrella {origin}")
print(f"📍 Destino: Estrella {destination}")

print("\n📊 MODO 1: SIN DESTINO (Greedy Conservador)")
print("-" * 80)
route_no_dest, stats_no_dest = optimizer.minimize_cost_route(origin)
print(f"Ruta ({len(route_no_dest)} estrellas): {route_no_dest}")
print(f"  - Distancia total: {stats_no_dest['total_distance']:.2f} años luz")
print(f"  - Energía final: {stats_no_dest['final_energy']:.2f}%")
print(f"  - ¿Está vivo?: {stats_no_dest['is_alive']}")
print(f"  - Algoritmo: {stats_no_dest.get('algorithm', 'N/A')}")

print("\n📊 MODO 2: CON DESTINO (Dijkstra Puro)")
print("-" * 80)
route_with_dest, stats_with_dest = optimizer.minimize_cost_route(origin, destination)
print(f"Ruta ({len(route_with_dest)} estrellas): {route_with_dest}")
print(f"  - Distancia total: {stats_with_dest['total_distance']:.2f} años luz")
print(f"  - Energía final: {stats_with_dest['final_energy']:.2f}%")
print(f"  - ¿Está vivo?: {stats_with_dest['is_alive']}")
print(f"  - ¿Llegó al destino?: {stats_with_dest.get('destination_reached', 'N/A')}")
print(f"  - Algoritmo: {stats_with_dest.get('algorithm', 'N/A')}")

print("\n🔍 COMPARACIÓN:")
print("-" * 80)
print(f"  Diferencia en estrellas: {len(route_with_dest) - len(route_no_dest)}")
print(f"  Diferencia en distancia: {stats_with_dest['total_distance'] - stats_no_dest['total_distance']:.2f} años luz")

if destination in route_with_dest:
    print(f"\n  ✅ Dijkstra llegó al destino (estrella {destination})")
else:
    print(f"\n  ❌ Dijkstra NO llegó al destino (estrella {destination})")

print("\n" + "=" * 80)
