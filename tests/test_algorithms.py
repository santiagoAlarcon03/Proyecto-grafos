"""
Tests básicos para validar funcionalidades del sistema
"""
import pytest
import json
from pathlib import Path

# Nota: Para ejecutar los tests, instalar pytest:
# pip install pytest
# Ejecutar: pytest tests/test_algorithms.py -v

def test_json_structure():
    """Verifica que el JSON de ejemplo tenga la estructura correcta"""
    json_path = Path('data/constellations_example.json')
    
    assert json_path.exists(), "Archivo JSON de ejemplo no encontrado"
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Verificar claves principales
    assert 'constellations' in data
    assert 'burroenergiaInicial' in data
    assert 'estadoSalud' in data
    assert 'pasto' in data
    assert 'startAge' in data
    assert 'deathAge' in data
    
    # Verificar que hay constelaciones
    assert len(data['constellations']) > 0
    
    # Verificar estructura de constelación
    constellation = data['constellations'][0]
    assert 'name' in constellation
    assert 'starts' in constellation
    
    # Verificar estructura de estrella
    star = constellation['starts'][0]
    required_fields = ['id', 'label', 'linkedTo', 'radius', 'timeToEat', 
                      'amountOfEnergy', 'coordenates', 'hypergiant']
    for field in required_fields:
        assert field in star, f"Campo {field} faltante en estrella"
    
    print("✅ Estructura JSON válida")


def test_hypergiant_limit():
    """Verifica que no haya más de 2 hipergigantes por constelación"""
    json_path = Path('data/constellations_example.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for constellation in data['constellations']:
        hypergiant_count = sum(1 for star in constellation['starts'] if star['hypergiant'])
        assert hypergiant_count <= 2, \
            f"Constelación '{constellation['name']}' tiene {hypergiant_count} hipergigantes (máximo 2)"
    
    print("✅ Límite de hipergigantes correcto")


def test_star_connections():
    """Verifica que todas las conexiones sean bidireccionales"""
    json_path = Path('data/constellations_example.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Construir diccionario de estrellas
    all_stars = {}
    for constellation in data['constellations']:
        for star in constellation['starts']:
            all_stars[star['id']] = star
    
    # Verificar bidireccionalidad
    for star_id, star in all_stars.items():
        for link in star['linkedTo']:
            target_id = link['starId']
            
            # Verificar que la estrella destino existe
            assert target_id in all_stars, \
                f"Estrella {star_id} conecta a {target_id} que no existe"
            
            # Verificar conexión inversa
            target_star = all_stars[target_id]
            reverse_link = next((l for l in target_star['linkedTo'] if l['starId'] == star_id), None)
            
            assert reverse_link is not None, \
                f"Conexión {star_id} -> {target_id} no tiene reversa"
            
            # Verificar que distancias coincidan
            assert link['distance'] == reverse_link['distance'], \
                f"Distancias no coinciden entre {star_id} <-> {target_id}"
    
    print("✅ Todas las conexiones son bidireccionales")


def test_energy_gain_rates():
    """Verifica los cálculos de ganancia de energía"""
    from app.utils import calculate_health_percentage
    
    # Probar cada estado de salud
    assert calculate_health_percentage('Excelente') == 87.5
    assert calculate_health_percentage('Buena') == 62.5
    assert calculate_health_percentage('Mala') == 37.5
    assert calculate_health_percentage('Moribundo') == 12.5
    assert calculate_health_percentage('Muerto') == 0
    
    print("✅ Tasas de ganancia de energía correctas")


def test_initial_donkey_state():
    """Verifica que el estado inicial del burro sea válido"""
    json_path = Path('data/constellations_example.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Verificar energía inicial
    assert 0 <= data['burroenergiaInicial'] <= 100, \
        "Energía inicial debe estar entre 0 y 100"
    
    # Verificar estado de salud
    valid_states = ['Excelente', 'Buena', 'Mala', 'Moribundo', 'Muerto']
    assert data['estadoSalud'] in valid_states, \
        f"Estado de salud inválido: {data['estadoSalud']}"
    
    # Verificar pasto
    assert data['pasto'] >= 0, "Pasto no puede ser negativo"
    
    # Verificar edades
    assert data['startAge'] >= 0, "Edad inicial no puede ser negativa"
    assert data['deathAge'] > data['startAge'], \
        "Edad de muerte debe ser mayor que edad inicial"
    
    print("✅ Estado inicial del burro válido")


if __name__ == "__main__":
    """Ejecutar tests directamente"""
    print("\n" + "=" * 60)
    print("🧪 EJECUTANDO TESTS DEL SISTEMA")
    print("=" * 60 + "\n")
    
    try:
        test_json_structure()
        test_hypergiant_limit()
        test_star_connections()
        test_energy_gain_rates()
        test_initial_donkey_state()
        
        print("\n" + "=" * 60)
        print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
        print("=" * 60 + "\n")
        
    except AssertionError as e:
        print("\n" + "=" * 60)
        print(f"❌ TEST FALLÓ: {str(e)}")
        print("=" * 60 + "\n")
        raise
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ ERROR: {str(e)}")
        print("=" * 60 + "\n")
        raise
