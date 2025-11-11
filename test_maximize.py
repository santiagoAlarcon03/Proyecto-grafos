"""Script de prueba para verificar el algoritmo maximize_stars_visited"""
from app.graph_logic import SpaceGraph
from app.algorithms import RouteOptimizer
from app.models import DonkeyState
import json

# Cargar JSON
with open('data/large_test_constellation.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Crear grafo
graph = SpaceGraph()
for constellation in data['constellations']:
    for star in constellation['starts']:
        graph.add_star(star)

# Estado inicial del burro
state = DonkeyState(
    current_star_id=12,
    energy=100,
    health='Excelente',
    grass=500,
    age=10,
    death_age=5000
)

# Calcular ruta
opt = RouteOptimizer(graph, state)
route, stats = opt.maximize_stars_visited(12)

print("=" * 60)
print("RESULTADOS DEL ALGORITMO MAXIMIZE_STARS_VISITED")
print("=" * 60)
print(f"Origen: Estrella 12")
print(f"Estrellas visitadas: {stats['stars_visited']}")
print(f"Energía final: {stats['final_energy']:.2f}%")
print(f"Edad final: {stats['final_age']:.2f} años luz")
print(f"Distancia total: {stats['total_distance']:.2f} años luz")
print(f"Causa de muerte: {stats.get('cause_of_death', 'N/A')}")
print(f"\nPrimeras 15 estrellas de la ruta:")
print(route[:15])
print(f"\nÚltimas 5 estrellas de la ruta:")
print(route[-5:])
print(f"\nRuta completa tiene {len(route)} estrellas")
