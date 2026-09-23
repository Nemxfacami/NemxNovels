/* ==========================================================
   OCCULT ARCANA — live comment overlay + countdown + reorder + prune
                   + notify countdown + bell + notification + blackout
   Timeline (from page load):
     60s   → comment panel appears, empty
     +30s  → the full script has sent itself, one message at a time
     +40s  → panel fades out and is removed
     +120s → (measured from panel removal) a red countdown timer
             floats over the page, showing 07:00, counts down to
             06:30, then disappears.
     right after countdown disappears → the item grid flips: last
             card becomes first, first becomes last.
     +30s  → (measured from the flip finishing) every card is
             removed except Rabacutas Statue, Wakeep Pills,
             Black Egg, Borrowed Shadow, and Soul.
     right after prune finishes → a silent 10s wait (no timer shown).
     right after that wait → a notification bell button appears
             (SVG bell, badge "1").
     on bell click → a notification panel opens, styled the same
             as the comment panel, with one notification: "You
             bought a body." and an X close button.
     on X click → 30s later, all pruned items are displayed again
             (grid restored to its pre-prune order).
     +30s  → (measured from the restore) the entire site goes
             fully black — nothing rendered except a "Home"
             button, which links to
             https://nemxnovels.site/stories-page.html — until
             the page is reloaded. No restart otherwise.
   Add after cases.js:
   <script src="comments.js"></script>
   Requires comments.css.
   ========================================================== */

