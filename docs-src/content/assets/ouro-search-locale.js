// Preserve Material matching, grouping and keyboard handling; only tell its
// search worker which reviewed locale should lead the existing result list.
(function () {
  var NativeWorker = window.Worker;
  if (!NativeWorker) return;
  window.Worker = function (url, options) {
    var resolved = new URL(url, location.href);
    var locale = document.documentElement.lang;
    if (resolved.origin === location.origin &&
        /\/workers\/search\.[a-z0-9]+\.min\.js$/.test(resolved.pathname) &&
        ['ko', 'en', 'zh-Hans'].indexOf(locale) !== -1) {
      resolved.searchParams.set('ouro_locale', locale);
      return new NativeWorker(resolved.href, options);
    }
    return new NativeWorker(url, options);
  };
  window.Worker.prototype = NativeWorker.prototype;
})();
