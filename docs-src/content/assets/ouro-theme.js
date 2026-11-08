(function(){
  var root = document.documentElement;
  var button = document.querySelector('[data-ouro-theme]');
  function sync(){
    var dark = root.dataset.theme === 'dark';
    document.body.setAttribute('data-md-color-scheme', dark ? 'slate' : 'default');
    if(button) button.setAttribute('aria-pressed', String(dark));
  }
  sync();
  if(button) button.addEventListener('click',function(){
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try{ localStorage.setItem('learn-theme',root.dataset.theme); }catch(e){}
    sync();
  });
})();

(function(){
  var toggle=document.getElementById('__drawer');
  var button=document.querySelector('.ouro-drawer');
  var sidebar=document.querySelector('.md-sidebar--primary');
  var searchToggle=document.getElementById('__search');
  var search=document.querySelector('[data-md-component="search"]');
  if(!toggle || !button || !sidebar) return;
  sidebar.id='ouro-navigation';
  var mobile=window.matchMedia('(max-width: 76.2344em)');
  function syncDrawer(){
    var open=toggle.checked && mobile.matches;
    sidebar.inert=mobile.matches && !open;
    button.setAttribute('aria-expanded',String(open));
    button.setAttribute('aria-label',open ? button.dataset.labelClose : button.dataset.labelOpen);
  }
  button.addEventListener('click',function(){toggle.click();syncDrawer();});
  toggle.addEventListener('change',syncDrawer);
  mobile.addEventListener('change',syncDrawer);
  document.addEventListener('keydown',function(event){
    if(event.key==='Escape' && !event.defaultPrevented && !event.isComposing && event.keyCode!==229 && toggle.checked && mobile.matches){
      if(search && search.contains(event.target)) return;
      toggle.click();syncDrawer();button.focus();
    }
  });
  syncDrawer();
})();

// Material's search listens for keyup; pasted text and IME input may not emit
// one after the value changes. Notify it after the input/composition commits.
(function(){
  var query=document.querySelector('[data-md-component="search-query"]');
  if(!query) return;
  function notify(){query.dispatchEvent(new KeyboardEvent('keyup',{bubbles:true,key:'Unidentified'}));}
  query.addEventListener('input',function(event){if(!event.isComposing) notify();});
  query.addEventListener('compositionend',notify);
})();

// Search keyboard operation and Escape focus restoration.
(function(){
  var opener=document.querySelector('[data-ouro-search-open]');
  var search=document.querySelector('[data-md-component="search"]');
  var toggle=document.getElementById('__search');
  var query=document.querySelector('[data-md-component="search-query"]');
  var output=document.querySelector('.md-search__output');
  if(!opener || !search || !toggle || !query || !output) return;
  var mobile=window.matchMedia('(max-width: 59.984375em)');
  var hadTab=query.hasAttribute('tabindex'), originalTab=query.getAttribute('tabindex');
  var previous=null, pending=null, composing=false, tokenTimer=null, tokenSerial=0, doc=document;
  function valid(e){
    if(!e || e===document.body || e.disabled || (e.matches && e.matches(':disabled')) || !e.isConnected || search.contains(e) || !e.getClientRects().length || typeof e.focus!=='function') return false;
    for(var node=e;node && node.nodeType===1;node=node.parentElement){
      if(node.hidden || node.inert || (node.hasAttribute && (node.hasAttribute('hidden') || node.hasAttribute('inert'))) || (node.getAttribute && node.getAttribute('aria-hidden')==='true')) return false;
      if(window.getComputedStyle && window.getComputedStyle(node).visibility==='hidden') return false;
    }
    return true;
  }
  function cancel(){pending=null;if(tokenTimer!==null){clearTimeout(tokenTimer);tokenTimer=null;}}
  function begin(trigger){
    cancel();
    var token={trigger:trigger,document:doc,url:location.href,serial:++tokenSerial,expires:Date.now()+700};
    pending=token;
    tokenTimer=setTimeout(function(){if(pending===token) cancel();},700);
    requestAnimationFrame(function(){restore(token);});
  }
  function restore(token){
    if(pending!==token || token.document!==document || token.url!==location.href || Date.now()>token.expires || toggle.checked || document.activeElement!==document.body || !document.hasFocus() || document.visibilityState==='hidden') return;
    var brand=document.querySelector('.ouro-brand');
    var candidates=[token.trigger,opener,brand], tried=[];
    cancel();
    for(var i=0;i<candidates.length;i++){
      var target=candidates[i];
      if(!valid(target) || tried.indexOf(target)!==-1) continue;
      tried.push(target);
      try{target.focus({preventScroll:true});}catch(e){}
      if(document.activeElement===target) return;
      if(document.activeElement!==document.body) return;
    }
  }
  function sync(){
    if(mobile.matches && !toggle.checked) query.setAttribute('tabindex','-1');
    else if(hadTab) query.setAttribute('tabindex',originalTab);
    else query.removeAttribute('tabindex');
    output.inert=mobile.matches && !toggle.checked;
  }
  opener.addEventListener('keydown',function(event){
    if(event.key==='Enter' || event.key===' '){event.preventDefault();event.stopPropagation();opener.click();}
  });
  document.addEventListener('focusin',function(event){
    if(search.contains(event.target)){
      if(!search.contains(event.relatedTarget)){
        var brand=document.querySelector('.ouro-brand');
        previous=valid(event.relatedTarget)?event.relatedTarget:(valid(opener)?opener:(valid(brand)?brand:null));
      }
      sync();
    } else if(pending && event.target!==document.body) cancel();
  },true);
  document.addEventListener('pointerdown',cancel,true);
  document.addEventListener('pagehide',cancel,true);
  document.addEventListener('visibilitychange',function(){if(document.visibilityState==='hidden') cancel();},true);
  window.addEventListener('pagehide',cancel,true);
  window.addEventListener('blur',function(event){if(event.target===window) cancel();},true);
  window.addEventListener('hashchange',cancel,true);
  document.addEventListener('compositionstart',function(){composing=true;cancel();},true);
  document.addEventListener('compositionend',function(){composing=false;},true);
  document.addEventListener('keydown',function(event){
    if(pending){cancel();return;}
    if(event.key!=='Escape') return;
    if(composing || event.isComposing || event.keyCode===229 || !toggle.checked || !search.contains(event.target)) return;
    begin(previous);
  },true);
  document.addEventListener('focusout',function(event){
    if(!search.contains(event.target)) return;
    requestAnimationFrame(sync);
    if(event.relatedTarget && event.relatedTarget!==document.body){cancel();return;}
    if(pending){var token=pending;requestAnimationFrame(function(){restore(token);});}
  },true);
  toggle.addEventListener('change',function(){if(toggle.checked) cancel();else if(pending){var token=pending;requestAnimationFrame(function(){restore(token);});}sync();});
  mobile.addEventListener('change',sync);
  sync();
})();

