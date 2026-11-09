// Separate exact-query shortcuts; Material search results and ranking are untouched.
(function () {
  var query = document.querySelector('[data-md-component="search-query"]');
  var results = document.querySelector('[data-md-component="search-result"]');
  if (!query || !results || !results.parentNode) return;
  var locale = document.documentElement.lang;
  var options = {
    ko: {query: '설치', href: '/docs/quickstart/#1', text: '빠른 시작: 설치 경로 고르기'},
    en: {query: 'seed', href: '/docs/en/quickstart/#shared-seed-review', text: 'Quickstart: review the generated Seed'}
  };
  if (!Object.prototype.hasOwnProperty.call(options, locale)) return;
  var option = options[locale];
  var box = document.createElement('p');
  box.hidden = true;
  box.style.padding = '0.6rem 0.8rem';
  var link = document.createElement('a');
  link.href = option.href;
  link.textContent = option.text;
  link.lang = locale;
  box.appendChild(link);
  results.parentNode.insertBefore(box, results);
  var composing = false;
  function update() {
    box.hidden = composing || query.value.trim().toLowerCase() !== option.query;
  }
  query.addEventListener('compositionstart', function () { composing = true; update(); });
  query.addEventListener('compositionend', function () { composing = false; update(); });
  query.addEventListener('input', update);
  if (query.form) query.form.addEventListener('reset', function () { box.hidden = true; });
  update();
})();
