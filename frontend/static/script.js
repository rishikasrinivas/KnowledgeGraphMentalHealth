// Global variable to store Cytoscape instance
let cy;

function initializeCytoscape(container) {
    // Create tooltip
    let tooltip = document.getElementById('node-tooltip');
    if (!tooltip) {
        tooltip = document.createElement('div');
        tooltip.id = 'node-tooltip';
        document.body.appendChild(tooltip);
    }

    // Create filter panel
    const existingPanel = document.getElementById('filter-panel');
    if (!existingPanel) {
        const filterPanel = createFilterPanel();
        container.parentNode.insertBefore(filterPanel, container);
    }

    return cytoscape({
        container: container,
        style: [
            {
                selector: 'node',
                style: {
                    'label': 'data(label)',
                    'background-color': '#bbe7e8',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'color': '#000',
                    'font-size': '15px', // Adjusted for better readability
                    'font-family': "'Poppins', sans-serif",
                    'width': '120px',  // Fixed width for consistent node size
                    'height': '120px',  // Fixed height to match width and padding
                    'min-zoomed-font-size': 8,
                    'border-width': '2px',
                    'border-color': '#F3F4F7',
                    'border-opacity': 0.8,
                    'padding': '10px', // Additional padding to contain text
                    'text-outline-color': '#bbe7e8',
                    'text-outline-width': 2,
                    'text-wrap': 'wrap', // Enable wrapping
                    'text-max-width': '100px', // Allow text to wrap at 100px width
                    'z-index': 10,
                    'cursor': 'pointer'
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': function(ele) {
                        return getEdgeWidth(ele.data('label').toLowerCase());
                    },
                    'line-color': function(ele) {
                        return getColorForRelationship(ele.data('label').toLowerCase());
                    },
                    'target-arrow-shape': 'triangle',
                    'target-arrow-color': function(ele) {
                        return getColorForRelationship(ele.data('label').toLowerCase());
                    },
                    'curve-style': 'bezier',
                    'label': 'data(label)',
                    'text-rotation': 'autorotate',
                    'text-margin-y': '-10px',
                    'font-size': '15px',
                    'font-family': "'Dancing Script', cursive",
                    'font-weight': 'normal',
                    'text-wrap': 'wrap',
                    'text-max-width': '80px',
                    'z-index': 1
                }
            },
            {
                selector: 'node.highlighted',
                style: {
                    'background-color': '#F3A475',
                    'border-color': '#ed732a',
                    'border-width': '2px',
                    'color': '#000'
                }
            }
        ],
        layout: {
            name: 'cose',
            idealEdgeLength: 150,
            nodeOverlap: 20,
            refresh: 20,
            fit: true,
            padding: 100,
            randomize: false,
            componentSpacing: 100,
            nodeRepulsion: 400000,
            edgeElasticity: 100,
            nestingFactor: 5,
            gravity: 80,
            numIter: 1000,
            initialTemp: 200,
            coolingFactor: 0.95,
            minTemp: 1.0
        },
        minZoom: 0.2,
        maxZoom: 3,
        wheelSensitivity: 0.2
    }).on('mouseover', 'node', function(event) {
        const node = event.target;
        const id = node.data('id');
        const label = node.data('label');
        
        tooltip.innerHTML = `<span>${label}</span>: ${id}`;
        tooltip.style.display = 'block';
        
        const renderedPosition = node.renderedPosition();
        const containerBox = container.getBoundingClientRect();
        
        tooltip.style.left = `${containerBox.left + renderedPosition.x + 45}px`;
        tooltip.style.top = `${containerBox.top + renderedPosition.y - 40}px`;
    }).on('mouseout', 'node', function() {
        tooltip.style.display = 'none';
    }).on('mousemove', 'node', function(event) {
        const node = event.target;
        const renderedPosition = node.renderedPosition();
        const containerBox = container.getBoundingClientRect();
        
        tooltip.style.left = `${containerBox.left + renderedPosition.x + 10}px`;
        tooltip.style.top = `${containerBox.top + renderedPosition.y - 10}px`;
    });
}


function getEdgeWidth(relationship) {
    const magnitudeMap = {
        'first-line treatment': 8,
        'definition': 8,
        'highly effective': 8,
        'treats': 8,
        'more effective': 6,
        'comparable to': 6,
        'side effects': 6,
        'associated with': 6,
        'second-line treatment': 4,
        'less effective': 4,
        'symptom': 4,
        'properties': 2,
        'less commonly used': 2,
        'specific efficacy in treating': 2,
        'most effective': 2,
        'more effective than': 2,
        'effective': 2,
        'more efficacious': 2,
        'treatment options': 2,
        'potential alternative': 2,
        'overview': 2,
        'goal': 2,
        'better acceptability': 2,
        'more favorable': 2,
        'more tolerable': 2,
        'more commonly used': 2,
        'widely used': 2,
        'recommendation': 2,
        'recommended': 2
    };

    return magnitudeMap[relationship] || 1;
}

