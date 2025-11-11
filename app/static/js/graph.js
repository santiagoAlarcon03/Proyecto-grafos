/**
 * Visualización del grafo espacial con D3.js
 */

class SpaceGraphVisualizer {
    constructor(svgId, width = 900, height = 600) {
        this.svg = d3.select(`#${svgId}`);
        this.width = width;
        this.height = height;
        this.graphData = null;
        this.simulation = null;
        this.visitedStars = [];
        this.blockedPaths = new Set();  // Para rastrear caminos bloqueados
        
        // Grupos para organizar elementos
        this.g = this.svg.append('g');
        this.linksGroup = this.g.append('g').attr('class', 'links');
        this.nodesGroup = this.g.append('g').attr('class', 'nodes');
        this.labelsGroup = this.g.append('g').attr('class', 'labels');
        
        // Configurar zoom
        this.setupZoom();
    }
    
    setupZoom() {
        const zoom = d3.zoom()
            .scaleExtent([0.1, 4])
            .on('zoom', (event) => {
                this.g.attr('transform', event.transform);
            });
        
        this.svg.call(zoom);
    }
    
    render(graphData) {
        this.graphData = graphData;
        
        // Limpiar visualización anterior
        this.linksGroup.selectAll('*').remove();
        this.nodesGroup.selectAll('*').remove();
        this.labelsGroup.selectAll('*').remove();
        
        if (!graphData || !graphData.nodes || !graphData.edges) {
            console.error('Datos de grafo inválidos');
            return;
        }
        
        // Escalar coordenadas al tamaño del SVG
        const xExtent = d3.extent(graphData.nodes, d => d.x);
        const yExtent = d3.extent(graphData.nodes, d => d.y);
        
        const xScale = d3.scaleLinear()
            .domain(xExtent)
            .range([50, this.width - 50]);
        
        const yScale = d3.scaleLinear()
            .domain(yExtent)
            .range([50, this.height - 50]);
        
        // Aplicar escala a las posiciones
        graphData.nodes.forEach(node => {
            node.fx = xScale(node.x);  // Fijar posición X
            node.fy = yScale(node.y);  // Fijar posición Y
        });
        
        // Crear enlaces (aristas) - primero las líneas invisibles gruesas para hover
        const linkInvisible = this.linksGroup.selectAll('.edge-hover-area')
            .data(graphData.edges)
            .enter()
            .append('line')
            .attr('class', 'edge-hover-area')
            .attr('stroke', 'transparent')
            .attr('stroke-width', 15)  // Área amplia para detectar hover
            .style('cursor', 'pointer')
            .on('mouseover', this.handleEdgeHover.bind(this))
            .on('mouseout', this.handleEdgeOut.bind(this))
            .on('click', this.handleEdgeClick.bind(this));
        
        // Luego las líneas visibles
        const links = this.linksGroup.selectAll('.graph-edge')
            .data(graphData.edges)
            .enter()
            .append('line')
            .attr('class', 'graph-edge')
            .attr('stroke', d => this.isEdgeBlocked(d) ? '#ef4444' : '#4a5568')
            .attr('stroke-width', d => this.isEdgeBlocked(d) ? 3 : 2)
            .attr('stroke-opacity', 0.6)
            .attr('stroke-dasharray', d => this.isEdgeBlocked(d) ? '5,5' : '0')
            .style('pointer-events', 'none');  // No capturar eventos, usamos las invisibles
        
        // Crear nodos (estrellas)
        const nodes = this.nodesGroup.selectAll('circle')
            .data(graphData.nodes)
            .enter()
            .append('circle')
            .attr('r', d => 5 + d.radius * 8)
            .attr('fill', d => d.color)
            .attr('stroke', d => d.hypergiant ? '#fbbf24' : '#fff')
            .attr('stroke-width', d => d.hypergiant ? 4 : 2)
            .attr('opacity', 0.9)
            .style('cursor', 'pointer')
            .on('mouseover', this.handleNodeHover.bind(this))
            .on('mouseout', this.handleNodeOut.bind(this))
            .on('click', this.handleNodeClick.bind(this));
        
        // Crear etiquetas
        const labels = this.labelsGroup.selectAll('text')
            .data(graphData.nodes)
            .enter()
            .append('text')
            .text(d => d.label)
            .attr('font-size', '12px')
            .attr('fill', '#fff')
            .attr('text-anchor', 'middle')
            .attr('dy', d => -(7 + d.radius * 8))
            .style('pointer-events', 'none')
            .style('user-select', 'none');
        
        // Crear simulación de fuerzas (solo para actualizar posiciones de enlaces)
        this.simulation = d3.forceSimulation(graphData.nodes)
            .force('link', d3.forceLink(graphData.edges)
                .id(d => d.id)
                .distance(100))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(this.width / 2, this.height / 2))
            .on('tick', () => {
                // Actualizar posiciones de enlaces visibles
                links
                    .attr('x1', d => {
                        const source = graphData.nodes.find(n => n.id === d.source.id || n.id === d.source);
                        return source ? source.fx : 0;
                    })
                    .attr('y1', d => {
                        const source = graphData.nodes.find(n => n.id === d.source.id || n.id === d.source);
                        return source ? source.fy : 0;
                    })
                    .attr('x2', d => {
                        const target = graphData.nodes.find(n => n.id === d.target.id || n.id === d.target);
                        return target ? target.fx : 0;
                    })
                    .attr('y2', d => {
                        const target = graphData.nodes.find(n => n.id === d.target.id || n.id === d.target);
                        return target ? target.fy : 0;
                    });
                
                // Actualizar posiciones de enlaces invisibles (hover areas)
                linkInvisible
                    .attr('x1', d => {
                        const source = graphData.nodes.find(n => n.id === d.source.id || n.id === d.source);
                        return source ? source.fx : 0;
                    })
                    .attr('y1', d => {
                        const source = graphData.nodes.find(n => n.id === d.source.id || n.id === d.source);
                        return source ? source.fy : 0;
                    })
                    .attr('x2', d => {
                        const target = graphData.nodes.find(n => n.id === d.target.id || n.id === d.target);
                        return target ? target.fx : 0;
                    })
                    .attr('y2', d => {
                        const target = graphData.nodes.find(n => n.id === d.target.id || n.id === d.target);
                        return target ? target.fy : 0;
                    });
                
                // Nodos mantienen posición fija
                nodes
                    .attr('cx', d => d.fx)
                    .attr('cy', d => d.fy);
                
                // Etiquetas
                labels
                    .attr('x', d => d.fx)
                    .attr('y', d => d.fy);
            });
        
