const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'content/assets/ouro-theme.js'), 'utf8');
const marker = '// Annotate only reviewed result URLs.';
assert(source.includes(marker));
const code = source.slice(source.indexOf(marker));
class Element {
  constructor(){ this.attrs={}; this.textContent=''; this.child=null; }
  setAttribute(k,v){this.attrs[k]=String(v)} getAttribute(k){return Object.hasOwn(this.attrs,k)?this.attrs[k]:null}
  hasAttribute(k){return Object.hasOwn(this.attrs,k)} removeAttribute(k){delete this.attrs[k]}
  appendChild(child){this.child=child;child.parent=this} remove(){if(this.parent)this.parent.child=null}
  querySelector(selector){return selector==='[data-ouro-result-language]'?this.child:null}
}
function result(href){
  const heading=new Element(), article=new Element(), terms=new Element();
  article.querySelector=s=>s==='h1,h2'?heading:s==='.md-search-result__terms'?terms:null;
  const link=new Element();link.setAttribute('href',href);link.querySelector=s=>s==='.md-search-result__article'?article:null;
  return {link,article,heading,terms};
}
async function run(fail, ui='zh-Hans'){
  let callback, nodes=[];const list={querySelectorAll:()=>nodes.map(x=>x.link)};
  class Observer{constructor(cb){callback=cb} observe(node,opts){assert.equal(node,list);assert.deepEqual(Array.from(opts.attributeFilter),['href']);}}
  const context={document:{documentElement:{lang:ui},querySelector:()=>list,createElement:()=>new Element()},window:{MutationObserver:Observer},MutationObserver:Observer,
    location:{href:'https://ouroboros.page/docs/zh/quickstart/',origin:'https://ouroboros.page'},URL,
    fetch:()=>fail?Promise.reject(Error('offline')):Promise.resolve({ok:true,json:()=>Promise.resolve({'/docs/seed-guide/':'ko','/docs/en/quickstart/':'en','/docs/zh/troubleshooting/':'zh-Hans'})})};
  vm.runInNewContext(code,context);await new Promise(resolve=>setImmediate(resolve));
  if(fail){const unknown=result('/docs/seed-guide/');nodes=[unknown];callback();assert.equal(unknown.heading.child,null);return;}
  const ko=result('/docs/seed-guide/#x'), en=result('/docs/en/quickstart/'), zh=result('/docs/zh/troubleshooting/#recovery'), unknown=result('/docs/unreviewed/');nodes=[ko,en,zh,unknown];callback();
  const labels={'zh-Hans':[' · 韩语',' · 英语',' · 中文',null],en:[' · Korean',' · English',' · Chinese',null],ko:[' · 한국어',' · 영어',' · 중국어',null]};
  assert.deepEqual(nodes.map(x=>x.heading.child?.textContent||null),labels[ui]);
  assert.deepEqual(nodes.slice(0,3).map(x=>x.article.getAttribute('lang')),['ko','en','zh-Hans']);
  assert.deepEqual(nodes.slice(0,3).map(x=>x.terms.getAttribute('lang')),[ui,ui,ui]);
  const original=ko.heading.child;callback();assert.equal(ko.heading.child,original);
  ko.link.setAttribute('href','/docs/unreviewed/');callback();assert.equal(ko.heading.child,null);assert.equal(ko.article.hasAttribute('lang'),false);assert.equal(ko.terms.hasAttribute('lang'),false);
  nodes=[];callback();const next=result('/docs/en/quickstart/');nodes=[next];callback();assert.equal(next.heading.child.textContent,labels[ui][1]);assert.equal(next.heading.child.getAttribute('lang'),ui);
}
Promise.all([run(false,'zh-Hans'),run(false,'en'),run(false,'ko'),run(true)]).then(()=>console.log('search language dynamic tests passed')).catch(e=>{console.error(e);process.exitCode=1});
