function loadCSVData(csvFile, callback) {
  Papa.parse(csvFile, {
    download: true,
    header: true,
    complete: function (results) {
      callback(results.data);
    },
    error: function (err) {
      console.error("Error loading CSV file:", err);
    }
  });
}
// Assuming you have a button or some event to trigger this function

// Function to process CSV data into Cytoscape format
function processCSVData(data) {
  const nodes = {};
  const edges = [];

  data.forEach(item => {
    const subSum=item.subjSumm;
    const source = item.subj;
    const target = item.obj;
    const objSum=item.objSumm;
    const relationship = item.rel;
    const description = "No desc";
    // Add unique nodes
    if (source && !nodes[source]) {
      nodes[source] = { data: { id: source, label: source,description: description || 'No description available' } };
    }
    if (target && !nodes[target]) {
      nodes[target] = { data: { id: target, label: target,description: description || 'No description available' } };
    }

    // Add edges
    if (source && target && relationship) {
      edges.push({
        data: {
          source: source,
          target: target,
          relationship: relationship,
          weight: 1 || 1,  // Convert weight to integer, default to 1
          label: relationship ,           // Label the edge with the relationship type
           description: "empty"
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
function getRandomColor() {
  console.log("ent random")
  let letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color
}

// Function to initialize Cytoscape with dynamically loaded data
export function initCytoscape(graphData) {
  console.log("ent init,", graphData)
  let edges_lab = Array.from(new Set(graphData.edges.map(edges => edges.data.label)))

  let labeltocolor = {}
  edges_lab.forEach(l => {
    labeltocolor[l] = getRandomColor();
  });

  console.log("Edges labels ", edges_lab)
    
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
          'color': '#000',
          'font-size': '10px',
          'width': '40px',   // Modern, larger nodes
          'height': '40px',
          'border-color': '#ccc',
          'border-width': '2px',
          'border-opacity': '0.8',
          'shape': 'ellipse',
        }

      },

      ...edges_lab.map(label => ({
        selector: 'edge',
        style: {
          'width': 4,
          'line-color': labeltocolor[label],
          'target-arrow-color': labeltocolor[label],
          'target-arrow-shape': 'triangle',
          'label': 'data(label)',
          'curve-style': 'bezier',
        }
      }))


    ],
    

    layout: {
      name: 'cose',  // COSE layout for automatic positioning
      animate: true,
        fit: true, // Fit the graph to the container
            padding: 30,
    }
  });
    
  console.log("applied layout")
  cy.edges().forEach(edge => {
    const label = edge.data('label');  // Get the label for the current edge
    if (label && labeltocolor[label]) {
      edge.style({
        'line-color': labeltocolor[label],
        'target-arrow-color': labeltocolor[label],
      });
    }
  });

  // Handle click event on nodes
  cy.on('click', 'node', function (evt) {
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

  cy.on('mouseover', 'node', function (event) {
    var node = event.target
    node.connectedEdges().addClass('highlighted');
    node.connectedNodes().addClass('highlighted');
    console.log("clikced")
  }

  );
  // Hide the pop-up when clicking elsewhere
  cy.on('click', function (event) {
    console.log("Events target is ", event.target)
    if (event.target === cy) {


      document.getElementById('popup').style.display = 'none';
    }
  });
}

export function make_kg(data){
    const graphData = processCSVData(data);
    initCytoscape(graphData);
    console.log("Made")
}