        // Detener simulación después de un tiempo (nodos tienen posición fija)
        this.simulation.alpha(0.3).restart();
        setTimeout(() => this.simulation.stop(), 1000);
    }
    
    handleNodeHover(event, d) {
        // Resaltar nodo
        d3.select(event.target)
            .transition()
            .duration(200)
            .attr('r', d => (5 + d.radius * 8) * 1.3)
            .attr('stroke-width', 4);
        
        // Mostrar tooltip
        this.showTooltip(event, d);
    }
    
    handleNodeOut(event, d) {
        d3.select(event.target)
            .transition()
            .duration(200)
            .attr('r', d => 5 + d.radius * 8)
            .attr('stroke-width', d => d.hypergiant ? 4 : 2);
        
        this.hideTooltip();
    }
    
    handleNodeClick(event, d) {
        console.log('Estrella clickeada:', d);
        document.getElementById('originStar').value = d.id;
    }
    
    handleEdgeHover(event, d) {
        // Resaltar la línea
        d3.select(event.target)
            .transition()
            .duration(200)
            .attr('stroke-width', 5)
            .attr('stroke-opacity', 0.9);
        
        // Obtener información de las estrellas
        const source = typeof d.source === 'object' ? d.source : this.graphData.nodes.find(n => n.id === d.source);
        const target = typeof d.target === 'object' ? d.target : this.graphData.nodes.find(n => n.id === d.target);
        const isBlocked = this.isEdgeBlocked(d);
        
        // Mostrar tooltip
        const tooltip = d3.select('body').append('div')
            .attr('class', 'graph-tooltip edge-tooltip')
            .style('position', 'absolute')
            .style('background', 'rgba(0, 0, 0, 0.9)')
            .style('color', 'white')
            .style('padding', '10px')
            .style('border-radius', '5px')
            .style('pointer-events', 'none')
            .style('font-size', '12px')
            .style('z-index', '1000')
            .html(`
                <strong>Camino:</strong> ${source.label} ↔ ${target.label}<br>
                <strong>Distancia:</strong> ${d.distance.toFixed(2)} años luz<br>
                ${isBlocked ? '<span style="color: #ef4444;">⚠️ BLOQUEADO</span>' : '<span style="color: #10b981;">✓ Disponible</span>'}<br>
                <em>Click para ${isBlocked ? 'desbloquear' : 'bloquear'}</em>
            `)
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 10) + 'px');
    }
    
    handleEdgeOut(event, d) {
        // Restaurar apariencia de la línea
        const isBlocked = this.isEdgeBlocked(d);
        d3.select(event.target)
            .transition()
            .duration(200)
            .attr('stroke-width', isBlocked ? 3 : 2)
            .attr('stroke-opacity', 0.6);
        
        // Eliminar tooltips de líneas
        d3.selectAll('.edge-tooltip').remove();
    }
    
    handleEdgeClick(event, d) {
        event.stopPropagation();
        
        const source = typeof d.source === 'object' ? d.source.id : d.source;
        const target = typeof d.target === 'object' ? d.target.id : d.target;
        const isBlocked = this.isEdgeBlocked(d);
        
        console.log(`Click en camino: ${source} ↔ ${target}, actualmente ${isBlocked ? 'bloqueado' : 'disponible'}`);
        
        // Llamar a la función global de bloqueo
        if (window.togglePathBlock) {
            window.togglePathBlock(source, target, !isBlocked);
        } else {
            console.error('togglePathBlock no está disponible');
            alert('Error: Sistema de bloqueo no cargado. Recarga la página.');
        }
    }
    
    showTooltip(event, data) {
        const tooltip = d3.select('body').append('div')
            .attr('class', 'graph-tooltip')
            .style('position', 'absolute')
            .style('background', 'rgba(0, 0, 0, 0.9)')
            .style('color', 'white')
            .style('padding', '10px')
            .style('border-radius', '5px')
            .style('pointer-events', 'none')
            .style('font-size', '12px')
            .style('z-index', '1000')
            .html(`
                <strong>${data.label}</strong> (ID: ${data.id})<br>
                Constelación(es): ${data.constellations.join(', ')}<br>
                ${data.hypergiant ? '<span style="color: #fbbf24;">⭐ Hipergigante</span><br>' : ''}
                ${data.isShared ? '<span style="color: #ef4444;">🔴 Compartida</span>' : ''}
            `)
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 10) + 'px');
    }
    
    hideTooltip() {
        d3.selectAll('.graph-tooltip').remove();
    }
    
    highlightRoute(route) {
        // Resaltar la ruta calculada
        if (!route || route.length === 0) return;
        
        // Restaurar opacidad normal
        this.nodesGroup.selectAll('circle').attr('opacity', 0.3);
        this.linksGroup.selectAll('line').attr('stroke-opacity', 0.2);
        
        // Resaltar nodos de la ruta
        this.nodesGroup.selectAll('circle')
            .filter(d => route.includes(d.id))
            .attr('opacity', 1)
            .attr('stroke', '#10b981')
            .attr('stroke-width', 4);
        
        // Resaltar enlaces de la ruta
        for (let i = 0; i < route.length - 1; i++) {
            this.linksGroup.selectAll('line')
                .filter(d => {
                    const sourceId = d.source.id || d.source;
                    const targetId = d.target.id || d.target;
                    return (sourceId === route[i] && targetId === route[i + 1]) ||
                           (sourceId === route[i + 1] && targetId === route[i]);
                })
                .attr('stroke', '#10b981')
                .attr('stroke-width', 4)
                .attr('stroke-opacity', 1);
        }
    }
    
    showDonkeyPosition(starId) {
        // Mostrar posición actual del burro
        const node = this.graphData.nodes.find(n => n.id === starId);
        if (!node) return;
        
        // Verificar si ya existe un marcador del burro
        const existingMarker = this.nodesGroup.select('.donkey-marker');
        const existingLabel = this.labelsGroup.select('.donkey-label');
        
        if (!existingMarker.empty()) {
            // Animar la transición
            existingMarker
                .transition()
                .duration(800)
                .attr('cx', node.fx)
                .attr('cy', node.fy);
            
            existingLabel
                .transition()
                .duration(800)
                .attr('x', node.fx)
                .attr('y', node.fy);
        } else {
            // Crear nuevo marcador del burro
            this.nodesGroup.append('circle')
                .attr('class', 'donkey-marker')
                .attr('cx', node.fx)
                .attr('cy', node.fy)
                .attr('r', 15)
                .attr('fill', '#22c55e')
                .attr('stroke', '#fff')
                .attr('stroke-width', 3)
                .style('opacity', 0)
                .transition()
                .duration(500)
                .style('opacity', 1);
            
            // Agregar emoji del burro
            this.labelsGroup.append('text')
                .attr('class', 'donkey-label')
                .attr('x', node.fx)
                .attr('y', node.fy)
                .attr('text-anchor', 'middle')
                .attr('dy', '0.3em')
                .attr('font-size', '24px')
                .style('opacity', 0)
                .text('🫏')
                .transition()
                .duration(500)
                .style('opacity', 1);
        }
        
        // Marcar estrella actual
        this.nodesGroup.selectAll('circle:not(.donkey-marker)')
            .classed('current-star', d => d.id === starId)
            .classed('visited-star', d => d.id !== starId && this.isStarVisited(d.id));
    }
    
    isStarVisited(starId) {
        // Verifica si una estrella ha sido visitada por el burro
        return this.visitedStars && this.visitedStars.includes(starId);
    }
    
    reset() {
        // Restaurar estado original
        this.visitedStars = [];
        
        this.nodesGroup.selectAll('circle:not(.donkey-marker)')
            .attr('opacity', 0.9)
            .attr('stroke', d => d.hypergiant ? '#fbbf24' : '#fff')
            .attr('stroke-width', d => d.hypergiant ? 4 : 2)
            .classed('current-star', false)
            .classed('visited-star', false);
        
        // Restaurar líneas visibles respetando bloqueos
        this.linksGroup.selectAll('.graph-edge')
            .attr('stroke', d => this.isEdgeBlocked(d) ? '#ef4444' : '#4a5568')
            .attr('stroke-width', d => this.isEdgeBlocked(d) ? 3 : 2)
            .attr('stroke-opacity', 0.6)
            .attr('stroke-dasharray', d => this.isEdgeBlocked(d) ? '5,5' : '0');
        
        this.nodesGroup.selectAll('.donkey-marker').remove();
        this.labelsGroup.selectAll('.donkey-label').remove();
    }
    
    // Métodos para manejar caminos bloqueados
    isEdgeBlocked(edge) {
        const source = typeof edge.source === 'object' ? edge.source.id : edge.source;
        const target = typeof edge.target === 'object' ? edge.target.id : edge.target;
        const key1 = `${source}-${target}`;
        const key2 = `${target}-${source}`;
        return this.blockedPaths.has(key1) || this.blockedPaths.has(key2);
    }
    
    updateBlockedPaths(blockedPathsList) {
        // Actualizar conjunto de caminos bloqueados
        this.blockedPaths.clear();
        if (blockedPathsList && Array.isArray(blockedPathsList)) {
            blockedPathsList.forEach(path => {
                this.blockedPaths.add(`${path.from_star_id}-${path.to_star_id}`);
            });
        }
        
        // Actualizar visualización de enlaces visibles si existen
        const links = this.linksGroup.selectAll('.graph-edge');
        if (!links.empty()) {
            links
                .attr('stroke', d => this.isEdgeBlocked(d) ? '#ef4444' : '#4a5568')
                .attr('stroke-width', d => this.isEdgeBlocked(d) ? 3 : 2)
                .attr('stroke-dasharray', d => this.isEdgeBlocked(d) ? '5,5' : '0');
        }
    }
}

// Instancia global del visualizador
let graphVisualizer = null;

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    const svg = document.getElementById('graphSvg');
    const container = document.getElementById('graphContainer');
    
    graphVisualizer = new SpaceGraphVisualizer('graphSvg', 
        container.clientWidth, 600);
});
