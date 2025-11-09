"""
Funciones auxiliares y utilidades
"""
from typing import Dict, Any
import json
from pathlib import Path


def validate_json_structure(data: Dict[str, Any]) -> bool:
    """
    Valida que el JSON tenga la estructura básica esperada
    """
    required_keys = ['constellations', 'burroenergiaInicial', 'estadoSalud', 
                     'pasto', 'number', 'startAge', 'deathAge']
    
    for key in required_keys:
        if key not in data:
            return False
    
    if not isinstance(data['constellations'], list) or len(data['constellations']) == 0:
        return False
    
    return True


def calculate_health_percentage(health: str) -> float:
    """
    Convierte el estado de salud a un porcentaje de energía asociado
    """
    health_map = {
        'Excelente': 87.5,  # 75-100
        'Buena': 62.5,      # 50-75
        'Mala': 37.5,       # 25-50
        'Moribundo': 12.5,  # 0-25
        'Muerto': 0
    }
    return health_map.get(health, 50)


def format_route_output(route: list, graph) -> str:
    """
    Formatea una ruta para mostrarla legiblemente
    """
    if not route:
        return "No se encontró ruta"
    
    star_labels = [graph.get_star(star_id).get_label() for star_id in route]
    return " → ".join(star_labels)


def save_json_file(data: Dict[str, Any], filepath: Path) -> bool:
    """
    Guarda datos en formato JSON
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar archivo: {e}")
        return False


def load_json_file(filepath: Path) -> Dict[str, Any]:
    """
    Carga un archivo JSON
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar archivo: {e}")
        return {}


def calculate_total_distance(route: list, graph) -> float:
    """
    Calcula la distancia total de una ruta
    """
    total = 0
    for i in range(len(route) - 1):
        current = route[i]
        next_star = route[i + 1]
        
        neighbors = graph.get_neighbors(current)
        distance = next((d for nid, d in neighbors if nid == next_star), 0)
        total += distance
    
    return total


def get_constellation_statistics(data) -> Dict[str, Any]:
    """
    Genera estadísticas sobre las constelaciones
    """
    stats = {
        'total_constellations': len(data.constellations),
        'total_stars': 0,
        'total_connections': 0,
        'hypergiant_stars': 0,
        'constellations_info': []
    }
    
    for constellation in data.constellations:
        constellation_stats = {
            'name': constellation.name,
            'stars_count': len(constellation.starts),
            'hypergiants': sum(1 for star in constellation.starts if star.hypergiant)
        }
        stats['constellations_info'].append(constellation_stats)
        stats['total_stars'] += len(constellation.starts)
        stats['hypergiant_stars'] += constellation_stats['hypergiants']
        
        for star in constellation.starts:
            stats['total_connections'] += len(star.linkedTo)
    
    # Las conexiones están duplicadas (bidireccionales)
    stats['total_connections'] = stats['total_connections'] // 2
    
    return stats
