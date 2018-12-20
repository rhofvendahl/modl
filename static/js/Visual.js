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
    .then(function(response) {
      return response.json();
    })
    .then(function(json) {
      console.log(json);

      var newIds = []

      var entities = json.model.entities;
      entities.forEach(function(entity) {
        var id = 'e' + entity.id;
        newIds.push(id);
        self.nodes.update({
          id: id,
          label: entity.text,
          title: entity.class
        });
      });

      var statements = json.model.statements;
      statements.forEach(function(statement) {
        var id = 's' + statement.id;
        newIds.push(id);
        self.nodes.update({
          id: id,
          label: statement.subject_text + ' ' + statement.predicate_text + ' ' + statement.object_text,
          title: statement.weight
        });
        if (statement.subject_id != undefined) {
          self.edges.update({
            id: id,
            to: 'e' + statement.subject_id,
            from: id
          });
        }
      });



    //   var resolved = document.getElementById('resolved');
    //   resolved.innerHTML = json.model.resolved_text;
    //
    //   var newIds = []
    //   var people = json.model.people
    //   console.log(people.length)
    //   for (var i = 0; i < people.length; i++) {
    //     var person = people[i];
    //     var personId = 'people/' + person.name;
    //     newIds.push(personId);
    //     self.nodes.update({
    //       id: personId,
    //       label: person.name
    //     });
    //
    //     var statements = person.statements
    //     for (var j = 0; j < statements.length; j++) {
    //       var statement = statements[j];
    //       var statementId = 'people/' + person.name + '/statements/' + j
    //       newIds.push(statementId);
    //       self.nodes.update({
    //         id: statementId,
    //         label: statement.cue + ' - ' + statement.fragment
    //       });
    //       self.edges.update({
    //         id: statementId,
    //         to: personId,
    //         from: statementId
    //       })
    //     }
    //   }
    //
      // remove additional nodes
      self.nodes.getIds().forEach(function(id) {
        remove = true
        newIds.forEach(function(newId) {
          if (id == newId) remove = false;
        });
        if (remove) {
          self.nodes.remove(id);
        }
      });
    });
    // TODO: make it so it chains requests if dirty
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
