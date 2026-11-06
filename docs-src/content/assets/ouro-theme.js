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
    if(event.key==='Escape' && toggle.checked && mobile.matches){
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

// The Material search opener is a label; make it operable from the keyboard.
(function(){
  var opener=document.querySelector('[data-ouro-search-open]');
  if(!opener) return;
  opener.addEventListener('keydown',function(event){
    if(event.key==='Enter' || event.key===' '){event.preventDefault();opener.click();}
  });
})();
