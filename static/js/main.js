window.onload = function() {
  visual = new Visual();

  var page = document.getElementById('page');
  visual.update(page.value);
  console.log(page);
  page.focus();
  // page.selectionStart = page.value.length;
  // page.selectionEnd = page.value.length;

  var dirty = false;
  var overload = 0;
  var minUpdateInterval = 100
  var maxUpdateInterval = 1000

  page.onkeypress = function(event) {
    char = event.which || event.charCode
    dirty = true;

    // if ws (space or enter) & not overloaded
    if ((char == 32 || char == 13) && overload == 0) {
      console.log('updating because ws')
      visual.update(page.value)
      dirty = false;

      // keep track of overload to prevent too many api calls
      overload += 1
      setTimeout(function() {
        overload -= 1;
      }, minUpdateInterval)
    }

  };

  // periodically update if needed (dirty)
  setInterval(function() {
    if (dirty) {
      console.log('updating because dirty')
      visual.update(page.value);
      dirty = false;
    }
  }, maxUpdateInterval);
};
