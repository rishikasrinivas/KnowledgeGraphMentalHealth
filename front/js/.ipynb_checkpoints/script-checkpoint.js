// just maintain whitespace
function preTitle(text) {
  const container = document.createElement("pre");
  container.innerText = text;
  return container;
}

// HTML parsing with all XSS goodness
function htmlTitle(html) {
  const container = document.createElement("div");
  container.innerHTML = html;
  return container;
}

// create an array with nodes
var nodes = new vis.DataSet([
  { id: 1, label: "PRE", title: preTitle("ASCII\n    art")},
  {
    id: 2,
    label: "HTML",
    title: htmlTitle(
      "Go wild <span style='display: inline-block; animation: be-tacky 5s ease-in-out alternate infinite; margin: 5px;'>!</span>"
    ),
  },
  { id: 3, label: "PRE", title: preTitle("ASCII\n    art") },
]);

// create an array with edges
var edges = new vis.DataSet([
  { from: 1, to: 2, label: "PRE", title: preTitle("ASCII\n    art") },
  {
    from: 2,
    to: 3,
    arrows: "to",
    label: "HTML",
    title: htmlTitle(
      "Go wild <span style='display: inline-block; animation: be-tacky 5s ease-in-out alternate infinite; margin: 5px;'>!</span>"
    ),
  },
]);

// create a network
var container = document.getElementById("mynetwork");
var data = {
  nodes: nodes,
  edges: edges,
};
var options = {};
var network = new vis.Network(container, data, options);