function getColorForRelationship(relationship) {
    const colorMap = {
        'reduces': '#A0E1A0',
        'increases': '#A0E1A0',
        'properties': '#A0E1A0',
        
        'recommendation': '#FAD02E',
        'recommended': '#FAD02E',
        'first-line treatment': '#FAD02E',
        'second-line treatment': '#FAD02E',
        'treatment options': '#FAD02E',
        'goal': '#FAD02E',
        
        'side effects': '#FF6B6B',
        'less effective': '#FF6B6B',
        'potential alternative': '#FF6B6B',
        'dosage': '#FF6B6B',
        'details': '#FF6B6B',
        'less well tolerated': '#FF6B6B',
        'less tolerated than': '#FF6B6B',
        
        'enhances': '#77aad4',
        'interacts with': '#77aad4',
        'alternative to': '#77aad4',
        'form of': '#77aad4',
        'treats': '#77aad4',
        
        'risk factor for': '#a891f2',
        'eligibility': '#a891f2',
        'requirements': '#a891f2',
        
        'symptom': '#fd91ca',
        'definition': '#fd91ca',
        'overview': '#fd91ca',
        'synonym': '#fd91ca',
        'associated with': '#fd91ca',
        'example': '#fd91ca',
        'short form': '#fd91ca',
        
        'subset': '#4DB6AC',
        'results': '#4DB6AC',
        'more common than in': '#4DB6AC',
        'same efficacy as for': '#4DB6AC',
        'more effective': '#4DB6AC',
        'highly effective': '#4DB6AC',
        'benefits': '#4DB6AC',
        'well tolerated': '#4DB6AC',
        'more effective than': '#4DB6AC',
        'least efficacious and acceptable': '#4DB6AC',
        'among most efficacious': '#4DB6AC',
        
        'consistency': '#4DB6AC',
        'moderately effective': '#4DB6AC',
        'widely used': '#4DB6AC',
        'more commonly used': '#4DB6AC',
        'less commonly used': '#4DB6AC',
        'not effective': '#FF6B6B',
        'specific efficacy in treating': '#4DB6AC',
        'comparable to': '#4DB6AC'
    };
        
    return colorMap[relationship.toLowerCase()] || '#CCCCCC';
}

function getRelationshipCategories() {
    return {
        'Reduces and Increases Effects': {
            color: '#A0E1A0',  // green
            id: 'reduces-increases'
        },
        'Clinical Recommendations and Guidelines': {
            color: '#FAD02E',  // yellow
            id: 'clinical-recommendations'
        },
        'Side Effects and Limitations': {
            color: '#FF6B6B',  // red
            id: 'side-effects'
        },
        'Interactions and Usage Patterns': {
            color: '#77aad4',  // blue
            id: 'interactions'
        },
        'Risk Factors and Requirements': {
            color: '#a891f2',  // purple
            id: 'risk-factors'
        },
        'Symptoms and General Information': {
            color: '#fd91ca',  // pink
            id: 'symptoms'
        },
        'Comparative Effectiveness and Clinical Outcomes': {
            color: '#4DB6AC',  // teal
            id: 'comparative-effectiveness'
        }
    };
}

function createFilterPanel() {
    const filterPanel = document.createElement('div');
    filterPanel.id = 'filter-panel';
    filterPanel.className = 'filter-panel';

    // Header with title and minimize button
    const header = document.createElement('div');
    header.className = 'panel-header';
    
    const title = document.createElement('h3');
    title.textContent = 'Filter Relationships';
    header.appendChild(title);

    const minimizeBtn = document.createElement('span');
    minimizeBtn.textContent = '−';  // or '+'
    minimizeBtn.style.cursor = 'pointer';
    minimizeBtn.style.marginLeft = 'auto';
    minimizeBtn.onclick = () => {
        filterPanel.classList.toggle('minimized');
        minimizeBtn.textContent = filterPanel.classList.contains('minimized') ? '+' : '−';
    };
    header.appendChild(minimizeBtn);

    filterPanel.appendChild(header);

    // Categories and checkboxes
    const categories = getRelationshipCategories();
    
    Object.entries(categories).forEach(([category, info]) => {
        const filterItem = document.createElement('div');
        filterItem.className = 'filter-item';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `filter-${info.id}`;
        checkbox.checked = true;
        checkbox.addEventListener('change', () => toggleRelationshipVisibility(category, info.color));
        
        const label = document.createElement('label');
        label.htmlFor = `filter-${info.id}`;
        label.innerHTML = `<span class="color-dot" style="background-color: ${info.color}"></span>${category}`;
        
        filterItem.appendChild(checkbox);
        filterItem.appendChild(label);
        filterPanel.appendChild(filterItem);
    });

    // Add "Select All" and "Clear All" buttons
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'filter-buttons';
    
    const selectAllBtn = document.createElement('button');
    selectAllBtn.textContent = 'Select All';
    selectAllBtn.onclick = () => toggleAll(true);
    
    const clearAllBtn = document.createElement('button');
    clearAllBtn.textContent = 'Clear All';
    clearAllBtn.onclick = () => toggleAll(false);
    
    buttonContainer.appendChild(selectAllBtn);
    buttonContainer.appendChild(clearAllBtn);
    filterPanel.appendChild(buttonContainer);

    // Dragging functionality
    let isDragging = false;
    let offsetX, offsetY;

    header.addEventListener('mousedown', (e) => {
        isDragging = true;
        offsetX = e.clientX - filterPanel.offsetLeft;
        offsetY = e.clientY - filterPanel.offsetTop;
    });

    document.addEventListener('mousemove', (e) => {
        if (isDragging) {
            filterPanel.style.left = e.clientX - offsetX + 'px';
            filterPanel.style.top = e.clientY - offsetY + 'px';
        }
    });

    document.addEventListener('mouseup', () => {
        isDragging = false;
    });

    return filterPanel;
}



