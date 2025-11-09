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
        
        // Crear enlaces (aristas)
        const links = this.linksGroup.selectAll('line')
            .data(graphData.edges)
            .enter()
            .append('line')
            .attr('stroke', '#4a5568')
            .attr('stroke-width', 2)
            .attr('stroke-opacity', 0.6);
        
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
                // Actualizar posiciones de enlaces
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
        
        // Remover burro anterior
        this.nodesGroup.selectAll('.donkey-marker').remove();
        
        // Agregar marcador del burro
        this.nodesGroup.append('circle')
            .attr('class', 'donkey-marker')
            .attr('cx', node.fx)
            .attr('cy', node.fy)
            .attr('r', 15)
            .attr('fill', '#22c55e')
            .attr('stroke', '#fff')
            .attr('stroke-width', 3)
            .style('animation', 'pulse 1s infinite');
        
        // Agregar emoji del burro
        this.labelsGroup.append('text')
            .attr('class', 'donkey-marker')
            .attr('x', node.fx)
            .attr('y', node.fy)
            .attr('text-anchor', 'middle')
            .attr('dy', '0.3em')
            .attr('font-size', '20px')
            .text('🫏');
    }
    
    reset() {
        // Restaurar estado original
        this.nodesGroup.selectAll('circle')
            .attr('opacity', 0.9)
            .attr('stroke', d => d.hypergiant ? '#fbbf24' : '#fff')
            .attr('stroke-width', d => d.hypergiant ? 4 : 2);
        
        this.linksGroup.selectAll('line')
            .attr('stroke', '#4a5568')
            .attr('stroke-width', 2)
            .attr('stroke-opacity', 0.6);
        
        this.nodesGroup.selectAll('.donkey-marker').remove();
        this.labelsGroup.selectAll('.donkey-marker').remove();
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
