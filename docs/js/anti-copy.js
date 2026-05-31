/* Anti-copy protection — disable right-click, Ctrl+C, Ctrl+A, Ctrl+S, F12 */
(function(){
    document.addEventListener('contextmenu', function(e){ e.preventDefault(); return false; });
    document.addEventListener('keydown', function(e){
        if (e.ctrlKey && (e.key === 'c' || e.key === 'C' || e.key === 'a' || e.key === 'A' || e.key === 's' || e.key === 'S' || e.key === 'u' || e.key === 'U')) {
            e.preventDefault(); return false;
        }
        if (e.key === 'F12') { e.preventDefault(); return false; }
    });
    document.addEventListener('selectstart', function(e){ e.preventDefault(); return false; });
    document.addEventListener('dragstart', function(e){ e.preventDefault(); return false; });
})();
