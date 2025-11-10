/**
 * Control de simulación del viaje del burro
 */

class SimulationController {
    constructor() {
        this.isRunning = false;
        this.currentRoute = null;
        this.donkeyState = null;
    }
    
    async startSimulation(originStarId, route) {
        try {
            const response = await fetch('/api/start-simulation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    origin_star_id: originStarId,
                    route: route
                })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al iniciar simulación');
            }
            
            const data = await response.json();
            
            if (data.success) {
                this.isRunning = true;
                this.currentRoute = route;
                
                // Habilitar botón de siguiente paso
                document.getElementById('nextStepBtn').disabled = false;
                document.getElementById('startSimBtn').disabled = true;
                
                // Mostrar log
                document.getElementById('logPanel').classList.remove('hidden');
                this.addLog('🚀 Simulación iniciada', 'info');
                
                return true;
            }
            
            return false;
            
        } catch (error) {
            console.error('Error al iniciar simulación:', error);
            this.addLog(`❌ Error: ${error.message}`, 'error');
            return false;
        }
    }
    
    async nextStep() {
        if (!this.isRunning) return;
        
        try {
            const response = await fetch('/api/simulation/next');
            
            if (!response.ok) {
                throw new Error('Error al obtener siguiente paso');
            }
            
            const data = await response.json();
            
            if (data.success) {
                const step = data.step;
                this.donkeyState = step.donkey_state;
                
                // Actualizar UI
                this.updateDonkeyPanel(this.donkeyState);
                
                // Mostrar posición del burro en el grafo y actualizar estrellas visitadas
                if (graphVisualizer) {
                    graphVisualizer.visitedStars = this.donkeyState.visited_stars || [];
                    graphVisualizer.showDonkeyPosition(step.current_star.id);
                }
                
                // Agregar mensaje al log
                this.addLog(step.message, this.getLogType(step.action));
                
                // Verificar si terminó
                if (data.is_complete || !this.donkeyState.is_alive) {
                    this.endSimulation();
                    
                    // Reproducir sonido si murió
                    if (!this.donkeyState.is_alive) {
                        this.playDeathSound();
                    }
                }
                
            } else {
                // Simulación terminada
                this.endSimulation();
                this.addLog(data.message, 'info');
                
                // Mostrar resumen
                if (data.summary) {
                    this.showSummary(data.summary);
                }
            }
            
        } catch (error) {
            console.error('Error en siguiente paso:', error);
            this.addLog(`❌ Error: ${error.message}`, 'error');
        }
    }
    
    endSimulation() {
        this.isRunning = false;
        document.getElementById('nextStepBtn').disabled = true;
        document.getElementById('startSimBtn').disabled = false;
        this.addLog('✅ Simulación completada', 'success');
    }
    
    reset() {
        this.isRunning = false;
        this.currentRoute = null;
        this.donkeyState = null;
        
        // Limpiar log
        document.getElementById('logContent').innerHTML = '';
        
        // Resetear grafo
        if (graphVisualizer) {
            graphVisualizer.reset();
        }
        
        // Resetear botones
        document.getElementById('nextStepBtn').disabled = true;
        document.getElementById('startSimBtn').disabled = false;
        
        this.addLog('🔄 Sistema reiniciado', 'info');
    }
    
    updateDonkeyPanel(state) {
        document.getElementById('donkeyHealth').textContent = state.health;
        document.getElementById('donkeyHealth').className = `font-bold text-lg ${this.getHealthColor(state.health)}`;
        
        // Barra de energía
        const energyBar = document.getElementById('energyBar');
        energyBar.style.width = `${state.energy}%`;
        energyBar.className = `h-4 rounded-full transition-all ${this.getEnergyColor(state.energy)}`;
        document.getElementById('energyText').textContent = `${state.energy.toFixed(1)}%`;
        
        document.getElementById('donkeyGrass').textContent = `${state.grass.toFixed(2)} kg`;
        document.getElementById('donkeyAge').textContent = 
            `${state.age.toFixed(2)} / ${state.death_age.toFixed(2)} años luz`;
        document.getElementById('starsVisited').textContent = state.visited_stars.length;
    }
    
    getHealthColor(health) {
        const colors = {
            'Excelente': 'text-green-400',
            'Buena': 'text-blue-400',
            'Mala': 'text-yellow-400',
            'Moribundo': 'text-orange-400',
            'Muerto': 'text-red-400'
        };
        return colors[health] || 'text-gray-400';
    }
    
    getEnergyColor(energy) {
        if (energy >= 75) return 'bg-green-500';
        if (energy >= 50) return 'bg-blue-500';
        if (energy >= 25) return 'bg-yellow-500';
        return 'bg-red-500';
    }
    
    getLogType(action) {
        if (action.includes('death')) return 'error';
        if (action === 'hypergiant_boost') return 'special';
        if (action === 'eat_and_research') return 'warning';
        return 'info';
    }
    
    addLog(message, type = 'info') {
        const logContent = document.getElementById('logContent');
        const timestamp = new Date().toLocaleTimeString();
        
        const logEntry = document.createElement('div');
        logEntry.className = `mb-2 ${this.getLogColor(type)}`;
        logEntry.innerHTML = `<span class="text-gray-500">[${timestamp}]</span> ${message}`;
        
        logContent.appendChild(logEntry);
        logContent.scrollTop = logContent.scrollHeight;
    }
    
    getLogColor(type) {
        const colors = {
            'info': 'text-blue-400',
            'success': 'text-green-400',
            'warning': 'text-yellow-400',
            'error': 'text-red-400',
            'special': 'text-purple-400'
        };
        return colors[type] || 'text-gray-400';
    }
    
    playDeathSound() {
        const audio = document.getElementById('deathSound');
        if (audio) {
            audio.play().catch(e => console.log('No se pudo reproducir el sonido:', e));
        }
        
        // Mostrar alerta visual
        const alert = document.createElement('div');
        alert.className = 'fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-red-600 text-white px-8 py-4 rounded-lg shadow-2xl text-2xl font-bold z-50 animate-pulse';
        alert.innerHTML = '💀 EL BURRO HA MUERTO 💀';
        document.body.appendChild(alert);
        
        setTimeout(() => alert.remove(), 3000);
    }
    
    showSummary(summary) {
        const message = `
            📊 RESUMEN DEL VIAJE
            ━━━━━━━━━━━━━━━━━━━━━━
            Estrellas visitadas: ${summary.stars_visited}
            Energía final: ${summary.final_energy.toFixed(1)}%
            Salud final: ${summary.final_health}
            Pasto restante: ${summary.remaining_grass.toFixed(2)} kg
            Edad final: ${summary.age.toFixed(2)} años luz
            Estado: ${summary.is_alive ? '✅ Vivo' : '💀 Muerto'}
        `;
        
        this.addLog(message.trim(), 'special');
    }
}

// Instancia global del controlador
const simulationController = new SimulationController();
