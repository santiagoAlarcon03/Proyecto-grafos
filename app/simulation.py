"""
Motor de simulación paso a paso del viaje del burro
"""
from typing import List, Dict, Optional
from app.models import DonkeyState, Star, SimulationStep
from app.graph_logic import SpaceGraph


class DonkeySimulation:
    """Simula el viaje del burro paso a paso"""
    
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
        if self.is_complete or self.current_step >= len(self.route):
            return None
        
        current_star_id = self.route[self.current_step]
        current_star = self.graph.get_star(current_star_id)
        
        if self.current_step == 0:
            # Primer paso: el burro está en la estrella de origen
            return SimulationStep(
                step=self.current_step,
                current_star=current_star,
                donkey_state=self.state,
                action='start',
                message=f'🚀 El burro inicia su viaje en la estrella {current_star.get_label()}'
            )
            self.state.visited_stars.append(current_star_id)
            self.current_step += 1
            self.simulation_log.append(step)
            return step
        
        # Viajar a la siguiente estrella
        next_star_id = current_star_id
        previous_star_id = self.route[self.current_step - 1]
        
        # Calcular distancia del viaje
        neighbors = self.graph.get_neighbors(previous_star_id)
        distance = next((d for nid, d in neighbors if nid == next_star_id), 0)
        
        # Actualizar edad (tiempo de vida)
        self.state.age += distance
        message = f'🌟 Viajando de {self.graph.get_star(previous_star_id).get_label()} a {current_star.get_label()} ({distance:.2f} años luz)'
        
        # Verificar si el burro murió en el viaje
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
        
        # Realizar investigación (consume energía)
        self.state.energy -= current_star.amountOfEnergy
        message += f'\n🔬 Investigación consumió {current_star.amountOfEnergy:.1f}% de energía'
        
        # Aplicar efectos de investigación (ganancia/pérdida de vida)
        life_change = current_star.lifeYearsGained - current_star.lifeYearsLost
        self.state.death_age += life_change
        if life_change != 0:
            message += f'\n⏱️ Tiempo de vida {"aumentó" if life_change > 0 else "disminuyó"} en {abs(life_change):.2f} años luz'
        
        # Verificar si necesita comer (energía < 50%)
        action = 'travel'
        if self.state.energy < 50 and self.state.grass > 0:
            # Calcular cuánto puede comer
            energy_gain_rate = self._get_energy_gain_rate()
            energy_needed = 50 - self.state.energy
            kg_needed = min(energy_needed / energy_gain_rate, self.state.grass)
            
            # El burro solo puede usar el 50% del tiempo en la estrella para comer
            max_eating_time = current_star.timeToEat * kg_needed
            actual_kg_eaten = kg_needed  # Simplificación: asumimos que siempre tiene tiempo
            
            # Consumir pasto y ganar energía
            energy_gained = actual_kg_eaten * energy_gain_rate
            self.state.energy += energy_gained
            self.state.grass -= actual_kg_eaten
            
            message += f'\n🌾 Comió {actual_kg_eaten:.2f}kg de pasto, ganó {energy_gained:.1f}% de energía'
            action = 'eat_and_research'
        
        # Actualizar estado de salud basado en energía
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
            self.is_complete = True
        
        return step
    
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
