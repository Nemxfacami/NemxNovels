/* ==========================================================
   CASES — builds the 20 cards + glitches the VIEW buttons
   Add after script.js:  <script src="cases.js"></script>

   Edit the CASES list to change titles / text / links.
   Images:  assets/cases/case-001.webp ... case-020.webp
   Links:   case-001.html ... (change `href` below if needed)
   Use <b>...</b> for the bold cream phrases.
   ========================================================== */

(() => {
  const CASES = [
 

  ['Rabacutas Statue', 'Recovered from a <b>possessed individual</b> in Havenfall, Edenus. The ancient demon <b>Rabacutas</b> sought a host.'],
  ['Dagger of Light', 'Made by <b>Magriman El Lazor</b> to kill his enemy. He gave the blade as a <b>gift</b>.'],
  ['Julius Mercesus Vase', 'Discovered in <b>Dothmodon</b> by ancient-cities enthusiasts. Its true origin remains unknown.'],
  ['How to Control Humans', 'Found inside a <b>cave in Western Ravenport</b>. Its authors and true origins remain unknown.'],
  ['Wakeep Pills', 'Created by the <b>finest scientists of Sociomic</b> through advanced pharmaceutical research.'],
   ['Lightning', '<b>Madlumuntu Ndlovu</b> used forbidden arts to weaponize lightning within a cube.'],
   ["The Saint's Finger", "A preserved saint\\'s finger said to <b>point toward places where humans were never meant to find anything</b>."],
  ['Steampunk Glasses', 'Created by an <b>absolute genius whose identity remains unknown</b>. The glasses are still being manufactured.'],
  ['Eye Contacts','Created by an <b>unknown maker</b>, these contacts allow the wearer to <b>switch bodies with anyone who looks them directly in the eye</b>.'],
  ['Perfect Compass', 'Found aboard a <b>ship near Dothmodon</b>. Said to lead its holder toward <b>their perfect better half</b>.'],
  ['Black Egg', 'A black egg that remains <b>warm to the touch</b> and occasionally produces a <b>distinct heartbeat</b>.'],
  ['Borrowed Shadow', 'A shadow <b>detached from its original owner</b> that still follows something. Buy it to discover what.'],
  ['Erenstein Camera', 'Whoever sees a photograph taken with it will be <b>killed by the person depicted before midnight</b>.'],
  ['Alien Doll', 'The doll <b>takes the form of the person its owner is attracted to</b>, turning fantasies into physical encounters.'],
  ['Honeypot', 'Its owner wants rid of it, claiming the pot and its gold bring <b>endless mysteries into your life</b>.'],
  ['The Pale Feather', 'A pale feather believed to have <b>fallen from something while flying</b>. Its origin remains unknown.'],
  ['Soul', 'A soul reportedly <b>captured after its owner died by suicide</b>, recovered by the mysterious <b>Suicide Hunters</b>.'],
  ['Faceless Photo', 'Everyone in the photograph has a face <b>except the person holding it</b>. The absence never changes.'],
  ['Mermaid', 'Said to grant <b>wealth through a deal</b>. Never look at its feminine features or become attracted to it.'],
  ['Carlos the Human', 'Carlos was <b>kidnapped from a beach</b> and reportedly possesses a <b>“third leg”</b> not used for walking.'],
  ["Eleanor's Panties", "Wearing them causes the wearer's <b>body to transform into Eleanor's body</b>."],
  ['Unknown Love Tattoo', 'Applied exclusively by <b>Dan Donalds</b>, this tattoo causes anyone marked by it to <b>fall permanently in love with the wearer</b>, even after death.'],

['3 Wishes Jinn', 'A <b>Jinn imprisoned in a cave</b> within the Dothmodon Wild Desert, capable of granting the buyer <b>three wishes</b>.'],

['Diogenes', 'A legendary <b>assassin who accepts contracts against anyone</b>, including beings in Heaven and Hell.'],

['Love Potion', 'Created by <b>Sosadium Company</b>, a single drop causes whoever drinks it to <b>fall in love with the person who administered it</b>.'],

['Necklace of Cylus', 'An anomalous necklace that forces anyone commanded by its wearer to <b>complete any possible task</b>, with failure resulting in death.'],

['Invitation Card', 'Found during an <b>anaconda hunting expedition</b> by Rodrigo Marinez, its purpose and supernatural properties remain unknown.'],

['Second Heart', 'Recovered from an <b>Anunnaki with three hearts</b>, this organ is believed to grant its recipient <b>2,000 additional years of life</b>.'],

['Key of Doors', 'A mysterious key capable of opening <b>any door to a different location in the present</b>, regardless of where the door originally leads.'],

['Hell Escape Card', 'Delivered mysteriously to Occult Arcana as a <b>gift from an unknown sender</b>, the card is believed to provide a way out of Hell.'],

['Naughty John Joy', 'An anomalous living device from an <b>unknown adult-toy manufacturer</b>, designed to extract <b>semen rather than blood</b>.'],

['Milkanum', 'Apparently just <b>ordinary milk</b>, although nobody knows why such a mundane product ended up in the Occult Arcana catalogue.'],

['Depresso Tea', 'An anomalous tea reportedly capable of providing <b>permanent relief from depression</b> after consumption.'],

['Skull of Roth', 'Found inside an ancient pyramid, speaking <b>"Rothacus Rathanos El&#39; Yelim"</b> while holding the skull reportedly reveals <b>visions of your future life</b>.'],

['Clone Seeds', 'Created by <b>Sosadium Company</b>, these seeds grow into plants that produce a <b>biological clone of the person who cultivated them</b>.'],

['Womenslator', 'Created by <b>Davenport</b>, this device claims to reveal <b>what a woman is thinking and exactly what she is feeling</b>.'],

['No Scars Razor', 'Recovered from a <b>blood-soaked crime scene with no visible wounds</b>, this razor causes injuries that completely heal without leaving scars after ten minutes.'],

['Idiot Virus', 'Recovered from an abandoned bunker in <b>Helen&#39;s Fields</b>, the virus causes those who inhale it to <b>permanently lose the ability to learn and acquire knowledge</b>.'],

['Time Travelling Watch', 'Found on a corpse in Southern Ravenport, this watch sends the wearer&#39;s <b>consciousness through time and into another person&#39;s body</b>.'],
  ];

  const grid = document.getElementById('cases-grid');
  if (!grid) return;

  const idFor = (i) => 'OA-' + String(471 + i).padStart(4, '0');

  grid.innerHTML = CASES.map(([title, text], i) => {
    const n = idFor(i);
    return `
      <article class="case">
        <div class="case__media">
          <img src="${n}.webp" alt="" loading="lazy" decoding="async">
          <span class="case__num">ITEM ${n}</span>
          <a class="view" href="item.html?id=${n}" aria-label="View case ${n}: ${title.replace(/"/g, '&quot;')}">
            <span class="view__txt" data-text="VIEW">VIEW</span>
          </a>
        </div>
        <div class="case__body">
          <h3 class="case__title">${title}</h3>
          <p class="case__text">${text}</p>
        </div>
      </article>`;
  }).join('');

  /* ---------- VIEW glitch (same style as the hero title) ---------- */
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) return;

  const FRAMES = [
    [-6,  10, 'none'],
    [ 8, -12, 'inset(0 0 52% 0)'],
    [-9,   4, 'inset(46% 0 0 0)'],
    [ 4,  -8, 'none'],
  ];
  const rand = (a, b) => a + Math.random() * (b - a);

  function glitch(btn, done) {
    const txt = btn.querySelector('.view__txt');
    const count = Math.random() < 0.5 ? 3 : 4;
    const flip = Math.random() < 0.5 ? -1 : 1;
    let i = 0;
    const step = () => {
      if (i >= count) {
        btn.classList.remove('is-glitching');
        txt.style.removeProperty('--gx');
        txt.style.removeProperty('--gy');
        txt.style.removeProperty('--gclip');
        return done();
      }
      const [x, y, clip] = FRAMES[(i + Math.floor(rand(0, FRAMES.length))) % FRAMES.length];
      txt.style.setProperty('--gx', (x * flip + rand(-1, 1)).toFixed(2) + '%');
      txt.style.setProperty('--gy', (y + rand(-2, 2)).toFixed(2) + '%');
      txt.style.setProperty('--gclip', clip);
      btn.classList.add('is-glitching');
      i++;
      setTimeout(step, rand(30, 50));
    };
    step();
  }

  // Only glitch buttons that are on screen, one at a time at random,
  // so 20 buttons don't all flicker together.
  const visible = new Set();
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => (e.isIntersecting ? visible.add(e.target) : visible.delete(e.target)));
  });
  grid.querySelectorAll('.view').forEach((b) => io.observe(b));

  function loop() {
    setTimeout(() => {
      const list = [...visible];
      if (document.hidden || !list.length) return loop();
      const btn = list[Math.floor(Math.random() * list.length)];
      glitch(btn, loop);
    }, rand(350, 900));
  }
  loop();
})();