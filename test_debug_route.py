"""Script para debuggear la ruta generada por maximize_stars_visited"""
import json
from app.graph_logic import SpaceGraph
from app.models import DonkeyState, ConstellationData

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

# Importar el optimizador
from app.algorithms import RouteOptimizer

# Crear optimizador
optimizer = RouteOptimizer(graph, initial_state)

# Ejecutar el algoritmo desde estrella 12
print("🔍 Ejecutando maximize_stars_visited desde estrella 12...\n")
route, stats = optimizer.maximize_stars_visited(origin=12)

# Mostrar resultados
print(f"📍 Ruta generada ({len(route)} estrellas):")
print(f"   {route}\n")

print(f"📊 Estadísticas:")
print(f"   - Estrellas visitadas: {stats['stars_visited']}")
print(f"   - Distancia total: {stats['total_distance']:.2f} años luz")
print(f"   - Energía final: {stats['final_energy']:.2f}%")
print(f"   - Edad final: {stats['final_age']:.2f} años")
print(f"   - ¿Está vivo?: {stats['is_alive']}")
print(f"   - Causa de muerte: {stats['cause_of_death']}")

# Mostrar últimas 3 estrellas
if len(route) >= 3:
    print(f"\n🎯 Últimas 3 estrellas visitadas:")
    for i, star_id in enumerate(route[-3:], start=len(route)-2):
        star = graph.get_star(star_id)
        print(f"   {i}. Estrella {star_id}: {star.name}")

# Verificar si la última estrella es mortal
if route:
    last_star_id = route[-1]
    last_star = graph.get_star(last_star_id)
    print(f"\n⚡ Última estrella: {last_star.name} (ID: {last_star_id})")
    print(f"   - Energía para investigar: {last_star.amountOfEnergy}%")
    
    # Calcular si el burro debería morir ahí
    if len(route) >= 2:
        prev_star_id = route[-2]
        neighbors = graph.get_neighbors(prev_star_id)
        distance_to_last = None
        for neighbor_id, dist in neighbors:
            if neighbor_id == last_star_id:
                distance_to_last = dist
                break
        
        if distance_to_last:
            travel_cost = distance_to_last * 0.1
            total_cost = travel_cost + last_star.amountOfEnergy
            print(f"   - Distancia desde estrella anterior: {distance_to_last:.2f} años luz")
            print(f"   - Costo de viaje: {travel_cost:.2f}%")
            print(f"   - Costo total (viaje + investigación): {total_cost:.2f}%")

print("\n✅ Prueba completada")
