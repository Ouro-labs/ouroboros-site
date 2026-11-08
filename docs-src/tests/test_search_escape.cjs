const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../content/assets/ouro-theme.js'),'utf8');
const code=source.slice(source.indexOf('// Search keyboard operation'),source.indexOf('// Annotate only reviewed result URLs.'));
function setup(){
 let handlers={},callbacks=[], mediaHandlers={},openerHandlers={},toggleHandlers={};
 let body={},input={attrs:{},isConnected:true,getClientRects:()=>[1],hasAttribute(k){return k in this.attrs},getAttribute(k){return this.attrs[k]??null},setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]}}, result={};
 let search={contains:x=>x===input||x===result},toggle={checked:false,addEventListener:(n,f)=>toggleHandlers[n]=f},output={},media={matches:true,addEventListener:(n,f)=>mediaHandlers[n]=f};
 let document={body,activeElement:body,querySelector:s=>({'[data-ouro-search-open]':opener,'[data-md-component="search"]':search,'[data-md-component="search-query"]':input,'.md-search__output':output,'.ouro-brand':brand}[s]),getElementById:()=>toggle,addEventListener:(n,f)=>handlers[n]=f};
 let opener={isConnected:true,getClientRects:()=>[1],focus(){document.activeElement=this},click(){toggle.checked=!toggle.checked;toggleHandlers.change()},addEventListener:(n,f)=>openerHandlers[n]=f},brand={isConnected:true,getClientRects:()=>[1],focus(){document.activeElement=this}};
 vm.runInNewContext(code,{document,window:{matchMedia:()=>media},requestAnimationFrame:f=>callbacks.push(f)});
 return {handlers,callbacks,mediaHandlers,openerHandlers,toggleHandlers,document,body,input,result,search,toggle,output,media,opener,brand};
}
function open(x){let prevented=false,stopped=false;x.openerHandlers.keydown({key:'Enter',preventDefault(){prevented=true},stopPropagation(){stopped=true}});assert(prevented&&stopped);x.document.activeElement=x.input;x.handlers.focusin({target:x.input,relatedTarget:x.opener});assert.equal(x.toggle.checked,true);assert.equal(x.output.inert,false);}
function escape(x){x.document.activeElement=x.result;x.handlers.keydown({key:'Escape',target:x.result});x.toggle.checked=false;x.document.activeElement=x.body;x.handlers.focusout({target:x.result,relatedTarget:null});while(x.callbacks.length)x.callbacks.shift()();}
{let x=setup();assert.equal(x.input.getAttribute('tabindex'),'-1');assert.equal(x.output.inert,true);open(x);escape(x);assert.equal(x.document.activeElement,x.opener);assert.equal(x.output.inert,true);assert.equal(x.input.getAttribute('tabindex'),'-1');}
{let x=setup();open(x);x.document.activeElement=x.result;x.handlers.keydown({key:'Escape',target:x.result});x.toggle.checked=false;x.document.activeElement=x.body;x.handlers.focusout({target:x.result,relatedTarget:null});x.toggle.checked=true;while(x.callbacks.length)x.callbacks.shift()();assert.notEqual(x.document.activeElement,x.opener);}
{let x=setup();open(x);x.handlers.compositionstart();x.handlers.keydown({key:'Escape',target:x.input,isComposing:true});x.toggle.checked=false;x.document.activeElement=x.body;x.handlers.focusout({target:x.input,relatedTarget:null});while(x.callbacks.length)x.callbacks.shift()();assert.notEqual(x.document.activeElement,x.opener);}
{let x=setup();x.media.matches=false;x.mediaHandlers.change();assert.equal(x.input.hasAttribute('tabindex'),false);assert.equal(x.output.inert,false);x.media.matches=true;x.mediaHandlers.change();assert.equal(x.output.inert,true);}
console.log('search Escape, mobile focus containment, reopen, composition and resize passed');
