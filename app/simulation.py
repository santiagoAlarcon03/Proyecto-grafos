"""
Motor de simulación paso a paso del viaje del burro
"""
from typing import List, Dict, Optional
from app.models import DonkeyState, Star, SimulationStep
from app.graph_logic import SpaceGraph


class DonkeySimulation:
    """Simula el viaje del burro paso a paso"""
    
    # Factor de consumo de energía por año luz viajado
    # Puedes ajustar este valor para cambiar la dificultad
    # 0.1 = 0.1% de energía por año luz (120 años luz = 12% energía)
    ENERGY_CONSUMPTION_PER_LIGHT_YEAR = 0.1
    
    def __init__(self, graph: SpaceGraph, route: List[int], initial_state: DonkeyState):
        self.graph = graph
        self.route = route
        self.state = initial_state
        self.current_step = 0
        self.simulation_log: List[SimulationStep] = []
        self.is_complete = False
    
    def next_step(self) -> Optional[SimulationStep]:
        """
        Ejecuta el siguiente paso de la simulación
        Retorna información sobre el paso actual
        """
        if self.is_complete:
            return None
        
        # Si llegó al final de la ruta pero aún está vivo, crear paso final de muerte
        if self.current_step >= len(self.route):
            if self.state.is_alive and self.state.energy > 0:
                # Crear paso final donde el burro muere por agotamiento
                last_star_id = self.route[-1]
                last_star = self.graph.get_star(last_star_id)
                
                # Consumir toda la energía restante
                self.state.energy = 0
                self.state.is_alive = False
                self.state.health = 'Muerto'
                self.is_complete = True
                
                step = SimulationStep(
                    step=self.current_step,
                    current_star=last_star,
                    donkey_state=self.state,
                    action='death_by_exhaustion',
                    message=f'💀 El burro murió por agotamiento extremo en {last_star.get_label()}. No puede continuar sin energía suficiente.'
                )
                
                self.simulation_log.append(step)
                return step
            return None
        
        current_star_id = self.route[self.current_step]
        current_star = self.graph.get_star(current_star_id)
        
        if self.current_step == 0:
            # Primer paso: el burro está en la estrella de origen
            self.state.visited_stars.append(current_star_id)
            self.state.current_star_id = current_star_id
            
            step = SimulationStep(
                step=self.current_step,
                current_star=current_star,
                donkey_state=self.state,
                action='start',
                message=f'🚀 El burro inicia su viaje en la estrella {current_star.get_label()}'
            )
            self.current_step += 1
            self.simulation_log.append(step)
            return step
        
        # Viajar a la siguiente estrella
        next_star_id = current_star_id
        previous_star_id = self.route[self.current_step - 1]
        
        # VERIFICAR SI EL CAMINO ESTÁ BLOQUEADO
        if self.graph.is_path_blocked(previous_star_id, next_star_id):
            # Intentar recalcular la ruta
            recalc_result = self.check_and_recalculate_if_blocked()
            
            if recalc_result and recalc_result['recalculated']:
                # Ruta recalculada exitosamente
                current_star = self.graph.get_star(previous_star_id)
                step = SimulationStep(
                    step=self.current_step,
                    current_star=current_star,
                    donkey_state=self.state,
                    action='route_recalculated',
                    message=recalc_result['message']
                )
                self.simulation_log.append(step)
                
                # Actualizar next_star_id al nuevo destino
                next_star_id = self.route[self.current_step]
                current_star_id = next_star_id
            else:
                # No hay ruta alternativa, el burro está atrapado
                self.state.is_alive = False
                self.state.health = 'Muerto'
                self.is_complete = True
                
                current_star = self.graph.get_star(previous_star_id)
                blocked_from = self.graph.get_star(previous_star_id).get_label()
                blocked_to = self.graph.get_star(next_star_id).get_label()
                
                step = SimulationStep(
                    step=self.current_step,
                    current_star=current_star,
                    donkey_state=self.state,
                    action='death_by_blocked_path',
                    message=f'💀 El burro murió porque el camino de {blocked_from} a {blocked_to} está bloqueado por cometas/meteoritos y no hay ruta alternativa disponible.'
                )
                self.simulation_log.append(step)
                return step
        
        # Calcular distancia del viaje
        neighbors = self.graph.get_neighbors(previous_star_id)
        distance = next((d for nid, d in neighbors if nid == next_star_id), 0)
        
        # Consumir energía por el viaje (basado en la distancia)
        # Fórmula: distancia * factor de consumo
        energy_consumed_by_travel = distance * self.ENERGY_CONSUMPTION_PER_LIGHT_YEAR
        self.state.energy -= energy_consumed_by_travel
        
        # Actualizar edad (tiempo de vida)
        self.state.age += distance
        message = f'🌟 Viajando de {self.graph.get_star(previous_star_id).get_label()} a {current_star.get_label()} ({distance:.2f} años luz)'
        message += f'\n⚡ El viaje consumió {energy_consumed_by_travel:.1f}% de energía'
        
        # Verificar si el burro murió en el viaje por falta de energía
        if self.state.energy <= 0:
            self.state.is_alive = False
            self.state.health = 'Muerto'
            self.is_complete = True
            
            step = SimulationStep(
                step=self.current_step,
                current_star=current_star,
                donkey_state=self.state,
                action='death_by_energy_travel',
                message=f'💀 El burro murió en el viaje por falta de energía. Distancia recorrida: {distance:.2f} años luz'
            )
            self.simulation_log.append(step)
            return step
        
        # Verificar si el burro murió en el viaje por edad
        if self.state.age >= self.state.death_age:
            self.state.is_alive = False
            self.state.health = 'Muerto'
            self.is_complete = True
            
            step = SimulationStep(
                step=self.current_step,
                current_star=current_star,
                donkey_state=self.state,
                action='death_by_age',
                message=f'💀 El burro murió en el viaje. Edad alcanzada: {self.state.age:.2f} años luz'
            )
            self.simulation_log.append(step)
            return step
        
        # Llegar a la estrella
        self.state.visited_stars.append(current_star_id)
        self.state.current_star_id = current_star_id
        
        # Actualizar estado de salud antes de investigación
        self.state.health = self._calculate_health()
        
        # Realizar investigación (consume energía adicional)
        energy_before_research = self.state.energy
        self.state.energy -= current_star.amountOfEnergy
        message += f'\n🔬 Investigación consumió {current_star.amountOfEnergy:.1f}% de energía (Total consumido: {energy_consumed_by_travel + current_star.amountOfEnergy:.1f}%)'
        
        # Verificar si murió por falta de energía después de investigar
        if self.state.energy <= 0:
            self.state.is_alive = False
            self.state.health = 'Muerto'
            self.is_complete = True
            
            step = SimulationStep(
                step=self.current_step,
                current_star=current_star,
                donkey_state=self.state,
                action='death_by_energy_research',
                message=message + '\n💀 El burro murió durante la investigación por falta de energía'
            )
            self.simulation_log.append(step)
            return step
        
        # Aplicar efectos de investigación (ganancia/pérdida de vida)
        life_change = current_star.lifeYearsGained - current_star.lifeYearsLost
        self.state.death_age += life_change
        if life_change != 0:
            message += f'\n⏱️ Tiempo de vida {"aumentó" if life_change > 0 else "disminuyó"} en {abs(life_change):.2f} años luz'
        
        # Verificar si necesita comer (energía < 50%)
        action = 'travel'
        if self.state.energy < 50 and self.state.grass > 0:
            # Actualizar estado de salud ACTUAL antes de calcular cuánto gana por kg
            self.state.health = self._calculate_health()
            energy_gain_rate = self._get_energy_gain_rate()
            
            # Calcular tiempo disponible para comer (50% del tiempo total en estrella)
            # Tiempo para comer 1 kg = timeToEat
            # Tiempo para investigar ~ timeToEat (asumimos proporcional)
            # Tiempo total = 2 * timeToEat → 50% disponible = timeToEat
            time_available_for_eating = current_star.timeToEat
            
            # Máximo kg que puede comer según tiempo disponible
            max_kg_by_time = time_available_for_eating / current_star.timeToEat  # = 1 kg
            
            # Calcular cuánto DESEARÍA comer (para llegar a 50% o más)
            energy_needed = 50 - self.state.energy
            kg_desired = energy_needed / energy_gain_rate if energy_gain_rate > 0 else 0
            
            # Lo que REALMENTE puede comer está limitado por tiempo y pasto disponible
            actual_kg_eaten = min(max_kg_by_time, kg_desired, self.state.grass)
            
            # Consumir pasto y ganar energía
            energy_gained = actual_kg_eaten * energy_gain_rate
            self.state.energy += energy_gained
            self.state.grass -= actual_kg_eaten
            
            message += f'\n🌾 Comió {actual_kg_eaten:.2f}kg de pasto (máx: {max_kg_by_time:.2f}kg por tiempo), ganó {energy_gained:.1f}% de energía (tasa: {energy_gain_rate:.1f}%/kg)'
            action = 'eat_and_research'
        
        # Actualizar estado de salud final basado en energía actual
        self.state.health = self._calculate_health()
        
        # Verificar si el burro murió
        if self.state.energy <= 0 or self.state.health == 'Muerto':
            self.state.is_alive = False
            self.state.health = 'Muerto'
            self.is_complete = True
            action = 'death_by_energy'
            message += '\n💀 El burro murió por falta de energía'
        
        # Verificar si es hipergigante y puede teletransportarse
        if current_star.hypergiant and self.state.is_alive:
            # Recargar energía y pasto
            self.state.energy = min(100, self.state.energy * 1.5)
            self.state.grass *= 2
            message += f'\n⭐ ¡Estrella Hipergigante! Energía recargada al {self.state.energy:.1f}% y pasto duplicado'
            action = 'hypergiant_boost'
        
        step = SimulationStep(
            step=self.current_step,
            current_star=current_star,
            donkey_state=self.state,
            action=action,
            message=message
        )
        
        self.current_step += 1
        self.simulation_log.append(step)
        
        # Verificar si terminó la ruta
        if self.current_step >= len(self.route):
            # Si el burro aún está vivo en la última estrella, debe morir por agotamiento
            if self.state.is_alive and self.state.energy > 0:
                # No marcar como completo todavía, permitir un paso más
                pass
            else:
                self.is_complete = True
        
        return step
    
    def check_and_recalculate_if_blocked(self) -> Optional[Dict]:
        """
        Verifica si el próximo paso está bloqueado y recalcula la ruta si es necesario.
        Retorna información sobre el recálculo o None si no hay bloqueo.
        """
        if self.is_complete or self.current_step >= len(self.route):
            return None
        
        # Obtener estrella actual y próxima
        if self.current_step == 0:
            # Primer paso, no hay camino que verificar
            return None
        
        current_star_id = self.route[self.current_step - 1]
        next_star_id = self.route[self.current_step]
        
        # Verificar si el camino está bloqueado
        if self.graph.is_path_blocked(current_star_id, next_star_id):
            # El camino está bloqueado, necesitamos recalcular
            # Obtener la estrella destino final de la ruta original
            final_destination = self.route[-1]
            
            # Intentar encontrar un nuevo camino desde la posición actual al destino
            new_path, distance = self.graph.shortest_path(current_star_id, final_destination)
            
            if not new_path or distance == float('inf'):
                # No hay camino alternativo disponible
                return {
                    'recalculated': False,
                    'blocked_from': current_star_id,
                    'blocked_to': next_star_id,
                    'reason': 'no_alternative_path',
                    'message': f'⚠️ Camino bloqueado y no hay ruta alternativa disponible. El burro está atrapado.'
                }
            
            # Reemplazar la ruta restante con el nuevo camino
            # Mantener las estrellas ya visitadas y agregar el nuevo camino
            visited_route = self.route[:self.current_step]
            self.route = visited_route + new_path
            
            return {
                'recalculated': True,
                'blocked_from': current_star_id,
                'blocked_to': next_star_id,
                'new_path': new_path,
                'new_distance': distance,
                'message': f'🔄 Ruta recalculada debido a bloqueo. Nueva ruta encontrada ({len(new_path)} estrellas, {distance:.2f} años luz)'
            }
        
        return None
    
    def run_full_simulation(self) -> List[SimulationStep]:
        """Ejecuta toda la simulación de una vez"""
        while not self.is_complete:
            step = self.next_step()
            if step is None:
                break
        return self.simulation_log
    
    def get_summary(self) -> Dict:
        """Retorna un resumen de la simulación"""
        return {
            'total_steps': len(self.simulation_log),
            'stars_visited': len(self.state.visited_stars),
            'final_energy': self.state.energy,
            'final_health': self.state.health,
            'remaining_grass': self.state.grass,
            'age': self.state.age,
            'remaining_life': self.state.remaining_life(),
            'is_alive': self.state.is_alive,
            'route': self.route,
            'visited_stars': self.state.visited_stars
        }
    
    def _get_energy_gain_rate(self) -> float:
        """Calcula cuánta energía gana por kg de pasto según salud"""
        rates = {
            'Excelente': 5.0,
            'Buena': 3.0,
            'Mala': 2.0,
            'Moribundo': 1.0,
            'Muerto': 0.0
        }
        return rates.get(self.state.health, 0.0)
    
    def _calculate_health(self) -> str:
        """Determina el estado de salud según el nivel de energía"""
        if self.state.energy >= 75:
            return 'Excelente'
        elif self.state.energy >= 50:
            return 'Buena'
        elif self.state.energy >= 25:
            return 'Mala'
        elif self.state.energy > 0:
            return 'Moribundo'
        else:
            return 'Muerto'
