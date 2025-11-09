"""
Construcción y gestión del grafo espacial usando NetworkX
"""
import networkx as nx
from typing import Dict, List, Tuple, Set
from app.models import ConstellationData, Star, Constellation


class SpaceGraph:
    """Grafo que representa el espacio de constelaciones"""
    
    def __init__(self, data: ConstellationData):
        self.data = data
        self.graph = nx.Graph()
        self.stars_dict: Dict[int, Star] = {}
        self.constellation_map: Dict[int, List[str]] = {}  # star_id -> [constellation_names]
        self._build_graph()
    
    def _build_graph(self):
        """Construye el grafo a partir de los datos JSON"""
        # Primera pasada: agregar todos los nodos (estrellas)
        for constellation in self.data.constellations:
            for star in constellation.starts:
                # Guardar referencia a la estrella
                self.stars_dict[star.id] = star
                
                # Mapear estrella a constelación(es)
                if star.id not in self.constellation_map:
                    self.constellation_map[star.id] = []
                self.constellation_map[star.id].append(constellation.name)
                
                # Agregar nodo con todos sus atributos
                self.graph.add_node(
                    star.id,
                    label=star.get_label(),
                    x=star.coordenates.x,
                    y=star.coordenates.y,
                    radius=star.radius,
                    timeToEat=star.timeToEat,
                    amountOfEnergy=star.amountOfEnergy,
                    hypergiant=star.hypergiant,
                    lifeYearsGained=star.lifeYearsGained if star.lifeYearsGained is not None else 0.0,
                    lifeYearsLost=star.lifeYearsLost if star.lifeYearsLost is not None else 0.0,
                    constellations=[]  # Se llenará después
                )
        
        # Actualizar constelaciones en los nodos
        for star_id, constellations in self.constellation_map.items():
            self.graph.nodes[star_id]['constellations'] = constellations
        
        # Segunda pasada: agregar aristas (conexiones entre estrellas)
        for constellation in self.data.constellations:
            for star in constellation.starts:
                for link in star.linkedTo:
                    # Agregar arista bidireccional con peso (distancia)
                    if self.graph.has_edge(star.id, link.starId):
                        # Si ya existe, mantener la distancia más corta
                        current_distance = self.graph[star.id][link.starId]['weight']
                        if link.distance < current_distance:
                            self.graph[star.id][link.starId]['weight'] = link.distance
                    else:
                        self.graph.add_edge(
                            star.id,
                            link.starId,
                            weight=link.distance
                        )
    
    def get_star(self, star_id: int) -> Star:
        """Obtiene una estrella por su ID"""
        return self.stars_dict.get(star_id)
    
    def get_neighbors(self, star_id: int) -> List[Tuple[int, float]]:
        """Obtiene los vecinos de una estrella con sus distancias"""
        if star_id not in self.graph:
            return []
        
        neighbors = []
        for neighbor_id in self.graph.neighbors(star_id):
            distance = self.graph[star_id][neighbor_id]['weight']
            neighbors.append((neighbor_id, distance))
        
        return neighbors
    
    def get_shared_stars(self) -> Set[int]:
        """Identifica estrellas que pertenecen a múltiples constelaciones"""
        shared = set()
        for star_id, constellations in self.constellation_map.items():
            if len(constellations) > 1:
                shared.add(star_id)
        return shared
    
    def get_hypergiant_stars(self) -> List[int]:
        """Obtiene todas las estrellas hipergigantes"""
        return [
            star_id for star_id, data in self.graph.nodes(data=True)
            if data.get('hypergiant', False)
        ]
    
    def get_graph_data_for_visualization(self) -> Dict:
        """
        Prepara los datos del grafo para visualización en el frontend
        """
        nodes = []
        edges = []
        
        # Preparar nodos
        shared_stars = self.get_shared_stars()
        constellation_colors = self._assign_constellation_colors()
        
        for star_id, data in self.graph.nodes(data=True):
            node_data = {
                'id': star_id,
                'label': data['label'],
                'x': data['x'],
                'y': data['y'],
                'radius': data['radius'],
                'hypergiant': data['hypergiant'],
                'constellations': data['constellations'],
                'isShared': star_id in shared_stars,
                'color': 'red' if star_id in shared_stars else constellation_colors.get(data['constellations'][0], '#888')
            }
            nodes.append(node_data)
        
        # Preparar aristas
        for edge in self.graph.edges(data=True):
            edge_data = {
                'source': edge[0],
                'target': edge[1],
                'distance': edge[2]['weight']
            }
            edges.append(edge_data)
        
        return {
            'nodes': nodes,
            'edges': edges,
            'constellations': list(constellation_colors.keys())
        }
    
    def _assign_constellation_colors(self) -> Dict[str, str]:
        """Asigna colores únicos a cada constelación"""
        colors = [
            '#3498db',  # Azul
            '#2ecc71',  # Verde
            '#f39c12',  # Naranja
            '#9b59b6',  # Púrpura
            '#e74c3c',  # Rojo oscuro
            '#1abc9c',  # Turquesa
            '#34495e',  # Gris oscuro
            '#16a085',  # Verde azulado
            '#27ae60',  # Verde oscuro
            '#2980b9',  # Azul oscuro
            '#8e44ad',  # Púrpura oscuro
            '#f1c40f',  # Amarillo
        ]
        
        constellation_colors = {}
        for i, constellation in enumerate(self.data.constellations):
            constellation_colors[constellation.name] = colors[i % len(colors)]
        
        return constellation_colors
    
    def shortest_path(self, source: int, target: int) -> Tuple[List[int], float]:
        """
        Calcula el camino más corto entre dos estrellas usando Dijkstra
        Retorna (path, total_distance)
        """
        try:
            path = nx.shortest_path(self.graph, source, target, weight='weight')
            distance = nx.shortest_path_length(self.graph, source, target, weight='weight')
            return path, distance
        except nx.NetworkXNoPath:
            return [], float('inf')
    
    def is_connected(self) -> bool:
        """Verifica si el grafo está completamente conectado"""
        return nx.is_connected(self.graph)
    
    def get_all_stars(self) -> List[int]:
        """Obtiene lista de todos los IDs de estrellas"""
        return list(self.graph.nodes())
