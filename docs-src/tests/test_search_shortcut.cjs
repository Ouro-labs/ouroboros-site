const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const code = fs.readFileSync(path.join(__dirname, '../content/assets/ouro-search-shortcut.js'), 'utf8');
function run(lang) {
  const handlers = {}, formHandlers = {}, inserted = [];
  const query = {value: '', addEventListener:(k, f)=>handlers[k]=f, form:{addEventListener:(k,f)=>formHandlers[k]=f}};
  const parent = {insertBefore:(node, before)=>{assert.equal(before,results); inserted.push(node)}};
  const results = {parentNode: parent};
  const doc = {documentElement:{lang},querySelector:s=>s.includes('search-query')?query:results,
    createElement:()=>({style:{},appendChild(c){this.child=c;}})};
  vm.runInNewContext(code, {document:doc, Object});
  return {query,handlers,formHandlers,inserted};
}
for (const [lang,term,href] of [['ko','설치','/docs/quickstart/#1'],['en','Seed','/docs/en/quickstart/#shared-seed-review']]) {
  const x=run(lang), box=x.inserted[0];assert.equal(box.hidden,true);x.query.value=term;x.handlers.input();
  assert.equal(box.hidden,false);assert.equal(box.child.href,href);assert.equal(box.child.lang,lang);
  x.handlers.compositionstart();assert.equal(box.hidden,true);x.handlers.compositionend();assert.equal(box.hidden,false);
  x.query.value='other';x.handlers.input();assert.equal(box.hidden,true);x.query.value=term;x.handlers.input();x.formHandlers.reset();assert.equal(box.hidden,true);
}
assert.equal(run('zh-Hans').inserted.length,0);assert.equal(run('fr').inserted.length,0);
console.log('search shortcuts: exact query, IME, reset, locale and fallback passed');
