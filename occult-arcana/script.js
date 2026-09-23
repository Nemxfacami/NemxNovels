/* ==========================================================
   OCCULT ARCANA — hero behaviour
   1) Title glitch: a white ghost slips out of place for ~150ms
      roughly every 2s, then snaps back. Irregular timing.
   2) Symbols: hold 3s -> flip -> hold 2s -> flip back (in sync).
   ========================================================== */

(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1) Title glitch ---------- */
  const title = document.getElementById('title');

  // Ghost offsets are % of the title's own size (x = width, y = height).
  // Each frame: [x%, y%, clip-path]. The clip slices make it feel like
  // the text is tearing / slipping, not just sliding.
  const FRAMES = [
    [-1.6,   7, 'none'],
    [ 4.2, -10, 'inset(0 0 52% 0)'],
    [-5.5,   3, 'inset(46% 0 0 0)'],
    [ 2.2,  -6, 'none'],
  ];

  const rand = (min, max) => min + Math.random() * (max - min);
  const pick = (arr) => arr[Math.floor(Math.random() * arr.length)];

  function playGlitch(done) {
    // 3 or 4 frames of 30–50ms  ->  roughly 90–200ms total
    const count = Math.random() < 0.5 ? 3 : 4;
    const flipX = Math.random() < 0.5 ? -1 : 1;
    let i = 0;

    const step = () => {
      if (i >= count) {
        title.classList.remove('is-glitching');   // snap back
        title.style.removeProperty('--gx');
        title.style.removeProperty('--gy');
        title.style.removeProperty('--gclip');
        done();
        return;
      }
      const [x, y, clip] = FRAMES[(i + Math.floor(rand(0, FRAMES.length))) % FRAMES.length];
      title.style.setProperty('--gx', (x * flipX + rand(-0.6, 0.6)).toFixed(2) + '%');
      title.style.setProperty('--gy', (y + rand(-1.5, 1.5)).toFixed(2) + '%');
      title.style.setProperty('--gclip', clip);
      title.classList.add('is-glitching');
      i++;
      setTimeout(step, rand(30, 50));
    };
    step();
  }

  function scheduleGlitch(first) {
    // 1.5–2.3s of calm between glitches (a little longer before the first)
    const wait = first ? rand(1600, 2400) : rand(1500, 2300);
    setTimeout(() => {
      if (document.hidden) return scheduleGlitch(false);   // don't burn cycles in background tabs
      playGlitch(() => scheduleGlitch(false));
    }, wait);
  }

  if (title && !reduceMotion) scheduleGlitch(true);

  /* ---------- 2) Rotating symbols ---------- */
  const syms = document.querySelectorAll('.sym');
  const rots = document.querySelectorAll('.sym__rot');

  const HOLD_UP   = 3000;   // shown with the line
  const HOLD_FLIP = 2000;   // shown flipped, no line
  const TURN_MS   = 900;    // matches the CSS transition

  let stepCount = 0;

  function applyStep() {
    rots.forEach((g) => {
      const base = Number(g.dataset.offset) || 0;
      g.style.transform = `rotate(${base + stepCount * 180}deg)`;
    });
    syms.forEach((s) => s.classList.toggle('is-flipped', stepCount % 2 === 1));
  }

  function loop() {
    const holding = stepCount % 2 === 0 ? HOLD_UP : HOLD_FLIP;
    setTimeout(() => {
      stepCount++;
      applyStep();
      setTimeout(loop, TURN_MS);
    }, holding);
  }

  if (rots.length) {
    applyStep();   // set the starting angles (right symbol starts pointing down)
    loop();
  }
})();