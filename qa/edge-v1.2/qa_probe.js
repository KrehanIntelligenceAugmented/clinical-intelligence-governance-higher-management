/* Prueflogik, die im Browser gegen die Fassung v1.2 laeuft. */
window.__probe = function () {
  var all = [].slice.call(document.querySelectorAll('.screen'));
  var vis = all.filter(function (s) {
    var c = getComputedStyle(s);
    return c.visibility !== 'hidden' && +c.opacity > 0.01;
  });
  var act = document.querySelector('.screen.is-active');
  var st = act.querySelector('.stage'), r = st.getBoundingClientRect();
  var bar = document.querySelector('.bar').getBoundingClientRect();
  var inner = act.querySelector('.inner').getBoundingClientRect();
  var overlap = !(inner.right < bar.left || inner.left > bar.right ||
                  inner.bottom < bar.top || inner.top > bar.bottom);
  var outside = [].slice.call(act.querySelectorAll('.inner *')).filter(function (e) {
    var b = e.getBoundingClientRect();
    if (!b.width && !b.height) return false;
    return b.left < r.left - 2 || b.right > r.right + 2 ||
           b.top < r.top - 2 || b.bottom > r.bottom + 2;
  }).length;
  var map = document.getElementById('map');
  return {
    vp: innerWidth + 'x' + innerHeight,
    dpr: window.devicePixelRatio,
    sichtbareScreens: vis.length,
    aktiv: act.id,
    k: +(+getComputedStyle(st).getPropertyValue('--k')).toFixed(3),
    buehneImViewport: r.top >= -1 && r.bottom <= innerHeight + 1 &&
                      r.left >= -1 && r.right <= innerWidth + 1,
    buehneUeberLeiste: r.bottom <= bar.top + 1,
    leisteUeberlappt: overlap,
    inhaltAusserhalb: outside,
    dokumentScrollt: document.documentElement.scrollHeight >
                     document.documentElement.clientHeight + 1,
    uebersichtUnsichtbar: map.hidden && getComputedStyle(map).display === 'none'
  };
};