(() => {
  const APPEAR_AFTER   = 60000;   // 60s after load
  const SEND_WINDOW    = 30000;   // all messages sent within this span
  const HOLD_AFTER     = 40000;   // stays fully visible this long once done
  const COUNTDOWN_WAIT = 120000;  // delay after panel disappears before timer shows
  const COUNTDOWN_FROM = 420;     // 07:00 in seconds
  const COUNTDOWN_TO   = 390;     // 06:30 in seconds
  const PRUNE_WAIT     = 30000;   // delay after the grid flip before pruning

  const NOTIFY_WAIT              = 10000; // silent delay after prune, before the bell appears
  const BELL_TO_RESTORE_WAIT     = 30000; // delay after notification is closed, before items return
  const RESTORE_TO_BLACKOUT_WAIT = 30000; // delay after items return, before full blackout

  // Items that survive the prune, by id (as used in item.html?id=...)
  const KEEP_IDS = new Set(['OA-0471', 'OA-0475', 'OA-0481', 'OA-0482', 'OA-0487']);

  // Remembers the full, pre-prune card set + order so it can be restored later
  let savedGrid  = null;
  let savedCards = null;

  const PEOPLE = {
    marcus: { name: 'Marcus', avatar: 'marcus.webp' },
    elias:  { name: 'Elias',  avatar: 'elias.webp' },
  };

  const SCRIPT = [
    ['marcus', 'I\u2019ve been thinking about that whole "consciousness pilots the body" thing again. What if we\u2019ve got it backwards? What if the brain isn\u2019t producing consciousness at all?'],
    ['elias',  'Here we go.'],
    ['marcus', 'I\u2019m serious. Think about a radio. Destroy the radio and you don\u2019t prove the broadcast stopped existing. You only proved you destroyed the receiver.'],
    ['elias',  'Except consciousness isn\u2019t a radio signal we\u2019ve detected.'],
    ['marcus', 'Neither was radioactivity before we knew how to detect it.'],
    ['elias',  'That\u2019s exactly how people end up believing anything they can\u2019t explain.'],
    ['marcus', 'And that\u2019s exactly how people stop asking questions the moment an explanation becomes uncomfortable.'],
    ['elias',  'Fine. Let\u2019s say you\u2019re right. What is doing the receiving?'],
    ['marcus', 'That\u2019s the interesting part. Maybe consciousness is the interface and the soul is whatever exists behind it.'],
    ['elias',  'So you\u2019re saying I\u2019m not me?'],
    ['marcus', 'I\u2019m saying your body might be something you\u2019re using rather than something you are.'],
    ['elias',  'Then explain brain damage. Change the brain and you can change someone\u2019s memories, personality, even their sense of self.'],
    ['marcus', 'You change the interface, you change what gets through. That\u2019s not necessarily proof the user disappeared.'],
    ['elias',  'You realize you\u2019re building a theory that can\u2019t be disproved, right?'],
    ['marcus', 'Maybe. But here\u2019s the part I can\u2019t get out of my head.'],
    ['elias',  'What?'],
    ['marcus', 'If consciousness is only the brain talking to itself\u2026 why does there have to be someone experiencing the conversation?'],
  ];

  const esc = (s) => String(s).replace(/[&<>"']/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  function buildPanel() {
    const panel = document.createElement('div');
    panel.className = 'comments';
    panel.id = 'comments';
    panel.setAttribute('aria-hidden', 'true');
    panel.innerHTML = `
      <div class="comments__head"><span class="comments__dot" aria-hidden="true"></span>LIVE</div>
      <div class="comments__list" id="comments-list"></div>`;
    document.body.appendChild(panel);
    return panel;
  }

  const HEART = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 20.5s-7.5-4.6-10-9.3C.6 8 2 4.6 5.3 4c2-.4 3.9.5 5.2 2.3a.6.6 0 0 0 1 0C12.8 4.5 14.7 3.6 16.7 4c3.3.6 4.7 4 3.3 7.2-2.5 4.7-8 9.3-8 9.3z"/></svg>';

  function appendMessage(list, who) {
    const p = PEOPLE[who[0]];
    const text = who[1];
    const row = document.createElement('div');
    row.className = 'comment';
    row.innerHTML = `
      <span class="comment__avatar"><img src="${esc(p.avatar)}" alt="" loading="lazy"></span>
      <span class="comment__body">
        <span class="comment__top">
          <span class="comment__name">${esc(p.name)}</span>
          <span class="comment__time">now</span>
        </span>
        <p class="comment__text">${esc(text)}</p>
        <span class="comment__reply">Reply</span>
      </span>
      <span class="comment__heart" aria-hidden="true">${HEART}</span>`;
    const nearBottom = list.scrollHeight - list.scrollTop - list.clientHeight < 60;
    list.appendChild(row);
    if (nearBottom) list.scrollTop = list.scrollHeight;
  }

  function playScript(panel) {
    const list = panel.querySelector('#comments-list');
    const step = SEND_WINDOW / SCRIPT.length;

    SCRIPT.forEach((line, i) => {
      const jitter = (Math.random() - 0.5) * step * 0.4;
      setTimeout(() => appendMessage(list, line), Math.max(0, i * step + jitter));
    });

    const totalTime = SEND_WINDOW + HOLD_AFTER;
    setTimeout(() => {
      panel.classList.add('is-hiding');
      panel.classList.remove('is-visible');
      setTimeout(() => {
        panel.remove();
        // countdown timer begins its own wait once the panel is gone
        setTimeout(startCountdown, COUNTDOWN_WAIT);
      }, 500);
    }, totalTime);
  }

  /* ---------- Countdown timer (07:00 → 06:30, then gone) ---------- */
  function format(sec) {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
  }

  function startCountdown() {
    const timer = document.createElement('div');
    timer.className = 'countdown';
    timer.id = 'countdown';
    timer.setAttribute('aria-hidden', 'true');
    timer.innerHTML = `<span class="countdown__digits" id="countdown-digits">${format(COUNTDOWN_FROM)}</span>`;
    document.body.appendChild(timer);

    requestAnimationFrame(() => timer.classList.add('is-visible'));

    const digits = timer.querySelector('#countdown-digits');
    let secondsLeft = COUNTDOWN_FROM;

    const tick = setInterval(() => {
      secondsLeft--;
      digits.textContent = format(secondsLeft);
      if (secondsLeft <= COUNTDOWN_TO) {
        clearInterval(tick);
        timer.classList.add('is-hiding');
        timer.classList.remove('is-visible');
        setTimeout(() => {
          timer.remove();
          reverseCaseGrid();
        }, 500);
      }
    }, 1000);
  }

  /* ---------- Flip the item grid order (top↔bottom) ---------- */
  function reverseCaseGrid() {
    const grid = document.getElementById('cases-grid');
    if (!grid) return;

    const cards = [...grid.children];
    if (!cards.length) return;

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const afterFlip = () => setTimeout(pruneCaseGrid, PRUNE_WAIT);

    if (reduceMotion) {
      cards.reverse().forEach((card) => grid.appendChild(card));
      afterFlip();
      return;
    }

    grid.classList.add('is-reordering');
    setTimeout(() => {
      cards.reverse().forEach((card) => grid.appendChild(card));
      grid.classList.remove('is-reordering');
      grid.classList.add('is-reordered');
      setTimeout(() => grid.classList.remove('is-reordered'), 500);
      afterFlip();
    }, 300);
  }

  /* ---------- Prune the grid down to KEEP_IDS ---------- */
  function idFromCard(card) {
    const link = card.querySelector('.view');
    if (!link) return null;
    const href = link.getAttribute('href') || '';
    const match = href.match(/id=([^&]+)/i);
    return match ? match[1].toUpperCase() : null;
  }

  function pruneCaseGrid() {
    const grid = document.getElementById('cases-grid');
    if (!grid) {
      startNotifyCountdown();
      return;
    }

    const cards = [...grid.children];
    const toRemove = cards.filter((card) => !KEEP_IDS.has(idFromCard(card)));

    if (!toRemove.length) {
      setTimeout(showBell, NOTIFY_WAIT);
      return;
    }

    // remember the full set + order so we can bring it back later
    savedGrid  = grid;
    savedCards = cards;

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (reduceMotion) {
      toRemove.forEach((card) => card.remove());
      setTimeout(showBell, NOTIFY_WAIT);
      return;
    }

    toRemove.forEach((card) => card.classList.add('is-pruning'));
    setTimeout(() => {
      toRemove.forEach((card) => card.remove());
      setTimeout(showBell, NOTIFY_WAIT);
    }, 400);
  }

  /* ---------- Notification bell button ---------- */
  const BELL_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>';

  function showBell() {
    const bell = document.createElement('button');
    bell.type = 'button';
    bell.className = 'bell';
    bell.id = 'notif-bell';
    bell.setAttribute('aria-label', 'Notifications');
    bell.innerHTML = `<span class="bell__icon">${BELL_SVG}</span><span class="bell__badge">1</span>`;
    document.body.appendChild(bell);

    requestAnimationFrame(() => bell.classList.add('is-visible'));

    bell.addEventListener('click', () => {
      bell.classList.remove('is-visible');
      setTimeout(() => bell.remove(), 400);
      showNotificationPanel();
    }, { once: true });
  }

  /* ---------- Notification panel (same look as the comment panel) ---------- */
  function showNotificationPanel() {
    const panel = document.createElement('div');
    panel.className = 'comments notifications';
    panel.id = 'notifications';
    panel.setAttribute('aria-hidden', 'true');
    panel.innerHTML = `
      <div class="comments__head">
        <span class="comments__dot" aria-hidden="true"></span>NOTIFICATIONS
        <button type="button" class="notifications__close" aria-label="Close">&times;</button>
      </div>
      <div class="comments__list">
        <div class="comment notification">
          <span class="comment__body">
            <span class="comment__top">
              <span class="comment__name">Occult Arcana</span>
              <span class="comment__time">now</span>
            </span>
            <p class="comment__text">You bought a body.</p>
          </span>
        </div>
      </div>`;
    document.body.appendChild(panel);

    requestAnimationFrame(() => panel.classList.add('is-visible'));

    const closeBtn = panel.querySelector('.notifications__close');
    closeBtn.addEventListener('click', () => {
      panel.classList.add('is-hiding');
      panel.classList.remove('is-visible');
      setTimeout(() => {
        panel.remove();
        setTimeout(restoreCaseGrid, BELL_TO_RESTORE_WAIT);
      }, 500);
    }, { once: true });
  }

  /* ---------- Bring the pruned items back, then black out the site ---------- */
  function restoreCaseGrid() {
    if (savedGrid && savedCards) {
      savedCards.forEach((card) => {
        card.classList.remove('is-pruning');
        savedGrid.appendChild(card);
      });
    }
    setTimeout(blackoutSite, RESTORE_TO_BLACKOUT_WAIT);
  }

  function blackoutSite() {
    document.documentElement.style.overflow = 'hidden';
    const cover = document.createElement('div');
    cover.className = 'blackout';
    cover.innerHTML = `<button type="button" class="blackout__home">Home</button>`;
    document.body.appendChild(cover);
    requestAnimationFrame(() => cover.classList.add('is-visible'));

    cover.querySelector('.blackout__home').addEventListener('click', () => {
      window.location.href = 'https://nemxnovels.site/stories-page.html';
    });
  }

  function start() {
    setTimeout(() => {
      const panel = buildPanel();
      // next frame, so the transition actually runs
      requestAnimationFrame(() => panel.classList.add('is-visible'));
      playScript(panel);
    }, APPEAR_AFTER);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();