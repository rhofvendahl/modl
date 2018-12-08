window.onload = function() {
  visual = new Visual();

  var page = document.getElementById('page');
  console.log(page);
  page.focus();
  // page.selectionStart = page.value.length;
  // page.selectionEnd = page.value.length;
  // visual.update(page.value);

  var dirty = false;
  var overload = 0;
  var minUpdateInterval = 500

  page.onkeydown = function(event) {
    var dirty = true;
    var char = event.which || event.keyCode;
    console.log(char)

    // if whitespace (space or enter) & not overloaded
    if ((char == 32 || char == 13) && overload == 0) {
      visual.update(page.value)
      dirty = false;
    }

    // keep track of overload to prevent too many api calls
    overload += 1
    setTimeout(function() {
      overload -= 1;
    }, minUpdateInterval)
  };

  // periodically update if needed (dirty)
  setInterval(function() {
    if (dirty) {
      parseTree.process(input.value);
      dirty = false;
    }
  }, minUpdateInterval);
};
