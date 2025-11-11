"""
Algoritmos de búsqueda y optimización de rutas
"""
import heapq
from typing import List, Tuple, Dict, Set, Optional
from app.graph_logic import SpaceGraph
from app.models import DonkeyState, Star


class RouteOptimizer:
    """Optimizador de rutas para el burro espacial"""
    
    # Factor de consumo debe coincidir con simulation.py
    ENERGY_CONSUMPTION_PER_LIGHT_YEAR = 0.1
    
    def __init__(self, graph: SpaceGraph, initial_donkey_state: DonkeyState):
        self.graph = graph
        self.initial_state = initial_donkey_state
    
    def maximize_stars_visited(self, origin: int) -> Tuple[List[int], Dict]:
        """
        PUNTO 2: Calcula la ruta que permite visitar la mayor cantidad de estrellas
        antes de que el burro muera, considerando solo valores iniciales.
        
        Usa DFS modificado con backtracking y poda.
        """
        best_route = []
        best_stats = {
            'stars_visited': 0,
            'total_distance': 0,
            'final_energy': 0,
            'final_age': 0,
            'cause_of_death': None
        }
        
        def dfs_backtrack(current_star: int, visited: Set[int], 
                         current_energy: float, current_age: float, 
                         current_grass: float, route: List[int],
                         total_distance: float):
            """DFS con backtracking para explorar todas las rutas posibles"""
            nonlocal best_route, best_stats
            
            # Verificar si el burro está muerto
            if current_age >= self.initial_state.death_age:
                if len(visited) > best_stats['stars_visited']:
                    best_route = route.copy()
                    best_stats = {
                        'stars_visited': len(visited),
                        'total_distance': total_distance,
                        'final_energy': current_energy,
                        'final_age': current_age,
                        'cause_of_death': 'age'
                    }
                return
            
            if current_energy <= 0:
                if len(visited) > best_stats['stars_visited']:
                    best_route = route.copy()
                    best_stats = {
                        'stars_visited': len(visited),
                        'total_distance': total_distance,
                        'final_energy': 0,
                        'final_age': current_age,
                        'cause_of_death': 'energy'
                    }
                return
            
            # Intentar visitar vecinos no visitados
            neighbors = self.graph.get_neighbors(current_star)
            
            if not neighbors:
                # Sin vecinos, actualizar mejor ruta si es necesario
                if len(visited) > best_stats['stars_visited']:
                    best_route = route.copy()
                    best_stats = {
                        'stars_visited': len(visited),
                        'total_distance': total_distance,
                        'final_energy': current_energy,
                        'final_age': current_age,
                        'cause_of_death': None
                    }
                return
            
            for neighbor_id, distance in neighbors:
                if neighbor_id not in visited:
                    # Calcular consumo de energía por el viaje
                    travel_energy_cost = distance * self.ENERGY_CONSUMPTION_PER_LIGHT_YEAR
                    
                    # Verificar si tiene suficiente energía para el viaje
                    if current_energy - travel_energy_cost <= 0:
                        continue  # No puede realizar este viaje
                    
                    # Calcular nuevo estado después de viajar
                    new_age = current_age + distance
                    
                    # Poda: si el viaje mata al burro por edad, no explorar
                    if new_age >= self.initial_state.death_age:
                        continue
                    
                    # Energía después del viaje
                    new_energy = current_energy - travel_energy_cost
                    
                    # Simular llegada a la estrella e investigación
                    star = self.graph.get_star(neighbor_id)
                    new_energy -= star.amountOfEnergy
                    new_grass = current_grass
                    
                    # Si energía < 50%, el burro come
                    if new_energy < 50 and new_grass > 0:
                        energy_gain_per_kg = self._get_energy_gain_rate(self.initial_state.health)
                        kg_needed = min((50 - new_energy) / energy_gain_per_kg, new_grass)
                        new_energy += kg_needed * energy_gain_per_kg
                        new_grass -= kg_needed
                    
                    # Poda: si no tiene energía después de todo, no continuar
                    if new_energy <= 0:
                        continue
                    
                    # Recursión
                    visited.add(neighbor_id)
                    route.append(neighbor_id)
                    
                    dfs_backtrack(
                        neighbor_id, visited, new_energy, new_age,
                        new_grass, route, total_distance + distance
                    )
                    
                    # Backtrack
                    visited.remove(neighbor_id)
                    route.pop()
            
            # Actualizar mejor ruta si esta rama es mejor
            if len(visited) > best_stats['stars_visited']:
                best_route = route.copy()
                best_stats = {
                    'stars_visited': len(visited),
                    'total_distance': total_distance,
                    'final_energy': current_energy,
                    'final_age': current_age,
                    'cause_of_death': None
                }
        
        # Iniciar DFS desde el origen
        initial_visited = {origin}
        initial_route = [origin]
        
        dfs_backtrack(
            origin, initial_visited,
            self.initial_state.energy,
            self.initial_state.age,
            self.initial_state.grass,
            initial_route, 0
        )
        
        return best_route, best_stats
    
    def minimize_cost_route(self, origin: int) -> Tuple[List[int], Dict]:
        """
        PUNTO 3: Calcula la ruta que permite conocer la mayor cantidad de estrellas
        con el menor gasto posible. Cada estrella solo se visita UNA vez.
        
        Usa algoritmo de Dijkstra para encontrar los caminos más cortos entre estrellas.
        En cada paso, selecciona la estrella no visitada más cercana que el burro pueda alcanzar.
        """
        route = [origin]
        visited = {origin}
        current_star = origin
        current_energy = self.initial_state.energy
        current_age = self.initial_state.age
        current_grass = self.initial_state.grass
        total_cost = 0
        total_dijkstra_distance = 0  # Distancia acumulada usando Dijkstra
        
        stats = {
            'stars_visited': 1,
            'total_distance': 0,
            'total_energy_consumed': 0,
            'total_grass_consumed': 0,
            'final_energy': current_energy,
            'final_age': current_age,
            'final_grass': current_grass,
            'is_alive': True
        }
        
        while True:
            # Obtener todas las estrellas no visitadas
            unvisited_stars = set(self.graph.get_all_stars()) - visited
            
            if not unvisited_stars:
                break  # No hay más estrellas por visitar
            
            # Usar Dijkstra para encontrar el camino más corto a cada estrella no visitada
            best_target = None
            best_path = None
            best_cost = float('inf')
            best_energy_after = 0
            best_grass_consumed = 0
            best_energy_gain = 0
            
            for target_id in unvisited_stars:
                # Calcular camino más corto usando Dijkstra
                path, dijkstra_distance = self.graph.shortest_path(current_star, target_id)
                
                if not path or dijkstra_distance == float('inf'):
                    continue  # No hay camino a esta estrella
                
                # Verificar si el burro sobreviviría el viaje por edad
                if current_age + dijkstra_distance >= self.initial_state.death_age:
                    continue  # Este viaje sería mortal por edad
                
                # Calcular consumo de energía por el viaje
                travel_energy_cost = dijkstra_distance * self.ENERGY_CONSUMPTION_PER_LIGHT_YEAR
                
                # Verificar si tiene suficiente energía para el viaje
                if current_energy - travel_energy_cost <= 0:
                    continue  # No puede realizar este viaje por energía
                
                star = self.graph.get_star(target_id)
                
                # Calcular consumo total de energía (viaje + investigación)
                energy_cost_research = star.amountOfEnergy
                total_energy_cost = travel_energy_cost + energy_cost_research
                
                # Simular si necesitará comer
                energy_after_travel = current_energy - total_energy_cost
                energy_gain = 0
                grass_consumed = 0
                
                if energy_after_travel < 50 and current_grass > 0:
                    energy_gain_rate = self._get_energy_gain_rate(self.initial_state.health)
                    kg_needed = min((50 - energy_after_travel) / energy_gain_rate, current_grass)
                    energy_gain = kg_needed * energy_gain_rate
                    grass_consumed = kg_needed
                
                # Verificar que tenga energía suficiente después de todo
                final_energy = energy_after_travel + energy_gain
                if final_energy <= 0:
                    continue
                
                # Costo = distancia de Dijkstra + energía consumida - ganancia por comer
                cost = dijkstra_distance + total_energy_cost - (energy_gain * 0.1)
                
                # Seleccionar la estrella con menor costo
                if cost < best_cost:
                    best_cost = cost
                    best_target = target_id
                    best_path = path
                    best_energy_after = final_energy
                    best_grass_consumed = grass_consumed
                    best_energy_gain = energy_gain
            
            if best_target is None:
                break  # No hay estrellas viables para visitar
            
            # Moverse a la mejor estrella encontrada usando el camino de Dijkstra
            # El camino incluye el origen, así que lo quitamos
            path_to_target = best_path[1:] if len(best_path) > 1 else [best_target]
            dijkstra_distance = self.graph.shortest_path(current_star, best_target)[1]
            
            # Calcular energía consumida
            travel_energy_cost = dijkstra_distance * self.ENERGY_CONSUMPTION_PER_LIGHT_YEAR
            star = self.graph.get_star(best_target)
            total_energy_cost = travel_energy_cost + star.amountOfEnergy
            
            # Actualizar estado
            current_age += dijkstra_distance
            current_energy -= total_energy_cost
            
            # Comer si es necesario
            if current_energy < 50 and current_grass > 0:
                current_energy += best_energy_gain
                current_grass -= best_grass_consumed
                stats['total_grass_consumed'] += best_grass_consumed
            
            # Agregar todas las estrellas del camino a la ruta (excepto las ya visitadas)
            for star_id in path_to_target:
                if star_id not in visited:
                    route.append(star_id)
                    visited.add(star_id)
            
            current_star = best_target
            total_cost += best_cost
            total_dijkstra_distance += dijkstra_distance
            
            stats['total_distance'] += dijkstra_distance
            stats['total_energy_consumed'] += total_energy_cost
            stats['stars_visited'] = len(visited)
            
            # Verificar si el burro sigue vivo
            if current_age >= self.initial_state.death_age or current_energy <= 0:
                stats['is_alive'] = False
                break
        
        stats['final_energy'] = current_energy
        stats['final_age'] = current_age
        stats['final_grass'] = current_grass
        stats['algorithm'] = 'Dijkstra'
        stats['total_dijkstra_distance'] = total_dijkstra_distance
        
        return route, stats
    
    def _get_energy_gain_rate(self, health: str) -> float:
        """Calcula cuánta energía gana por kg de pasto según salud"""
        rates = {
            'Excelente': 5.0,
            'Buena': 3.0,
            'Mala': 2.0,
            'Moribundo': 1.0,
            'Muerto': 0.0
        }
        return rates.get(health, 0.0)
    
    def _calculate_health_from_energy(self, energy: float) -> str:
        """Determina el estado de salud según el nivel de energía"""
        if energy >= 75:
            return 'Excelente'
        elif energy >= 50:
            return 'Buena'
        elif energy >= 25:
            return 'Mala'
        elif energy > 0:
            return 'Moribundo'
        else:
            return 'Muerto'
