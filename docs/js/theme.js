// Theme toggle — 昼/夜 切换
(function(){
  var KEY = 'tianwen-kb-theme';
  var saved = localStorage.getItem(KEY) || 'dark';
  document.documentElement.setAttribute('data-theme', saved);

  function setTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem(KEY, t);
    updateUI(t);
  }

  function updateUI(t) {
    var d = document.getElementById('theme-day');
    var n = document.getElementById('theme-night');
    if (d) d.style.fontWeight = (t === 'light') ? '700' : '400';
    if (n) n.style.fontWeight = (t === 'dark') ? '700' : '400';
  }

  // Expose to inline onclick
  window._switchTheme = function(t) { setTheme(t); };

  // Update UI on load
  document.addEventListener('DOMContentLoaded', function() {
    updateUI(document.documentElement.getAttribute('data-theme') || 'dark');
  });
})();
