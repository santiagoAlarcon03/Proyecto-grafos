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
            'is_alive': True,
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
                        'is_alive': False,
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
                        'is_alive': False,
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
                        'is_alive': current_energy > 0 and current_age < self.initial_state.death_age,
                        'cause_of_death': None
                    }
                return
            
            explored_any = False
            for neighbor_id, distance in neighbors:
                if neighbor_id not in visited:
                    # Calcular consumo de energía por el viaje
                    travel_energy_cost = distance * self.ENERGY_CONSUMPTION_PER_LIGHT_YEAR
                    
                    # Calcular nuevo estado después de viajar
                    new_age = current_age + distance
                    
                    # Energía después del viaje
                    new_energy = current_energy - travel_energy_cost
                    
                    # Simular llegada a la estrella e investigación
                    star = self.graph.get_star(neighbor_id)
                    new_energy -= star.amountOfEnergy
                    new_grass = current_grass
                    
                    # Si energía < 50%, el burro come
                    if new_energy < 50 and new_grass > 0 and new_energy > 0:
                        # Calcular estado de salud según energía ACTUAL
                        current_health = self._calculate_health_from_energy(new_energy)
                        energy_gain_per_kg = self._get_energy_gain_rate(current_health)
                        
                        # Límite de tiempo para comer (50% del tiempo en estrella)
                        time_available = star.timeToEat
                        max_kg_by_time = time_available / star.timeToEat  # = 1 kg
                        
                        kg_needed = (50 - new_energy) / energy_gain_per_kg if energy_gain_per_kg > 0 else 0
                        kg_actual = min(max_kg_by_time, kg_needed, new_grass)
                        
                        new_energy += kg_actual * energy_gain_per_kg
                        new_grass -= kg_actual
                    
                    # PERMITIR explorar aunque muera (para llegar a la estrella mortal)
                    # La verificación de muerte se hará en la próxima iteración del DFS
                    explored_any = True
                    
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
            
            # IMPORTANTE: Actualizar mejor ruta después del loop
            # Solo si exploró al menos un vecino O si no tiene vecinos disponibles
            if len(visited) > best_stats['stars_visited']:
                best_route = route.copy()
                best_stats = {
                    'stars_visited': len(visited),
                    'total_distance': total_distance,
                    'final_energy': current_energy,
                    'final_age': current_age,
                    'is_alive': current_energy > 0 and current_age < self.initial_state.death_age,
                    'cause_of_death': None if current_energy > 0 else 'energy'
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
        
        # Si el burro terminó vivo (no murió), intentar agregar UNA estrella más aunque sea mortal
        if best_stats['cause_of_death'] is None and best_stats['final_energy'] > 0:
            last_star = best_route[-1] if best_route else origin
            neighbors = self.graph.get_neighbors(last_star)
            visited_stars = set(best_route)
            
            # Buscar el vecino más cercano no visitado
            closest_neighbor = None
            closest_distance = float('inf')
            
            for neighbor_id, distance in neighbors:
                if neighbor_id not in visited_stars and distance < closest_distance:
                    closest_neighbor = neighbor_id
                    closest_distance = distance
            
            # Si encontró un vecino, agregarlo a la ruta (será la estrella mortal)
            if closest_neighbor is not None:
                best_route.append(closest_neighbor)
                # Actualizar estadísticas simulando muerte
                travel_cost = closest_distance * self.ENERGY_CONSUMPTION_PER_LIGHT_YEAR
                star = self.graph.get_star(closest_neighbor)
                final_energy = best_stats['final_energy'] - travel_cost - star.amountOfEnergy
                best_stats['final_energy'] = max(0, final_energy)
                best_stats['final_age'] += closest_distance
                best_stats['total_distance'] += closest_distance
                best_stats['stars_visited'] += 1
                best_stats['is_alive'] = False
                best_stats['cause_of_death'] = 'energy' if final_energy <= 0 else ('age' if best_stats['final_age'] >= self.initial_state.death_age else None)
        
        return best_route, best_stats
    
    def minimize_cost_route(self, origin: int, destination: int = None) -> Tuple[List[int], Dict]:
        """
        PUNTO 3: Calcula la ruta con el menor gasto posible.
        
        Si se proporciona 'destination':
            Usa Dijkstra para encontrar el camino más corto del origen al destino,
            visitando todas las estrellas intermedias en el camino óptimo.
        
        Si NO se proporciona 'destination':
            Estrategia greedy que visita la mayor cantidad de estrellas con menor gasto,
            eligiendo en cada paso el vecino directo que requiera menor energía.
        """
        
        # MODO 1: Con destino específico - Usar Dijkstra puro
        if destination is not None:
            return self._dijkstra_to_destination(origin, destination)
        
        # MODO 2: Sin destino - Greedy conservador (código existente)
        route = [origin]
        visited = {origin}
        current_star = origin
        current_energy = self.initial_state.energy
        current_age = self.initial_state.age
        current_grass = self.initial_state.grass
        total_cost = 0
        
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
            # Obtener vecinos DIRECTOS no visitados
            neighbors = self.graph.get_neighbors(current_star)
            unvisited_neighbors = [(nid, dist) for nid, dist in neighbors if nid not in visited]
            
            if not unvisited_neighbors:
                break  # No hay vecinos disponibles
            
            # Evaluar cada vecino y elegir el de MENOR GASTO
            best_target = None
            best_distance = 0
            best_cost = float('inf')
            best_energy_after = 0
            best_grass_consumed = 0
            best_energy_gain = 0
            best_will_die = False
            
            for neighbor_id, distance in unvisited_neighbors:
                # Calcular consumo de energía por el viaje DIRECTO
                travel_energy_cost = distance * self.ENERGY_CONSUMPTION_PER_LIGHT_YEAR
                
                star = self.graph.get_star(neighbor_id)
                
                # Calcular consumo total de energía (viaje + investigación)
                energy_cost_research = star.amountOfEnergy
                total_energy_cost = travel_energy_cost + energy_cost_research
                
                # Simular si necesitará comer
                energy_after_travel = current_energy - total_energy_cost
                energy_gain = 0
                grass_consumed = 0
                will_die = False  # Flag para saber si morirá en esta estrella
                
                # Verificar muerte por edad
                if current_age + distance >= self.initial_state.death_age:
                    will_die = True
                
                # Verificar muerte por energía en el viaje
                if current_energy - travel_energy_cost <= 0:
                    will_die = True
                
                # Si sobrevive el viaje, simular comer
                if not will_die:
                    if energy_after_travel < 50 and current_grass > 0:
                        # Calcular estado de salud ACTUAL según energía después de viajar
                        current_health = self._calculate_health_from_energy(energy_after_travel)
                        energy_gain_rate = self._get_energy_gain_rate(current_health)
                        
                        # Límite de tiempo: 50% del tiempo en la estrella
                        time_available = star.timeToEat  # 50% del tiempo total
                        max_kg_by_time = time_available / star.timeToEat  # = 1 kg
                        
                        # Calcular kg necesarios y lo que realmente puede comer
                        kg_needed = (50 - energy_after_travel) / energy_gain_rate if energy_gain_rate > 0 else 0
                        kg_actual = min(max_kg_by_time, kg_needed, current_grass)
                        
                        energy_gain = kg_actual * energy_gain_rate
                        grass_consumed = kg_actual
                    
                    # Verificar muerte después de investigación y comer
                    final_energy = energy_after_travel + energy_gain
                    if final_energy <= 0:
                        will_die = True
                
                # Calcular el COSTO de visitar este vecino
                # ESTRATEGIA CONSERVADORA: Priorizar EFICIENCIA sobre cantidad
                # Si morirá o el gasto es demasiado alto, evitar esa estrella
                if will_die:
                    # NO considerar estrellas donde morirá (estrategia conservadora)
                    continue
                else:
                    # Costo = energía total gastada (viaje + investigación) - energía ganada comiendo
                    # Menor costo = más eficiente
                    cost = total_energy_cost - energy_gain
                    final_energy = energy_after_travel + energy_gain
                
                # Seleccionar el vecino con MENOR COSTO (menor gasto de energía)
                if cost < best_cost:
                    best_cost = cost
                    best_target = neighbor_id
                    best_distance = distance
                    best_energy_after = final_energy
                    best_grass_consumed = grass_consumed
                    best_energy_gain = energy_gain
                    best_will_die = will_die
            
            if best_target is None:
                break  # No hay vecinos viables para visitar
            
            # ESTRATEGIA CONSERVADORA: Detenerse si el costo es muy alto o la energía es baja
            # Umbral: Si el próximo paso consume más del 30% de energía restante, detenerse
            star = self.graph.get_star(best_target)
            travel_energy_cost = best_distance * self.ENERGY_CONSUMPTION_PER_LIGHT_YEAR
            total_energy_cost = travel_energy_cost + star.amountOfEnergy
            
            # Si el gasto es más del 30% de la energía actual, detenerse (estrategia conservadora)
            if total_energy_cost > (current_energy * 0.3) and len(visited) > 1:
                break  # Detenerse para ahorrar energía
            
            # Si la energía caerá por debajo del 25% después de este paso, detenerse
            if best_energy_after < 25 and len(visited) > 1:
                break  # Detenerse antes de quedarse sin energía
            
            # Actualizar estado
            current_age += best_distance
            current_energy -= total_energy_cost
            
            # Comer si es necesario
            if current_energy < 50 and current_grass > 0:
                current_energy += best_energy_gain
                current_grass -= best_grass_consumed
                stats['total_grass_consumed'] += best_grass_consumed
            
            # Agregar la estrella a la ruta
            route.append(best_target)
            visited.add(best_target)
            
            current_star = best_target
            total_cost += best_cost
            
            stats['total_distance'] += best_distance
            stats['total_energy_consumed'] += total_energy_cost
            stats['stars_visited'] = len(visited)
            
            # Si la estrella seleccionada causa la muerte, agregar y terminar
            if best_will_die:
                stats['is_alive'] = False
                break
            
            # Verificar si el burro sigue vivo después de actualizar estado
            if current_age >= self.initial_state.death_age or current_energy <= 0:
                stats['is_alive'] = False
                break
        
        stats['final_energy'] = current_energy
        stats['final_age'] = current_age
        stats['final_grass'] = current_grass
        stats['algorithm'] = 'Greedy - Minimizar Costo'
        
        # ESTRATEGIA CONSERVADORA: NO agregar estrella mortal
        # Este algoritmo debe terminar con el burro VIVO y con energía restante
        # (a diferencia de maximize_stars que exprime hasta la muerte)
        
        return route, stats
    
    def _dijkstra_to_destination(self, origin: int, destination: int) -> Tuple[List[int], Dict]:
        """
        Usa Dijkstra para encontrar el camino más corto del origen al destino.
        Retorna la ruta completa con todas las estrellas intermedias.
        """
        # Usar el método shortest_path del grafo (implementa Dijkstra)
        path, total_distance = self.graph.shortest_path(origin, destination)
        
        if not path or total_distance == float('inf'):
            # No hay camino posible
            return [origin], {
                'stars_visited': 1,
                'total_distance': 0,
                'total_energy_consumed': 0,
                'total_grass_consumed': 0,
                'final_energy': self.initial_state.energy,
                'final_age': self.initial_state.age,
                'final_grass': self.initial_state.grass,
                'is_alive': True,
                'algorithm': 'Dijkstra - Sin camino',
                'destination_reached': False
            }
        
        # Simular el viaje siguiendo el camino de Dijkstra
        current_energy = self.initial_state.energy
        current_age = self.initial_state.age
        current_grass = self.initial_state.grass
        total_energy_consumed = 0
        total_grass_consumed = 0
        destination_reached = False
        
        # Recorrer el camino estrella por estrella
        for i in range(len(path) - 1):
            current_star_id = path[i]
            next_star_id = path[i + 1]
            
            # Obtener distancia entre estrellas consecutivas
            neighbors = self.graph.get_neighbors(current_star_id)
            distance = next((d for nid, d in neighbors if nid == next_star_id), 0)
            
            # Calcular consumo de energía por el viaje
            travel_energy_cost = distance * self.ENERGY_CONSUMPTION_PER_LIGHT_YEAR
            
            # Obtener información de la estrella destino
            star = self.graph.get_star(next_star_id)
            research_cost = star.amountOfEnergy
            total_energy_cost = travel_energy_cost + research_cost
            
            # Actualizar estado
            current_age += distance
            current_energy -= travel_energy_cost
            
            # Verificar muerte en el viaje
            if current_energy <= 0:
                break
            
            # Consumir energía de investigación
            current_energy -= research_cost
            
            # Verificar muerte después de investigar
            if current_energy <= 0:
                break
            
            # Si energía < 50%, el burro come
            if current_energy < 50 and current_grass > 0:
                current_health = self._calculate_health_from_energy(current_energy)
                energy_gain_rate = self._get_energy_gain_rate(current_health)
                
                # Límite de 1 kg por estrella
                time_available = star.timeToEat
                max_kg_by_time = 1.0
                
                kg_needed = (50 - current_energy) / energy_gain_rate if energy_gain_rate > 0 else 0
                kg_actual = min(max_kg_by_time, kg_needed, current_grass)
                
                energy_gained = kg_actual * energy_gain_rate
                current_energy += energy_gained
                current_grass -= kg_actual
                total_grass_consumed += kg_actual
            
            total_energy_consumed += total_energy_cost
            
            # Verificar si llegó al destino
            if next_star_id == destination:
                destination_reached = True
                break
        
        # Calcular estadísticas
        stats = {
            'stars_visited': len(path),
            'total_distance': total_distance,
            'total_energy_consumed': total_energy_consumed,
            'total_grass_consumed': total_grass_consumed,
            'final_energy': max(0, current_energy),
            'final_age': current_age,
            'final_grass': current_grass,
            'is_alive': current_energy > 0 and current_age < self.initial_state.death_age,
            'algorithm': 'Dijkstra - Ruta Óptima',
            'destination_reached': destination_reached
        }
        
        return path, stats
    
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
