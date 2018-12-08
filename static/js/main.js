window.onload = function() {
  // model = new Model();

  var input = document.getElementById('page');
  input.focus();
  input.selectionStart = input.value.length;
  input.selectionEnd = input.value.length;

  // model.update(input.value);

  // // don't update constantly if timeOuts overlap
  // var timeOuts = 0;
  document.oninput = function(event) {
    // event.which?
    console.log(event.code)
    // if (event.code == )
    // var updated = false;
    // if (timeOuts == 0) {
    //   parseTree.process(input.value);
    //   var updated = true;
    // }
    // timeOuts += 1
    // setTimeout(function() {
    //   timeOuts -= 1;
    //   if (timeOuts == 0 && !updated) parseTree.process(input.value);
    // }, 100)
  };
  //
  // // update at intervals if timeOuts overlap
  // setInterval(function() {
  //   if (timeOuts > 1) parseTree.process(input.value)
  // }, 100);

  // setInterval(function() {
  //   model.update(input.value);
  // }, 3000);
}
