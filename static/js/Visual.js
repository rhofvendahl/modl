var Visual = function() {
  var self = this;

  self.nodes = new vis.DataSet();
  self.edges = new vis.DataSet();

  var container = document.getElementById('visual');
  var data = {nodes: self.nodes, edges: self.edges};
  var options = {};
  self.network = new vis.Network(container, data, options);

  // self.tokenNodes = []
  //
  // //// DOESN'T BELONG
  // // RETURN TOKENNODE BY ID
  // self.getTokenNode = function(id) {
  //   var match = null;
  //   self.tokenNodes.forEach(function(tokenNode) {
  //     if (tokenNode.id == id) match = tokenNode;
  //   });
  //   return match;
  // }
  //
  // // GENERATE TOKENNODES FROM TOKENS, render
  // self.importSubtree = function(tokens, token) {
  //   if (token.dep != 'punct') {
  //     tokenNode = new TokenNode(self, token);
  //     self.tokenNodes.push(tokenNode);
  //     token.child_ids.forEach(function(childId) {
  //       self.importSubtree(tokens, tokens[childId])
  //     });
  //   }
  // }
  //
  // self.renderSubtree = function(tokenNode) {
  //   tokenNode.render();
  //   tokenNode.children.forEach(function(child) {
  //     self.renderSubtree(child);
  //   });
  // }
  //// BELONS HERE
  // PROCESS QUERY, DISPLAY RESULTS
  self.update = function(text) {
    fetch('/model', {
      method: 'post',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: text
      })
    })
    // .then(function(response) {
    //   return response.json();
    // })
    // .then(function(json) {
    //   console.log(json);
    //   names = json.names;
    //   resolved_text = json.resolved;
    //
    //   var resolved = document.getElementById('resolved');
    //   resolved.innerHTML = resolved_text;
    //
    //   for (var i = 0; i < names.length; i++) {
    //     self.nodes.update({
    //       id: i,
    //       label: names[i]
    //     });
    //   }
    //   // for (var i = 0; i < predictions.length; i++) {
    //   //   var p = predictions[i];
    //   //   if (p.neutral < .2) {
    //   //     var title = 'e' + p.entailment.toFixed(1) +
    //   //       '-c' + p.contradiction.toFixed(1) +
    //   //       '-n' + p.neutral.toFixed(1)
    //   //     self.edges.update({
    //   //       id: i,
    //   //       from: p.premise,
    //   //       to: p.hypothesis,
    //   //       label: ((p.entailment + (1 - p.contradiction)) / 2).toFixed(1).toString(),
    //   //       title: title,
    //   //       arrows: 'to',
    //   //       physics: false,
    //   //       width: (1 - p.neutral) * 2
    //   //     });
    //   //   }
    //   // }
    //
    //   // remove additional nodes
    //   self.nodes.getIds().forEach(function(id) {
    //     if (id >= names.length) {
    //       self.nodes.remove(id);
    //     }
    //   });
    // });
  };

  //// BELONGS HERE
  // COLLAPSE SUBTREE WHEN CLICKED
//   self.network.on('click', function(properties) {
//     if (properties.nodes.length > 0) {
//       tokenNode = self.getTokenNode(properties.nodes[0]);
//       tokenNode.collapsed = !tokenNode.collapsed;
//       self.renderSubtree(tokenNode);
//     }
//   });
};
