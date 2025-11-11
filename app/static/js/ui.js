/**
 * Manejo de la interfaz de usuario y eventos
 */

let currentGraphData = null;
let currentRoute = null;
let donkeyInitialState = null;
let blockedPathsList = [];

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Cargar archivo JSON
    document.getElementById('loadBtn').addEventListener('click', loadJSONFile);
    
    // Calcular ruta
    document.getElementById('calculateBtn').addEventListener('click', calculateRoute);
    
    // Mostrar/ocultar campo de destino según algoritmo
    document.getElementById('algorithmSelect').addEventListener('change', (e) => {
        const destinationContainer = document.getElementById('destinationContainer');
        if (e.target.value === 'minimize_cost') {
            destinationContainer.classList.remove('hidden');
        } else {
            destinationContainer.classList.add('hidden');
            document.getElementById('destinationStar').value = '';
        }
    });
    
    // Controles de simulación
    document.getElementById('startSimBtn').addEventListener('click', startSimulation);
    document.getElementById('nextStepBtn').addEventListener('click', () => simulationController.nextStep());
    document.getElementById('resetBtn').addEventListener('click', resetSimulation);
});

async function loadJSONFile() {
    const fileInput = document.getElementById('jsonFile');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Por favor selecciona un archivo JSON');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        showLoading('Cargando archivo...');
        
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error al cargar archivo');
        }
        
        const data = await response.json();
        
        if (data.success) {
            currentGraphData = data.graph_data;
            donkeyInitialState = data.donkey_initial_state;
            
            // Renderizar grafo
            if (graphVisualizer && currentGraphData) {
                graphVisualizer.render(currentGraphData);
                document.getElementById('loadingMessage').classList.add('hidden');
                document.getElementById('legend').classList.remove('hidden');
            }
            
            // Mostrar paneles
            document.getElementById('donkeyPanel').classList.remove('hidden');
            document.getElementById('routePanel').classList.remove('hidden');
            document.getElementById('simulationPanel').classList.remove('hidden');
            document.getElementById('statsPanel').classList.remove('hidden');
            
            // Actualizar estado inicial del burro
            updateInitialDonkeyState(donkeyInitialState);
            
            // Mostrar estadísticas
            displayStatistics(data.statistics);
            
            // Cargar caminos bloqueados inicialmente
            await loadBlockedPaths();
            
            showSuccess('Archivo cargado exitosamente');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    }
}

function updateInitialDonkeyState(state) {
    document.getElementById('donkeyHealth').textContent = state.health;
    document.getElementById('donkeyHealth').className = `font-bold text-lg ${getHealthColor(state.health)}`;
    
    const energyBar = document.getElementById('energyBar');
    energyBar.style.width = `${state.energy}%`;
    energyBar.className = `h-4 rounded-full transition-all ${getEnergyColor(state.energy)}`;
    document.getElementById('energyText').textContent = `${state.energy}%`;
    
    document.getElementById('donkeyGrass').textContent = `${state.grass} kg`;
    document.getElementById('donkeyAge').textContent = `${state.age} / ${state.death_age} años luz`;
    document.getElementById('starsVisited').textContent = '0';
}

async function calculateRoute() {
    const originStarId = parseInt(document.getElementById('originStar').value);
    const algorithm = document.getElementById('algorithmSelect').value;
    
    if (isNaN(originStarId)) {
        showError('Por favor ingresa un ID de estrella válido');
        return;
    }
    
    try {
        showLoading('Calculando ruta óptima...');
        
        const requestBody = {
            origin_star_id: originStarId,
            algorithm: algorithm
        };
        
        // Agregar destino solo si está definido y el algoritmo es minimize_cost
        const destinationStarId = document.getElementById('destinationStar').value;
        if (algorithm === 'minimize_cost' && destinationStarId && !isNaN(parseInt(destinationStarId))) {
            requestBody.destination_star_id = parseInt(destinationStarId);
        }
        
        const response = await fetch('/api/calculate-route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error al calcular ruta');
        }
        
        const data = await response.json();
        
        if (data.success) {
            currentRoute = data.route;
            
            // Resaltar ruta en el grafo
            if (graphVisualizer) {
                graphVisualizer.highlightRoute(currentRoute);
            }
            
            // Mostrar información de la ruta
            displayRouteInfo(data);
            
            // Habilitar botón de iniciar simulación
            document.getElementById('startSimBtn').disabled = false;
            
            showSuccess(`Ruta calculada: ${data.route_labels.join(' → ')}`);
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    }
}

function displayRouteInfo(routeData) {
    const statsContent = document.getElementById('statsContent');
    
    let html = `
        <div class="space-y-2">
            <div>
                <p class="text-gray-400 text-xs">Algoritmo</p>
                <p class="font-bold">${routeData.algorithm}</p>
            </div>
            <div>
                <p class="text-gray-400 text-xs">Estrellas en ruta</p>
                <p class="font-bold text-purple-400">${routeData.route.length}</p>
            </div>
    `;
    
    // Mostrar estadísticas según el algoritmo
    if (routeData.statistics) {
        if (routeData.statistics.stars_visited !== undefined) {
            html += `
                <div>
                    <p class="text-gray-400 text-xs">Estrellas visitadas (proyección)</p>
                    <p class="font-bold text-green-400">${routeData.statistics.stars_visited}</p>
                </div>
            `;
        }
        
        if (routeData.statistics.total_distance !== undefined) {
            html += `
                <div>
                    <p class="text-gray-400 text-xs">Distancia total</p>
                    <p class="font-bold">${routeData.statistics.total_distance.toFixed(2)} años luz</p>
                </div>
            `;
        }
        
        if (routeData.statistics.final_energy !== undefined) {
            html += `
                <div>
                    <p class="text-gray-400 text-xs">Energía final estimada</p>
                    <p class="font-bold">${routeData.statistics.final_energy.toFixed(1)}%</p>
                </div>
            `;
        }
    }
    
    html += '</div>';
    statsContent.innerHTML = html;
}

