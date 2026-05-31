(function(){
// QR Code popup on nav-logo hover
// Resolves image path relative to current page location
document.addEventListener('DOMContentLoaded',function(){
    var logo=document.querySelector('.nav-logo');
    if(!logo) return;
    
    // Determine image path based on page depth
    var path=window.location.pathname;
    var imgSrc;
    if(path.indexOf('/chapters/')!==-1||path.indexOf('/kg/')!==-1){
        imgSrc='../images/qrcode.jpg';
    }else{
        imgSrc='images/qrcode.jpg';
    }
    
    // Wrap logo
    var wrap=document.createElement('span');
    wrap.className='nav-logo-wrap';
    logo.parentNode.insertBefore(wrap,logo);
    wrap.appendChild(logo);
    
    // Add QR popup
    var popup=document.createElement('div');
    popup.className='qr-popup';
    popup.innerHTML='<img src="'+imgSrc+'" alt="公众号二维码"><span class="qr-label">关注公众号 · 星庐</span>';
    wrap.appendChild(popup);
});
})();
