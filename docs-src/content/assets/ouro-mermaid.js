(function(){
  var blocks = document.querySelectorAll('pre.mermaid');
  if(!blocks.length) return;
  // Material's default loader can silently erase the source if its CDN module
  // is unavailable. Keep the original pre/code until local rendering succeeds.
  blocks.forEach(function(block){ block.classList.remove('mermaid'); block.classList.add('ouro-mermaid-source'); });
  if(!window.mermaid || typeof window.mermaid.render !== 'function') return;
  window.mermaid.initialize({startOnLoad:false,securityLevel:'strict',theme:'neutral',fontFamily:'Paperlogy, system-ui, sans-serif'});
  blocks.forEach(async function(block,index){
    var code=block.querySelector('code'); var source=code ? code.textContent : block.textContent;
    try {
      var result=await window.mermaid.render('ouro-local-diagram-'+index,source);
      var wrapper=document.createElement('div'); wrapper.className='ouro-diagram'; wrapper.setAttribute('role','img');
      wrapper.setAttribute('aria-label','다이어그램 '+(index+1)); wrapper.innerHTML=result.svg;
      var details=document.createElement('details');
      var summary=document.createElement('summary');
      summary.textContent='다이어그램 원문 보기';
      details.appendChild(summary);
      block.replaceWith(wrapper,details);
      details.appendChild(block);
    } catch(e) { console.warn('Diagram rendering unavailable; source retained.'); }
  });
})();
