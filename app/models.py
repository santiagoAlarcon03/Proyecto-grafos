"""
Modelos Pydantic para validación de datos del JSON
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class Coordinates(BaseModel):
    """Coordenadas de una estrella en el espacio"""
    x: float
    y: float


class LinkedStar(BaseModel):
    """Conexión entre estrellas"""
    starId: int
    distance: float = Field(gt=0, description="Distancia en años luz")


class Star(BaseModel):
    """Modelo de una estrella"""
    id: int
    name: Optional[str] = None  # Acepta 'name' del JSON
    label: Optional[str] = None  # Acepta 'label' del JSON
    linkedTo: List[LinkedStar]
    radius: float = Field(gt=0)
    timeToEat: float = Field(gt=0, description="Tiempo para comer 1kg de pasto")
    amountOfEnergy: float = Field(ge=0, description="Energía consumida por investigación")
    coordenates: Coordinates
    hypergiant: bool = False
    
    # Campos dinámicos que el científico puede modificar (opcionales en el JSON)
    lifeYearsGained: Optional[float] = 0.0
    lifeYearsLost: Optional[float] = 0.0
    
    @field_validator('name')
    @classmethod
    def validate_name_or_label(cls, v, info):
        """Asegurar que al menos name o label esté presente"""
        # Si name es None, verificar que label exista
        if v is None and info.data.get('label') is None:
            raise ValueError("La estrella debe tener 'name' o 'label'")
        return v
    
    def get_label(self) -> str:
        """Obtiene el label/nombre de la estrella"""
        return self.label or self.name or f"Star {self.id}"

    @field_validator('linkedTo')
    @classmethod
    def validate_links(cls, v):
        if not v:
            raise ValueError("Una estrella debe tener al menos una conexión")
        return v


class Constellation(BaseModel):
    """Modelo de una constelación"""
    name: str
    starts: List[Star]  # Nota: en el JSON viene como "starts" (typo original)
    
    @field_validator('starts')
    @classmethod
    def validate_stars(cls, v):
        if not v:
            raise ValueError("Una constelación debe tener al menos una estrella")
        
        # Validar que no haya más de 2 hipergigantes
        hypergiant_count = sum(1 for star in v if star.hypergiant)
        if hypergiant_count > 2:
            raise ValueError(f"Una constelación no puede tener más de 2 hipergigantes (encontradas: {hypergiant_count})")
        
        return v


class ConstellationData(BaseModel):
    """Modelo completo del archivo JSON"""
    constellations: List[Constellation]
    burroenergiaInicial: float = Field(ge=0, le=100, description="Energía inicial del burro (0-100%)")
    estadoSalud: str = Field(pattern="^(Excelente|Buena|Mala|Moribundo|Muerto)$")
    pasto: float = Field(ge=0, description="Pasto inicial en kg")
    number: int
    startAge: float = Field(ge=0, description="Edad inicial en años luz")
    deathAge: float = Field(gt=0, description="Edad de muerte en años luz")
    
    @field_validator('estadoSalud')
    @classmethod
    def validate_health(cls, v):
        valid_states = ["Excelente", "Buena", "Mala", "Moribundo", "Muerto"]
        if v not in valid_states:
            raise ValueError(f"Estado de salud debe ser uno de: {valid_states}")
        return v


class DonkeyState(BaseModel):
    """Estado actual del burro durante la simulación"""
    current_star_id: int
    energy: float = Field(ge=0, le=100)
    health: str
    grass: float = Field(ge=0)
    age: float = Field(ge=0)
    death_age: float
    visited_stars: List[int] = []
    is_alive: bool = True
    
    def remaining_life(self) -> float:
        """Calcula el tiempo de vida restante"""
        return max(0, self.death_age - self.age)
    
    def is_dead(self) -> bool:
        """Verifica si el burro está muerto"""
        return self.age >= self.death_age or self.health == "Muerto"


class RouteRequest(BaseModel):
    """Solicitud para calcular una ruta"""
    origin_star_id: int
    algorithm: str = Field(pattern="^(maximize_stars|minimize_cost)$")
    
    
class SimulationStep(BaseModel):
    """Paso de la simulación"""
    step: int
    current_star: Star
    donkey_state: DonkeyState
    action: str
    message: str
