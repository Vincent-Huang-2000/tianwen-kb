document.addEventListener('DOMContentLoaded',function(){
  var hash=window.location.hash;
  if(!hash)return;
  var m=hash.match(/^#find=(.+)/);
  if(!m)return;
  var text=decodeURIComponent(m[1]);
  var body=document.querySelector('.chapter-body');
  if(!body)return;

  var fullText=body.textContent;
  var idx=fullText.indexOf(text);
  if(idx<0)return;

  var walker=document.createTreeWalker(body,NodeFilter.SHOW_TEXT,null,false);
  var pos=0,node;
  while(node=walker.nextNode()){
    var len=node.textContent.length;
    if(pos+len>idx){
      var offset=idx-pos;
      var range=document.createRange();
      range.setStart(node,offset);
      var remaining=text.length;
      var endNode=node,endOffset=offset;
      while(remaining>0){
        var avail=endNode.textContent.length-endOffset;
        var take=Math.min(avail,remaining);
        remaining-=take;endOffset+=take;
        if(remaining>0){endNode=walker.nextNode();if(!endNode)break;endOffset=0;}
      }
      range.setEnd(endNode,endOffset);

      // Scroll first, then highlight in next frame to avoid visual flash
      var rect=range.getClientRects()[0];
      if(rect){
        var targetTop=window.scrollY+rect.top-120;
        window.scrollTo({top:targetTop,behavior:'instant'});
        // Highlight after scroll settles
        requestAnimationFrame(function(){
          try{
            var span=document.createElement('span');
            span.style.background='rgba(201,169,110,0.35)';
            span.style.borderRadius='3px';
            span.style.padding='2px 0';
            span.id='kg-highlight';
            range.surroundContents(span);
          }catch(e){}
        });
      }
      break;
    }
    pos+=len;
  }
});