function displayStatistics(stats) {
    // Agregar estadísticas adicionales
    const statsContent = document.getElementById('statsContent');
    const currentHTML = statsContent.innerHTML;
    
    const additionalStats = `
        <div class="mt-4 pt-4 border-t border-gray-700">
            <p class="text-xs font-bold text-gray-400 mb-2">ESTADÍSTICAS GENERALES</p>
            <div class="space-y-1 text-xs">
                <p>Constelaciones: <span class="font-bold">${stats.total_constellations}</span></p>
                <p>Estrellas totales: <span class="font-bold">${stats.total_stars}</span></p>
                <p>Conexiones: <span class="font-bold">${stats.total_connections}</span></p>
                <p>Hipergigantes: <span class="font-bold text-yellow-400">${stats.hypergiant_stars}</span></p>
            </div>
        </div>
    `;
    
    statsContent.innerHTML = currentHTML + additionalStats;
}

async function startSimulation() {
    if (!currentRoute) {
        showError('Primero debes calcular una ruta');
        return;
    }
    
    const originStarId = parseInt(document.getElementById('originStar').value);
    const success = await simulationController.startSimulation(originStarId, currentRoute);
    
    if (success) {
        showSuccess('Simulación iniciada - Usa "Siguiente Paso" para avanzar');
    }
}

function resetSimulation() {
    simulationController.reset();
    
    // Resetear UI
    if (donkeyInitialState) {
        updateInitialDonkeyState(donkeyInitialState);
    }
    
    // Resetear grafo
    if (graphVisualizer && currentRoute) {
        graphVisualizer.highlightRoute(currentRoute);
    }
}

// Utilidades UI
function showLoading(message) {
    // Implementar loading indicator si se desea
    console.log('Loading:', message);
}

function showSuccess(message) {
    showNotification(message, 'success');
}

function showError(message) {
    showNotification(message, 'error');
}

function showNotification(message, type = 'info') {
    const colors = {
        success: 'bg-green-600',
        error: 'bg-red-600',
        info: 'bg-blue-600'
    };
    
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-fade-in`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('animate-fade-out');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function getHealthColor(health) {
    const colors = {
        'Excelente': 'text-green-400',
        'Buena': 'text-blue-400',
        'Mala': 'text-yellow-400',
        'Moribundo': 'text-orange-400',
        'Muerto': 'text-red-400'
    };
    return colors[health] || 'text-gray-400';
}

function getEnergyColor(energy) {
    if (energy >= 75) return 'bg-green-500';
    if (energy >= 50) return 'bg-blue-500';
    if (energy >= 25) return 'bg-yellow-500';
    return 'bg-red-500';
}

// ===== FUNCIONES PARA BLOQUEO DE CAMINOS =====

async function togglePathBlock(fromStarId, toStarId, shouldBlock) {
    if (!currentGraphData) {
        showError('Primero debes cargar un archivo JSON');
        return;
    }
    
    try {
        const response = await fetch('/api/block-path', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                from_star_id: fromStarId,
                to_star_id: toStarId,
                block: shouldBlock,
                reason: shouldBlock ? 'Paso de cometas/meteoritos' : 'Ruta despejada'
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error al modificar camino');
        }
        
        const data = await response.json();
        if (data.success) {
            await loadBlockedPaths();
            showSuccess(data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    }
}

async function loadBlockedPaths() {
    if (!currentGraphData) return;
    
    try {
        const response = await fetch('/api/blocked-paths');
        if (!response.ok) return;
        
        const data = await response.json();
        blockedPathsList = data.blocked_paths || [];
        
        // Actualizar visualización
        if (graphVisualizer && graphVisualizer.updateBlockedPaths) {
            graphVisualizer.updateBlockedPaths(blockedPathsList);
        }
        
        // Actualizar panel
        updateBlockedPathsPanel();
    } catch (error) {
        console.error('Error al cargar caminos bloqueados:', error);
    }
}

function updateBlockedPathsPanel() {
    const panel = document.getElementById('blockedPathsPanel');
    const list = document.getElementById('blockedPathsList');
    
    if (!panel || !list) return;
    
    if (blockedPathsList.length === 0) {
        panel.classList.add('hidden');
        return;
    }
    
    panel.classList.remove('hidden');
    list.innerHTML = '';
    
    blockedPathsList.forEach(path => {
        const item = document.createElement('div');
        item.className = 'flex items-center justify-between p-2 bg-red-900 bg-opacity-30 rounded border border-red-700';
        item.innerHTML = `
            <div class="flex-1">
                <span class="text-sm">⚠️ ${path.path}</span>
            </div>
            <button 
                onclick="togglePathBlock(${path.from_star_id}, ${path.to_star_id}, false)"
                class="px-2 py-1 bg-green-600 hover:bg-green-700 rounded text-xs transition-colors"
            >
                Desbloquear
            </button>
        `;
        list.appendChild(item);
    });
}

// Hacer disponible globalmente
window.togglePathBlock = togglePathBlock;
window.loadBlockedPaths = loadBlockedPaths;
