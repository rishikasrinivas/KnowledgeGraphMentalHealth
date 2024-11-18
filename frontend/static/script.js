// Global variable to store Cytoscape instance
let cy;

function initializeCytoscape(container) {
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
                    'font-size': '14px',
                    'font-family': "'Poppins', sans-serif",
                    'text-wrap': 'wrap',
                    'text-max-width': '80px',
                    'width': '100px',
                    'height': '100px',
                    'min-zoomed-font-size': 8,
                    'border-width': '2px',
                    'border-color': '#F3F4F7',
                    'border-opacity': 0.8,
                    'padding': '5px',
                    'shape': 'ellipse',
                    'text-margin-y': 5,
                    'text-overflow-wrap': 'break-word',
                    'text-outline-color': '#bbe7e8',
                    'text-outline-width': 2,
                    'overlay-padding': '6px',
                    'z-index': 10,
                    'word-wrap': 'break-word', 
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
                    'font-size': '12px',
                    'font-family': "'Dancing Script', cursive",  // Cute, cursive font for edges
                    'font-weight': 'normal',  // Lighter font weight for edges
                    'text-wrap': 'wrap',
                    'text-max-width': '80px',
                    'z-index': 1
                }
            },
            {
                selector: 'node.highlighted',
                style: {
                    'background-color': '#F3A475',  // Matching  CSS color
                    'border-color': '#ed732a',
                    'border-width': '2px',
                    'color': '#000'
                }
            }
        ],
        layout: {
            name: 'cose',
            idealEdgeLength: 120,
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
    });
}

// Function to get edge width based on relationship magnitude
function getEdgeWidth(relationship) { // can be changed as needed 
    const magnitudeMap = {
        'first-line treatment': 4,
        'definition': 4,
        'highly effective': 4,
        'treats': 4,
        'more effective': 3,
        'comparable to': 3,
        'side effects': 3,
        'associated with': 3,
        'side effects': 2,
        'second-line treatment': 2,
        'less effective': 2,
        'symptom': 2,
        'properties': 1,
        'less commonly used': 1,
        'specific efficacy in treating': 1,
        'less effective': 1,
        'most effective': 1,
        'more effective than': 1,
        'effective': 1,
        'specific efficacy in treating': 1,
        'more efficacious': 1,
        'highly effective': 1,
        'treatment options': 1,
        'potential alternative': 1,
        'overview': 1,
        'goal': 1,
        'better acceptability': 1,
        'more favorable': 1,
        'more tolerable': 1,
        'more commonly used': 1,
        'widely used': 1,
        'recommendation': 1,
        'recommended': 1
    };

    return magnitudeMap[relationship] || 1;
}

function getColorForRelationship(relationship) {
    const colorMap = {
        'treatment options': '#FFB3BA',
        'treatment types': '#FFB3BA',
        'treats': '#FFB3BA',
        'first-line treatment': '#FFB3BA',
        'second-line treatment': '#FFB3BA',
        'definition': '#77aad4',
        'properties': '#77aad4',
        'overview': '#77aad4',
        'goal': '#77aad4',
        'symptom': '#FFEB99',
        'less commonly used': '#a891f2',
        'more commonly used': '#a891f2',
        'more common than': '#a891f2',
        'widely used': '#a891f2',
        'most effective': '#A0E1A0',
        'more effective than': '#A0E1A0',
        'effective': '#A0E1A0',
        'more effective': '#A0E1A0',
        'more efficacious': '#A0E1A0',
        'highly effective': '#A0E1A0',
        'better acceptability': '#A0E1A0',
        'more favorable': '#A0E1A0',
        'more tolerable': '#A0E1A0',
        'comparable to': '#A0E1A0',
        'associated with': '#A0E1A0',
        'specific efficacy in treating': '#A0E1A0',
        'side effects': '#FF6B6B',
        'less effective': '#FF6B6B',
        'potential alternative': '#FF6B6B',
        'recommendation': '#FAD02E',
        'recommended': '#FAD02E'
    };
    return colorMap[relationship.toLowerCase()] || '#CCCCCC';
}

// Updated search function
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

// Add event listener to search button if not using inline HTML event
document.querySelector('.search-button').addEventListener('click', findNode);

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

// Update the graph initialization to include highlight styles
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
        
        // Initialize or reset Cytoscape instance
        cy = initializeCytoscape(cyContainer);
        cy.elements().remove();
        cy.add(processedData);
        
        // Apply layout
        cy.layout({
            name: 'cose',
            padding: 50
        }).run();
        
        
        // Add event listeners
        cy.on('tap', 'node', function(evt) {
            const node = evt.target;
            console.log('Clicked node:', node.data('label'));
        });

        // Add search input event listener
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

    // Add search input event listener
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', findNode);
    }
});

export { updateGraph, processDataForCytoscape, getColorForRelationship, findNode };