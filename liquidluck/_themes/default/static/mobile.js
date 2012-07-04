// iOS scaling bug fix
// Rewritten version
// By @mathias, @cheeaun and @jdalton
// Source url: https://gist.github.com/901295
(function(doc) {
  var addEvent = 'addEventListener',
      type = 'gesturestart',
      qsa = 'querySelectorAll',
      scales = [1, 1],
      meta = qsa in doc ? doc[qsa]('meta[name=viewport]') : [];
  function fix() {
    meta.content = 'width=device-width,minimum-scale=' + scales[0] + ',maximum-scale=' + scales[1];
    doc.removeEventListener(type, fix, true);
  }
  if ((meta = meta[meta.length - 1]) && addEvent in doc) {
    fix();
    scales = [0.25, 1.6];
    doc[addEvent](type, fix, true);
  }
}(document));

// fix navigation for mobile
(function(d) {
    if (!d.querySelectorAll || d.body.clientWidth > 560) {
        return;
    }
    var nav = d.getElementById('nav');
    var links = nav.querySelectorAll('a');
    var select = d.createElement('select');
    select.appendChild(createOption('nav', '#'));
    for (var i = 0; i < links.length; i++) {
        var link = links[i];
        var option = createOption(link.innerHTML, link.href);
        nav.removeChild(link);
        select.appendChild(option);
    }
    select.onchange = function() {
        location.href = select.value;
    }
    nav.appendChild(select);

    function createOption(name, link) {
        var option = d.createElement('option');
        option.value = link; option.innerHTML = name;
        if (location.href == link) {
            option.selected = true;
        }
        return option;
    }
}(document));
