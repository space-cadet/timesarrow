/* KaTeX auto-render initializer */
/* Runs after both katex.min.js and auto-render.min.js are loaded */

(function () {
  'use strict';

  function renderMath() {
    if (typeof renderMathInElement === 'undefined') {
      console.warn('[katex-loader] renderMathInElement not available yet — retrying');
      setTimeout(renderMath, 100);
      return;
    }

    console.info('[katex-loader] Starting KaTeX render pass');

    renderMathInElement(document.body, {
      delimiters: [
        { left: '$$', right: '$$', display: true  },
        { left: '\\[', right: '\\]', display: true  },
        { left: '$',  right: '$',  display: false },
        { left: '\\(', right: '\\)', display: false }
      ],
      throwOnError: false,
      errorCallback: function (msg, err) {
        console.warn('[katex-loader] Render error:', msg, err);
      }
    });

    console.info('[katex-loader] KaTeX render pass complete');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderMath);
  } else {
    renderMath();
  }
})();
