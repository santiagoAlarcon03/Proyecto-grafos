"""
FastAPI - Servidor principal
Endpoints para el sistema de navegación espacial del burro de la NASA
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
import json
from typing import Optional

from app.models import ConstellationData, RouteRequest, DonkeyState, StartSimulationRequest
from app.graph_logic import SpaceGraph
from app.algorithms import RouteOptimizer
from app.simulation import DonkeySimulation
from app.utils import validate_json_structure, get_constellation_statistics

# Inicializar FastAPI
app = FastAPI(
    title="NASA Burro Space Explorer",
    description="Sistema de navegación interestelar para el burro explorador de la NASA",
    version="1.0.0"
)

# Configurar archivos estáticos y templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Variables globales para mantener el estado
current_graph: Optional[SpaceGraph] = None
current_data: Optional[ConstellationData] = None
current_simulation: Optional[DonkeySimulation] = None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal de la aplicación"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/upload")
async def upload_json(file: UploadFile = File(...)):
    """
    Endpoint para cargar el archivo JSON con las constelaciones
    """
    global current_graph, current_data, current_simulation
    
    try:
        # Leer el contenido del archivo
        content = await file.read()
        data_dict = json.loads(content.decode('utf-8'))
        
        # Validar estructura básica
        if not validate_json_structure(data_dict):
            raise HTTPException(
                status_code=400,
                detail="El archivo JSON no tiene la estructura correcta"
            )
        
        # Validar con Pydantic
        try:
            current_data = ConstellationData(**data_dict)
        except ValidationError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error de validación: {str(e)}"
            )
        
        # Construir el grafo
        current_graph = SpaceGraph(current_data)
        
        # Resetear simulación
        current_simulation = None
        
        # Obtener estadísticas
        stats = get_constellation_statistics(current_data)
        
        # Obtener datos para visualización
        graph_data = current_graph.get_graph_data_for_visualization()
        
        return JSONResponse({
            "success": True,
            "message": "Archivo cargado exitosamente",
            "statistics": stats,
            "graph_data": graph_data,
            "donkey_initial_state": {
                "energy": current_data.burroenergiaInicial,
                "health": current_data.estadoSalud,
                "grass": current_data.pasto,
                "age": current_data.startAge,
                "death_age": current_data.deathAge
            }
        })
        
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=400,
            detail=f"El archivo no es un JSON válido: {str(e)}"
        )
    except ValidationError as ve:
        # Mostrar detalles específicos del error de validación
        errors = ve.errors()
        error_details = []
        for error in errors:
            loc = ' -> '.join(str(l) for l in error['loc'])
            error_details.append(f"{loc}: {error['msg']}")
        raise HTTPException(
            status_code=400,
            detail=f"Error de validación del JSON: {'; '.join(error_details)}"
        )
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error detallado:\n{error_trace}")  # Para debug en consola
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el archivo: {str(e)}"
        )


@app.get("/api/graph-data")
async def get_graph_data():
    """
    Obtiene los datos del grafo para visualización
    """
    if current_graph is None:
        raise HTTPException(
            status_code=400,
            detail="Primero debe cargar un archivo JSON"
        )
    
    graph_data = current_graph.get_graph_data_for_visualization()
    return JSONResponse(graph_data)


@app.post("/api/calculate-route")
async def calculate_route(request: RouteRequest):
    """
    Calcula una ruta óptima según el algoritmo seleccionado
    - maximize_stars: Mayor cantidad de estrellas (Punto 2)
    - minimize_cost: Menor gasto posible (Punto 3)
    """
    if current_graph is None or current_data is None:
        raise HTTPException(
            status_code=400,
            detail="Primero debe cargar un archivo JSON"
        )
    
    # Verificar que la estrella origen existe
    if request.origin_star_id not in current_graph.get_all_stars():
        raise HTTPException(
            status_code=400,
            detail=f"La estrella {request.origin_star_id} no existe"
        )
    
    # Crear estado inicial del burro
    initial_state = DonkeyState(
        current_star_id=request.origin_star_id,
        energy=current_data.burroenergiaInicial,
        health=current_data.estadoSalud,
        grass=current_data.pasto,
        age=current_data.startAge,
        death_age=current_data.deathAge,
        visited_stars=[],
        is_alive=True
    )
    
    # Crear optimizador de rutas
    optimizer = RouteOptimizer(current_graph, initial_state)
    
    try:
        if request.algorithm == "maximize_stars":
            # Punto 2: Maximizar estrellas visitadas
            route, stats = optimizer.maximize_stars_visited(request.origin_star_id)
            algorithm_name = "Maximizar Estrellas Visitadas"
        else:
            # Punto 3: Minimizar costo
            route, stats = optimizer.minimize_cost_route(request.origin_star_id)
            algorithm_name = "Minimizar Costo"
        
        if not route:
            return JSONResponse({
                "success": False,
                "message": "No se pudo calcular una ruta viable"
            })
        
        # Formatear ruta con nombres de estrellas
        route_labels = [current_graph.get_star(sid).get_label() for sid in route]
        
        return JSONResponse({
            "success": True,
            "algorithm": algorithm_name,
            "route": route,
            "route_labels": route_labels,
            "statistics": stats
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al calcular la ruta: {str(e)}"
        )


@app.post("/api/start-simulation")
async def start_simulation(request: StartSimulationRequest):
    """
    Inicia una simulación paso a paso con una ruta calculada
    """
    global current_simulation
    
    if current_graph is None or current_data is None:
        raise HTTPException(
            status_code=400,
            detail="Primero debe cargar un archivo JSON"
        )
    
    # Crear estado inicial del burro
    initial_state = DonkeyState(
        current_star_id=request.origin_star_id,
        energy=current_data.burroenergiaInicial,
        health=current_data.estadoSalud,
        grass=current_data.pasto,
        age=current_data.startAge,
        death_age=current_data.deathAge,
        visited_stars=[],
        is_alive=True
    )
    
    # Crear simulación
    current_simulation = DonkeySimulation(current_graph, request.route, initial_state)
    
    return JSONResponse({
        "success": True,
        "message": "Simulación iniciada",
        "total_steps": len(request.route)
    })


@app.get("/api/simulation/next")
async def simulation_next_step():
    """
    Ejecuta el siguiente paso de la simulación
    """
    if current_simulation is None:
        raise HTTPException(
            status_code=400,
            detail="Primero debe iniciar una simulación"
        )
    
    step = current_simulation.next_step()
    
    if step is None:
        return JSONResponse({
            "success": False,
            "message": "La simulación ha terminado",
            "summary": current_simulation.get_summary()
        })
    
    return JSONResponse({
        "success": True,
        "step": step.dict(),
        "is_complete": current_simulation.is_complete
    })


@app.get("/api/simulation/summary")
async def simulation_summary():
    """
    Obtiene el resumen de la simulación actual
    """
    if current_simulation is None:
        raise HTTPException(
            status_code=400,
            detail="No hay simulación activa"
        )
    
    return JSONResponse(current_simulation.get_summary())


@app.put("/api/star/update-effects")
async def update_star_effects(star_id: int, life_gained: float = 0, life_lost: float = 0):
    """
    Actualiza los efectos de investigación de una estrella
    (Permite al científico modificar los valores antes de iniciar el viaje)
    """
    if current_graph is None:
        raise HTTPException(
            status_code=400,
            detail="Primero debe cargar un archivo JSON"
        )
    
    star = current_graph.get_star(star_id)
    if star is None:
        raise HTTPException(
            status_code=404,
            detail=f"Estrella {star_id} no encontrada"
        )
    
    # Actualizar valores
    star.lifeYearsGained = life_gained
    star.lifeYearsLost = life_lost
    
    # También actualizar en el grafo
    current_graph.graph.nodes[star_id]['lifeYearsGained'] = life_gained
    current_graph.graph.nodes[star_id]['lifeYearsLost'] = life_lost
    
    return JSONResponse({
        "success": True,
        "message": f"Efectos de la estrella {star.get_label()} actualizados",
        "star": {
            "id": star_id,
            "label": star.get_label(),
            "lifeYearsGained": life_gained,
            "lifeYearsLost": life_lost
        }
    })


@app.get("/api/constellation-stats")
async def get_constellation_stats():
    """
    Obtiene estadísticas de las constelaciones cargadas
    """
    if current_data is None:
        raise HTTPException(
            status_code=400,
            detail="Primero debe cargar un archivo JSON"
        )
    
    stats = get_constellation_statistics(current_data)
    return JSONResponse(stats)


@app.get("/api/hypergiant-stars")
async def get_hypergiant_stars():
    """
    Obtiene todas las estrellas hipergigantes disponibles
    """
    if current_graph is None:
        raise HTTPException(
            status_code=400,
            detail="Primero debe cargar un archivo JSON"
        )
    
    hypergiant_ids = current_graph.get_hypergiant_stars()
    hypergiants = [
        {
            "id": star_id,
            "label": current_graph.get_star(star_id).get_label(),
            "constellations": current_graph.constellation_map[star_id]
        }
        for star_id in hypergiant_ids
    ]
    
    return JSONResponse({
        "count": len(hypergiants),
        "hypergiants": hypergiants
    })


# Manejo de errores
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint no encontrado"}
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