// Annotate only reviewed result URLs. Unknown URLs or a failed map load are left alone.
(function(){
  var list=document.querySelector('[data-md-component="search-result"]');
  if(!list || !window.MutationObserver) return;
  var names={
    'ko':{'ko':'한국어','en':'영어','zh-Hans':'중국어'},
    'en':{'ko':'Korean','en':'English','zh-Hans':'Chinese'},
    'zh-Hans':{'ko':'韩语','en':'英语','zh-Hans':'中文'}
  };
  var ui=document.documentElement.lang;
  if(!Object.prototype.hasOwnProperty.call(names,ui)) return;
  var routes=null;
  function update(){
    if(!routes) return;
    list.querySelectorAll('a.md-search-result__link').forEach(function(link){
      var url; try{url=new URL(link.getAttribute('href'),location.href);}catch(e){return;}
      var language=url.origin===location.origin ? routes[url.pathname] : null;
      var article=link.querySelector('.md-search-result__article');
      var heading=article && article.querySelector('h1,h2');
      var terms=article && article.querySelector('.md-search-result__terms');
      if(!heading) return;
      var badge=heading.querySelector('[data-ouro-result-language]');
      if(!Object.prototype.hasOwnProperty.call(names[ui],language)){
        if(badge) badge.remove();
        if(article.hasAttribute('data-ouro-result-language-applied')){article.removeAttribute('lang');article.removeAttribute('data-ouro-result-language-applied');}
        if(terms && terms.hasAttribute('data-ouro-ui-language-applied')){terms.removeAttribute('lang');terms.removeAttribute('data-ouro-ui-language-applied');}
        return;
      }
      article.setAttribute('lang',language);
      article.setAttribute('data-ouro-result-language-applied','');
      // Material 9.7.1 inserts the translated missing-term message inside the article.
      if(terms){terms.setAttribute('lang',ui);terms.setAttribute('data-ouro-ui-language-applied','');}
      if(!badge){badge=document.createElement('span');badge.setAttribute('data-ouro-result-language','');heading.appendChild(badge);}
      if(badge.getAttribute('lang')!==ui) badge.setAttribute('lang',ui);
      var label=' · '+names[ui][language];
      if(badge.textContent!==label) badge.textContent=label;
    });
  }
  new MutationObserver(update).observe(list,{childList:true,subtree:true,attributes:true,attributeFilter:['href']});
  fetch('/docs/search/languages.json').then(function(response){if(!response.ok) throw Error('language map');return response.json();}).then(function(data){routes=data;update();}).catch(function(){});
})();