function toggleAll(state) {
    const categories = getRelationshipCategories();
    Object.entries(categories).forEach(([category, info]) => {
        const checkbox = document.getElementById(`filter-${info.id}`);
        if (checkbox) {
            checkbox.checked = state;
            toggleRelationshipVisibility(category, info.color);
        }
    });
}

function toggleRelationshipVisibility(category, color) {
    const checkbox = document.getElementById(`filter-${getRelationshipCategories()[category].id}`);
    const isVisible = checkbox.checked;
    
    // Find all edges with the corresponding color
    const edges = cy.edges().filter(edge => {
        const edgeColor = getColorForRelationship(edge.data('label').toLowerCase());
        return edgeColor === color;
    });
    
    if (isVisible) {
        edges.style('display', 'element');
    } else {
        edges.style('display', 'none');
    }
} 

function findNode() {
    if (!cy) {
        console.error('Cytoscape instance not initialized');
        return;
    }

    const query = document.getElementById("searchInput").value.toLowerCase();
    if (!query) {
        cy.nodes().removeClass('highlighted');
        return;
    }

    const allNodes = cy.nodes();
    allNodes.removeClass('highlighted');

    const matchedNodes = allNodes.filter(node => 
        node.data('label') && 
        node.data('label').toLowerCase().includes(query)
    );

    if (matchedNodes.length > 0) {
        matchedNodes.addClass('highlighted');
        cy.fit(matchedNodes, 50);
    } else {
        alert("No matches found.");
    }
}

function processDataForCytoscape(data) {
    const elements = {
        nodes: [],
        edges: []
    };
    
    const addedNodes = new Set();
    
    data.forEach(item => {
        if (!addedNodes.has(item.subj)) {
            elements.nodes.push({
                data: {
                    id: item.subj,
                    label: item.subjsummary
                }
            });
            addedNodes.add(item.subj);
        }
        
        if (!addedNodes.has(item.obj)) {
            elements.nodes.push({
                data: {
                    id: item.obj,
                    label: item.objsummary
                }
            });
            addedNodes.add(item.obj);
        }
        
        elements.edges.push({
            data: {
                id: `${item.subj}-${item.obj}`,
                source: item.subj,
                target: item.obj,
                label: item.rel
            }
        });
    });
    
    return elements;
}

function showLoading() {
    const loadingText = document.getElementById('loadingtext');
    if (loadingText) {
        loadingText.style.display = 'block';
    }
}

function hideLoading() {
    const loadingText = document.getElementById('loadingtext');
    if (loadingText) {
        loadingText.style.display = 'none';
    }
}

async function updateGraph() {
    const cyContainer = document.getElementById('cy');
    if (!cyContainer) {
        console.error('Graph container not found');
        return;
    }

    showLoading();

    try {
        const response = await fetch('/get_results');
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }

        const data = await response.json();
        const processedData = processDataForCytoscape(data);
        
        cy = initializeCytoscape(cyContainer);
        cy.elements().remove();
        cy.add(processedData);
        
        cy.layout({
            name: 'cose',
            padding: 50
        }).run();
        
        cy.on('tap', 'node', function(evt) {
            const node = evt.target;
            console.log('Clicked node:', node.data('label'));
        });

        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', findNode);
        }
        
        return cy;
    } catch (error) {
        console.error('Error updating graph:', error);
        cyContainer.innerHTML = '<p>Error loading graph</p>';
    } finally {
        hideLoading();
    }
}

async function handleUpload(formData) {
    showLoading();
    
    try {
        const uploadResponse = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!uploadResponse.ok) {
            throw new Error('Upload failed');
        }

        const uploadResult = await uploadResponse.json();
        console.log('Upload result:', uploadResult);

        await updateGraph();
    } catch (error) {
        console.error('Error during upload process:', error);
        const cyContainer = document.getElementById('cy');
        if (cyContainer) {
            cyContainer.innerHTML = '<p>Error uploading files and updating graph</p>';
        }
    } finally {
        hideLoading();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const fetchButton = document.getElementById('fetchButton');
    if (fetchButton) {
        fetchButton.addEventListener('click', async (event) => {
            event.preventDefault();
            await updateGraph();
        });
    }

    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(uploadForm);
            await handleUpload(formData);
        });
    }

    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', findNode);
    }
});

export { updateGraph, processDataForCytoscape, getColorForRelationship, findNode };