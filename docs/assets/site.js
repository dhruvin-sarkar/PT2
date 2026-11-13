/*
 * Website behaviour (classic script, no modules, no framework). Copied to docs/assets/site.js.
 * Every page works without it: questions and full solutions are in the HTML; this adds
 *   - theme toggle (day sketchbook / night study chalkboard), remembered in localStorage
 *   - progress: per question "got" / "revisit" in localStorage key "pt2-progress-v1"
 *       { "ch01/school": { "7": "got", "9": "revisit" } }
 *     shown on the home cards, the chapter sets and question list, and the walkthrough picker
 *   - chapter page: question filters (set, level, type, status)
 *   - walkthrough: one question at a time (#q7 deep links), step-by-step reveal, hint, show all,
 *     show answer, tap-to-check options, keyboard (Space / Right arrow, A, H, N, P)
 * Storage can be missing or throw (private mode, blocked site data): everything still works for the visit.
 */
(function () {
  'use strict';
  var doc = document;
  var root = doc.documentElement;
  var KEY = 'pt2-progress-v1';

  /* ---------------------------------------------------------- storage */
  var mem = {};
  function readAll() {
    try {
      var raw = window.localStorage.getItem(KEY);
      var v = raw ? JSON.parse(raw) : {};
      return v && typeof v === 'object' ? v : {};
    } catch (e) {
      return mem;
    }
  }
  function writeAll(v) {
    mem = v;
    try {
      window.localStorage.setItem(KEY, JSON.stringify(v));
    } catch (e) {
      /* storage unavailable: keep it in memory for this visit */
    }
  }
  function getState(key, n) {
    var all = readAll();
    return (all[key] && all[key][n]) || '';
  }
  function setState(key, n, state) {
    var all = readAll();
    var set = all[key] || {};
    if (state) set[n] = state;
    else delete set[n];
    all[key] = set;
    writeAll(all);
  }
  function countSet(key) {
    var s = readAll()[key] || {};
    var got = 0;
    var rev = 0;
    for (var k in s) {
      if (s[k] === 'got') got++;
      else if (s[k] === 'revisit') rev++;
    }
    return { got: got, rev: rev };
  }

  function $(sel, el) {
    return (el || doc).querySelector(sel);
  }
  function $$(sel, el) {
    return Array.prototype.slice.call((el || doc).querySelectorAll(sel));
  }
  function plural(n, one, many) {
    return n + ' ' + (n === 1 ? one : many || one + 's');
  }
  function fillBar(bar, got, rev, total) {
    if (!bar || !total) return;
    bar.style.setProperty('--got', Math.min(100, (got / total) * 100).toFixed(2) + '%');
    bar.style.setProperty('--rev', Math.min(100, (rev / total) * 100).toFixed(2) + '%');
  }
  function progressText(got, rev, total) {
    if (!got && !rev) return 'Not started';
    var t = got + ' of ' + total + ' got it';
    if (rev) t += ', ' + rev + ' to revisit';
    return t;
  }

  /* ---------------------------------------------------------- theme */
  function initTheme() {
    var btn = $('.theme-toggle');
    if (!btn) return;
    function current() {
      return root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    }
    function sync() {
      var dark = current() === 'dark';
      btn.setAttribute('aria-pressed', dark ? 'true' : 'false');
      btn.title = dark ? 'Day theme' : 'Night study theme';
      var label = $('.vh', btn);
      if (label) label.textContent = 'Night study theme';
    }
    sync();
    btn.addEventListener('click', function () {
      var next = current() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try {
        window.localStorage.setItem('pt2-theme', next);
      } catch (e) {
        /* ignore */
      }
      sync();
    });
    if (window.matchMedia) {
      var mq = window.matchMedia('(prefers-color-scheme: dark)');
      var onChange = function (e) {
        var stored = null;
        try {
          stored = window.localStorage.getItem('pt2-theme');
        } catch (err) {
          /* ignore */
        }
        if (!stored) {
          root.setAttribute('data-theme', e.matches ? 'dark' : 'light');
          sync();
        }
      };
      if (mq.addEventListener) mq.addEventListener('change', onChange);
    }
  }

  /* ---------------------------------------------------------- home */
  function initHome() {
    var totalGot = 0;
    var totalRev = 0;
    var total = 0;
    $$('.card[data-sets]').forEach(function (card) {
      var got = 0;
      var rev = 0;
      var n = 0;
      card.getAttribute('data-sets').split(',').forEach(function (pair) {
        var i = pair.lastIndexOf(':');
        var c = countSet(pair.slice(0, i));
        got += c.got;
        rev += c.rev;
        n += Number(pair.slice(i + 1)) || 0;
      });
      fillBar($('.pbar', card), got, rev, n);
      var t = $('.card-progress-text', card);
      if (t && (got || rev)) t.textContent = got + ' of ' + n + ' got it';
      totalGot += got;
      totalRev += rev;
      total += n;
    });
    var note = $('.sticky');
    if (!note) return;
    fillBar($('.pbar', note), totalGot, totalRev, total);
    var text = $('.sticky-text', note);
    if (text && (totalGot || totalRev)) {
      var s = 'You have ticked off ' + plural(totalGot, 'question') + ' of ' + total + '.';
      if (totalRev) s += ' ' + plural(totalRev, 'question') + ' marked to revisit.';
      text.textContent = s;
    }
  }

  /* ---------------------------------------------------------- chapter */
  function initChapter() {
    $$('.set[data-key]').forEach(function (row) {
      var c = countSet(row.getAttribute('data-key'));
      var total = Number(row.getAttribute('data-total')) || 0;
      fillBar($('.pbar', row), c.got, c.rev, total);
      var t = $('.set-progress-text', row);
      if (t) t.textContent = progressText(c.got, c.rev, total);
    });

    var sets = $$('.ql-set');
    var rows = $$('.ql-row');
    rows.forEach(function (r) {
      var key = r.closest('.ql-set').getAttribute('data-key');
      var st = getState(key, r.getAttribute('data-n'));
      r.setAttribute('data-status', st || 'todo');
      if (st === 'got') r.classList.add('is-got');
      if (st === 'revisit') r.classList.add('is-revisit');
      var label = $('.ql-state-text', r);
      if (label) label.textContent = st === 'got' ? ' (got it)' : st === 'revisit' ? ' (to revisit)' : '';
    });

    var filters = { set: sets.length ? sets[0].getAttribute('data-set') : '', level: '', type: '', status: '' };
    var hasSetChips = !!$('.chip[data-group="set"]');
    if (!hasSetChips) filters.set = '';
    var countEl = $('.ql-count');
    var empty = $('.ql-empty');
    var questions = $('.questions');
    if (questions && hasSetChips) questions.classList.add('filters-sets');

    function apply() {
      var shown = 0;
      var total = 0;
      sets.forEach(function (s) {
        var setOk = !filters.set || s.getAttribute('data-set') === filters.set;
        s.hidden = !setOk;
        if (!setOk) return;
        $$('.ql-level', s).forEach(function (lv) {
          var lvShown = 0;
          $$('.ql-row', lv).forEach(function (r) {
            total++;
            var ok =
              (!filters.level || r.getAttribute('data-level') === filters.level) &&
              (!filters.type || r.getAttribute('data-type') === filters.type) &&
              (!filters.status || r.getAttribute('data-status') === filters.status);
            r.hidden = !ok;
            if (ok) lvShown++;
          });
          lv.hidden = !lvShown;
          shown += lvShown;
        });
      });
      if (countEl) countEl.textContent = shown === total ? 'Showing all ' + plural(total, 'question') : 'Showing ' + shown + ' of ' + plural(total, 'question');
      if (empty) empty.hidden = shown !== 0;
    }

    $$('.chip').forEach(function (chip) {
      chip.addEventListener('click', function () {
        var g = chip.getAttribute('data-group');
        filters[g] = chip.getAttribute('data-value');
        $$('.chip[data-group="' + g + '"]').forEach(function (c) {
          c.setAttribute('aria-pressed', c === chip ? 'true' : 'false');
        });
        apply();
      });
    });
    apply();
    if (window.PT && window.PT.fitMath) window.PT.fitMath(doc.querySelector('.questions'));
  }

  /* ---------------------------------------------------------- walkthrough */
  function parseMarks(text) {
    var t = String(text || '').replace(/\s/g, '');
    if (!t) return 0;
    var half = t.indexOf('½') >= 0;
    var whole = parseFloat(t.replace('½', '')) || 0;
    return whole + (half ? 0.5 : 0);
  }
  function fmtMarks(n) {
    var w = Math.floor(n);
    var h = Math.abs(n - w - 0.5) < 1e-9;
    if (h) return w ? w + '½' : '½';
    return String(n);
  }
  function marksLabel(n) {
    return fmtMarks(n) + (n === 1 || n === 0.5 ? ' mark' : ' marks');
  }

  function initWalk() {
    var wt = $('.wt');
    if (!wt) return;
    var key = wt.getAttribute('data-key');
    var sections = $$('.wt-q', wt);
    if (!sections.length) return;
    var byN = {};
    sections.forEach(function (s) {
      byN[s.getAttribute('data-n')] = s;
    });
    var order = sections.map(function (s) {
      return s.getAttribute('data-n');
    });
    var pickerWrap = $('.pk-wrap');
    var wide = window.matchMedia ? window.matchMedia('(min-width: 921px)') : { matches: true };
    if (pickerWrap && !wide.matches) pickerWrap.open = false;
    var current = null;
    var models = {};

    function fit(el) {
      if (!el || !window.PT || !window.PT.fitMath) return;
      window.PT.fitMath(el, { lastResort: 'scroll' });
      // a block that scrolls sideways can be reached and scrolled with the keyboard
      $$('.math-fit', el).forEach(function (b) {
        if (b.getAttribute('data-fit') === 'scroll') {
          b.setAttribute('tabindex', '0');
          b.setAttribute('role', 'group');
          b.setAttribute('aria-label', 'Wide maths, scroll sideways');
        } else if (b.hasAttribute('tabindex')) {
          b.removeAttribute('tabindex');
          b.removeAttribute('role');
          b.removeAttribute('aria-label');
          b.classList.remove('is-scrolled-end');
        }
      });
    }
    doc.addEventListener(
      'scroll',
      function (e) {
        var b = e.target;
        if (b && b.classList && b.classList.contains('math-fit')) b.classList.toggle('is-scrolled-end', b.scrollLeft + b.clientWidth >= b.scrollWidth - 2);
      },
      true,
    );

    /* build the reveal sequence of one question: groups of elements shown together */
    function model(sec) {
      var n = sec.getAttribute('data-n');
      if (models[n]) return models[n];
      var sol = $('.sol', sec);
      var groups = [];
      var pending = [];
      var items = sol ? $$('.sol-fig, .sol-or, .sol-part-head, .step, .answer, .watch', sol) : [];
      items.forEach(function (el) {
        if (el.classList.contains('step')) {
          groups.push({ els: pending.concat([el]), marks: parseMarks(($('.step-mark', el) || {}).textContent) });
          pending = [];
        } else if (el.classList.contains('answer') || el.classList.contains('watch')) {
          if (groups.length) groups[groups.length - 1].els.push(el);
          else pending.push(el);
        } else pending.push(el);
      });
      if (pending.length) {
        if (groups.length) groups[groups.length - 1].els = groups[groups.length - 1].els.concat(pending);
        else groups.push({ els: pending, marks: 0 });
      }
      var m = {
        sec: sec,
        sol: sol,
        groups: groups,
        shown: 0,
        total: Number(sec.getAttribute('data-marks')) || 0,
        steps: $$('.step', sol || sec).length,
      };
      models[n] = m;
      return m;
    }

    function showEl(el, animate) {
      if (el.classList.contains('is-shown')) return;
      el.classList.add('is-shown');
      if (animate) {
        // the row fades in, then the red tick is drawn and the mark written: keep the class until all three end
        el.classList.add('is-new');
        setTimeout(function () {
          el.classList.remove('is-new');
        }, 1100);
      }
      var p = el.parentElement;
      while (p && !p.classList.contains('sol')) {
        if (p.classList.contains('steps') || p.classList.contains('sol-part')) p.classList.add('is-shown');
        p = p.parentElement;
      }
      fit(el);
    }

    function update(m) {
      var sec = m.sec;
      var marks = 0;
      var stepsShown = 0;
      $$('.step.is-shown', m.sol || sec).forEach(function (s) {
        stepsShown++;
        marks += parseMarks(($('.step-mark', s) || {}).textContent);
      });
      var tSteps = $('.wt-tally-steps', sec);
      var tMarks = $('.wt-tally-marks', sec);
      if (tSteps) tSteps.textContent = 'Step ' + stepsShown + ' of ' + m.steps;
      if (tMarks) tMarks.textContent = fmtMarks(Math.round(marks * 2) / 2) + ' of ' + marksLabel(m.total);
      var next = $('[data-act="next"]', sec);
      var done = m.shown >= m.groups.length;
      if (next) {
        next.disabled = done;
        var lbl = $('.btn-label', next);
        if (lbl) lbl.textContent = done ? 'All steps shown' : m.shown ? 'Next step' : 'First step';
      }
      var all = $('[data-act="all"]', sec);
      if (all) all.disabled = done;
      var ans = $('[data-act="answer"]', sec);
      if (ans) ans.disabled = !$$('.answer:not(.is-shown)', m.sol || sec).length;
      if (m.shown || $('.is-shown', m.sol || sec)) sec.classList.add('has-started');
    }

    /* the controls bar sticks to the bottom of the screen, so a step revealed below it would be out of sight:
       scroll just enough to bring the new rows above the bar (never past the top of the first one) */
    var calm = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
    function keepInView(els, sec) {
      var top = Infinity;
      var bottom = -Infinity;
      els.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (!r.height) return;
        top = Math.min(top, r.top);
        bottom = Math.max(bottom, r.bottom);
      });
      if (bottom === -Infinity) return;
      var bar = $('.wt-controls', sec);
      var limit = window.innerHeight - (bar && bar.offsetHeight ? bar.offsetHeight : 0) - 12;
      var delta = Math.min(bottom - limit, top - 12);
      if (delta > 0) window.scrollBy({ top: delta, left: 0, behavior: calm.matches ? 'auto' : 'smooth' });
    }

    function revealNext(m, animate) {
      if (m.shown >= m.groups.length) return false;
      var els = m.groups[m.shown].els;
      els.forEach(function (el) {
        showEl(el, animate);
      });
      m.shown++;
      update(m);
      if (animate) keepInView(els, m.sec);
      return true;
    }
    function revealAll(m) {
      while (m.shown < m.groups.length) revealNext(m, false);
    }
    function revealAnswer(m) {
      var answers = $$('.answer', m.sol || m.sec);
      answers.forEach(function (a) {
        showEl(a, true);
      });
      update(m);
      keepInView(answers, m.sec);
    }
    function toggleHint(m, btn) {
      var c = $('.sol-concept', m.sol || m.sec);
      if (!c) return;
      var on = !c.classList.contains('is-shown');
      if (on) showEl(c, true);
      else c.classList.remove('is-shown');
      if (btn) btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    }

    function syncPicker() {
      $$('.pk').forEach(function (a) {
        var n = a.getAttribute('data-n');
        var st = getState(key, n);
        a.classList.toggle('is-got', st === 'got');
        a.classList.toggle('is-revisit', st === 'revisit');
        var lab = $('.pk-state', a);
        if (lab) lab.textContent = st === 'got' ? ' (got it)' : st === 'revisit' ? ' (to revisit)' : '';
        if (n === current) a.setAttribute('aria-current', 'true');
        else a.removeAttribute('aria-current');
      });
      var cur = $('.pk-cur');
      if (cur && current) cur.textContent = current;
    }

    function syncRate(sec) {
      var st = getState(key, sec.getAttribute('data-n'));
      $$('[data-rate]', sec).forEach(function (b) {
        b.setAttribute('aria-pressed', b.getAttribute('data-rate') === st ? 'true' : 'false');
      });
    }

    function show(n, focus) {
      if (!byN[n]) n = order[0];
      if (n === current) return;
      current = n;
      sections.forEach(function (s) {
        s.hidden = s.getAttribute('data-n') !== n;
      });
      var sec = byN[n];
      var m = model(sec);
      syncRate(sec);
      syncPicker();
      fit($('.slip', sec));
      $$('.is-shown', m.sol || sec).forEach(fit);
      update(m);
      if (pickerWrap && !wide.matches) pickerWrap.open = false;
      if (focus) {
        sec.focus({ preventScroll: true });
        var top = $('.wt-head') || sec;
        var y = top.getBoundingClientRect().top + window.pageYOffset - 8;
        if (window.pageYOffset > y) window.scrollTo(0, y);
      }
    }

    function fromHash() {
      var h = (location.hash || '').replace(/^#q/, '');
      return byN[h] ? h : order[0];
    }

    function go(delta) {
      var i = order.indexOf(current) + delta;
      if (i < 0 || i >= order.length) return;
      location.hash = '#q' + order[i];
    }

    /* options: tap to check before the steps */
    $$('.q-options[data-correct]', wt).forEach(function (list) {
      var correct = list.getAttribute('data-correct');
      var sec = list.closest('.wt-q');
      var fb = $('.opt-feedback', sec);
      $$('.opt-btn', list).forEach(function (b) {
        b.addEventListener('click', function () {
          var li = b.closest('.q-opt');
          var right = b.getAttribute('data-i') === correct;
          var letter = ($('.q-opt-letter', b) || {}).textContent || '';
          letter = letter.replace(/\s/g, '');
          if (right) {
            $$('.q-opt', list).forEach(function (o) {
              o.classList.remove('is-wrong');
            });
            li.classList.add('is-right');
          } else li.classList.add('is-wrong');
          b.setAttribute('aria-pressed', 'true');
          if (fb) {
            fb.classList.toggle('is-right', right);
            fb.textContent = right ? letter + ' is right. Now check the reasoning in the steps.' : letter + ' is not right. Try another option, or take a hint.';
          }
        });
      });
    });

    /* buttons */
    wt.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b || !wt.contains(b)) return;
      var sec = b.closest('.wt-q');
      if (!sec) return;
      var m = model(sec);
      var act = b.getAttribute('data-act');
      if (act === 'next') revealNext(m, true);
      else if (act === 'all') revealAll(m);
      else if (act === 'answer') revealAnswer(m);
      else if (act === 'hint') toggleHint(m, b);
      var rate = b.getAttribute('data-rate');
      if (rate) {
        var n = sec.getAttribute('data-n');
        setState(key, n, getState(key, n) === rate ? '' : rate);
        syncRate(sec);
        syncPicker();
      }
    });

    /* keyboard */
    doc.addEventListener('keydown', function (e) {
      if (e.altKey || e.ctrlKey || e.metaKey) return;
      var t = e.target;
      var tag = t && t.tagName ? t.tagName.toLowerCase() : '';
      if (tag === 'input' || tag === 'textarea' || tag === 'select' || (t && t.isContentEditable)) return;
      var sec = byN[current];
      if (!sec) return;
      var m = model(sec);
      var k = e.key;
      if (k === 'ArrowRight' || (k === ' ' && tag !== 'button' && tag !== 'summary' && tag !== 'a')) {
        e.preventDefault();
        revealNext(m, true);
        var nb = $('[data-act="next"]', sec);
        if (nb && nb.disabled && t === nb) sec.focus({ preventScroll: true });
      } else if (k === 'a' || k === 'A') {
        revealAll(m);
      } else if (k === 'h' || k === 'H') {
        toggleHint(m, $('[data-act="hint"]', sec));
      } else if (k === 'n' || k === 'N') {
        go(1);
      } else if (k === 'p' || k === 'P') {
        go(-1);
      }
    });

    window.addEventListener('hashchange', function () {
      show(fromHash(), true);
    });
    var rt = 0;
    window.addEventListener('resize', function () {
      clearTimeout(rt);
      rt = setTimeout(function () {
        var sec = byN[current];
        if (sec) fit(sec);
      }, 150);
    });
    if (wide.addEventListener) {
      wide.addEventListener('change', function (e) {
        if (pickerWrap) pickerWrap.open = e.matches;
      });
    }
    $$('.pk').forEach(function (a) {
      a.addEventListener('click', function () {
        if (pickerWrap && !wide.matches) pickerWrap.open = false;
      });
    });
    show(fromHash(), !!location.hash);
  }

  function init() {
    initTheme();
    var page = doc.body.getAttribute('data-page');
    if (page === 'home') initHome();
    else if (page === 'chapter') initChapter();
    else if (page === 'walk') initWalk();
  }
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', init);
  else init();
})();
