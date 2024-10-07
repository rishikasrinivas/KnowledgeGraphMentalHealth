function loadCSVData(csvFile, callback) {
    Papa.parse(csvFile, {
      download: true,
      header: true,
      complete: function(results) {
        callback(results.data);
      },
      error: function(err) {
        console.error("Error loading CSV file:", err);
      }
    });
  }

  // Function to process CSV data into Cytoscape format
function processCSVData(data) {
    const nodes = {};
    const edges = [];
    
    data.forEach(row => {
      const source = row['subj'];
      const target = row['obj'];
      const relationship = row['rel'];
      const weight = row['weight'];
      const description = row['description'];  // Assume CSV has 'description' field
    
      // Add unique nodes
      if (source && !nodes[source]) {
        nodes[source] = { data: { id: source, label: source, description: description || 'No description available' } };
      }
      if (target && !nodes[target]) {
        nodes[target] = { data: { id: target, label: target, description: description || 'No description available' } };
      }
    
      // Add edges
      if (source && target && relationship) {
        edges.push({
          data: {
            source: source,
            target: target,
            relationship: relationship,
            weight: parseInt(weight, 10) || 1,  // Convert weight to integer, default to 1
            label: relationship            // Label the edge with the relationship type
          }
        });
      }
    });
    
    // Convert nodes object to array
    return {
      nodes: Object.values(nodes),
      edges: edges
    };
    }

// Function to initialize Cytoscape with dynamically loaded data
function initCytoscape(graphData) {
    const cy = cytoscape({
      container: document.getElementById('cy'),
    
      elements: graphData,
    
      style: [
        {
          selector: 'node',
          style: {
            'label': 'data(label)',
            'background-color': '#666',
            'text-valign': 'center',
            'text-halign': 'center',
            'color': '#fff',
            'font-size': '10px',
            'width': '40px',   // Modern, larger nodes
            'height': '40px',
            'border-color': '#ccc',
            'border-width': '2px',
            'border-opacity': '0.8',
            'shape': 'ellipse'
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 'mapData(weight, 1, 5, 2, 10)',  // Dynamic width based on weight
            'line-color': function(ele) {
              return ele.data('relationship') === 'associated with' ? 'blue' : 'red'; // Customize colors as needed
            },
            'curve-style': 'bezier',  // Smooth curved edges
            'target-arrow-shape': 'triangle',
            'target-arrow-color': function(ele) {
              return ele.data('relationship') === 'associated with' ? 'blue' : 'red'; // Customize arrow colors
            },
            'arrow-scale': 1.5,  // Larger arrowheads for modern look
            'line-style': 'solid',
            'opacity': 0.8,
            'overlay-padding': '6px',  // Creates better padding around the edges
            'z-index': 9999,
            'label': 'data(label)',  // Display relationship type as label
            'font-size': '8px',  // Small font for edge labels
            'text-rotation': 'autorotate',  // Rotates text to align with edge direction
            'text-margin-y': -10,  // Position label closer to the edge
            'color': '#555'  // Darker color for labels for better readability
          }
        }
      ],
    
      layout: {
        name: 'cose',  // COSE layout for automatic positioning
        animate: true
      }
    });
    
    // Handle click event on nodes
    cy.on('click', 'node', function(evt) {
      const node = evt.target;
      const description = node.data('description'); // Fetch node description
    
      const popUp = document.getElementById('popup');
      popUp.style.display = 'block';
      popUp.innerHTML = `<strong>${node.data('label')}</strong><br>${description}`;
    
      // Get node position and adjust pop-up position
      const nodePosition = node.renderedPosition();
      const containerPosition = document.getElementById('cy').getBoundingClientRect();
      popUp.style.left = (containerPosition.left + nodePosition.x + 10) + 'px';
      popUp.style.top = (containerPosition.top + nodePosition.y + 10) + 'px';
    });
    
    // Hide the pop-up when clicking elsewhere
    cy.on('click', function(event) {
        console.log("Events target is ", event.target)
      if (event.target === cy) {
          
        
        document.getElementById('popup').style.display = 'none';
      }
    });
    }

// Load the CSV and initialize the graph
loadCSVData('knowledge_graph_data.csv', function(data) {
    console.log("called")
    const graphData = processCSVData(data);
    initCytoscape(graphData);
});