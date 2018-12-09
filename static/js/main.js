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
  var maxUpdateFrequency = 2;

  page.oninput = function(event) {
    dirty = true;

    // update if not overloaded
    if (overload == 0) {
      visual.update(page.value)
      dirty = false;

      // increment overload for a bit after updating
      overload += 1
      setTimeout(function() {
        overload -= 1;

        // update after waiting in case dirty
        if (dirty) {
          visual.update(page.value);
          dirty = false;
        }
      }, 1000 / maxUpdateFrequency)
    }
  };
};
