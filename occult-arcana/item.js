/* ==========================================================
   OCCULT ARCANA — item page
   Open with:  item.html?id=OA-0471
   Add items to the ITEMS list below. Fields:
     id            item number / serial (shown top-left of the image)
     name          product name
     price         number, shown in Crowns (₡)
     category      Artifact, Book, Relic, Device, Clothing ...
     availability  In Stock | Limited | Unknown | Unavailable
     condition     New | Used | Damaged | Unknown
     image         path to the picture
     origin        the paragraph (use <b>...</b> for cream highlights)
   ========================================================== */

(() => {
  const ITEMS = [

    {
      id: 'OA-0471',
      name: 'Rabacutas Statue',
      price: 597,
      category: 'Relic',
      availability: 'In Stock',
      condition: 'Unknown',
      image: 'OA-0474.webp',
      origin: 'Recovered from an individual discovered to be under the possession of an unidentified entity in Edenus, Havenfall. The entity, believed to be the demon known as <b>Rabacutas</b>, was reportedly attempting to establish a permanent host through the individual. The statue was recovered following the incident. Its exact connection to Rabacutas remains undocumented, although records suggest that the object may have served as a vessel, anchor, or representation of the entity prior to its recovery. The circumstances surrounding its original creation, the identity of its maker, and the manner in which it came into the possession of the host remain unknown.',
    },
    {
      id: 'OA-0475',
      name: 'Wakeep Pills',
      price: 800,
      category: 'Pills',
      availability: 'In Stock',
      condition: 'New',
      image: 'OA-0475.webp',
      origin: 'Manufactured in Sociomic by a select team of its most accomplished scientists and researchers. Wakeep Pills - are <b>hypnagogic state pills </b>, they were developed through advanced pharmaceutical research and refined through extensive laboratory testing. The precise methodology behind their production remains proprietary to Sociomic, with the full composition and development process restricted to authorized personnel.',
    },
    {
      id: 'OA-0473',
      name: 'Julius Mercesus Vase',
      price: 14000,
      category: 'Antiquity',
      availability: 'Limited',
      condition: 'Used',
      image: 'OA-0473.webp',
      origin: 'The origins of the Julius Mercesus Vase remain unknown. The vase was discovered in <b>Dothmodon</b> by a group of ancient-cities enthusiasts conducting an unofficial exploration of the region. No definitive record has been established regarding its original creator, period of construction, or intended purpose. The name <b>Julius Mercesus</b> is believed to have been associated with the artifact after its discovery, although the reason for the designation remains undocumented. Further archaeological examination has yet to establish where the vase originated or how it came to be preserved in Dothmodon.',
    },
    {
      id: 'OA-0472',
      name: 'Dagger of Light',
      price: 5700,
      category: 'Weapon',
      availability: 'Limited',
      condition: 'Used',
      image: 'OA-0472.webp',
      origin: 'The Dagger of Light is believed to have been created for a singular purpose: to kill the individual who possesses it. Historical accounts attribute its creation to <b>Magriman El Lazor</b>, who is said to have sought the death of an enemy without confronting him directly. Rather than presenting his enemy with a weapon openly, Magriman offered the dagger as a gift. The intention was simple. The recipient would accept what appeared to be a valuable and extraordinary blade, unaware that the weapon had allegedly been designed to turn against its owner. The circumstances surrounding the dagger\'s creation remain uncertain, as do the means by which it is believed to accomplish its purpose. Only a limited number of records concerning the weapon have survived.',
    },
    {
      id: 'OA-0476',
      name: 'Lightning',
      price: 130,
      category: 'Weapon',
      availability: 'In Stock',
      condition: 'New',
      image: 'OA-0476.webp',
      origin: 'The weaponization of lightning is attributed to <b>Madlumuntu Ndlovu</b>, who is believed to have employed forbidden arts to contain and manipulate the phenomenon within a compact cube. According to Ndlovu\'s instructions, the cube must be handled with particular caution. Buyers are advised <b>not to speak their own name while holding the object</b>, as the lightning is said to recognize the spoken name and strike its bearer. To direct the lightning toward another individual, the holder must speak only the name of the intended target. Whether the cube responds to the spoken name itself or to something beyond ordinary physical mechanisms remains undocumented.',
    },
    {
      id: 'OA-0474',
      name: 'How to Control Humans',
      price: 345,
      category: 'Book',
      availability: 'Limited',
      condition: 'New',
      image: 'OA-0474.webp',
      origin: 'The authorship of <i>How to Control Humans</i> remains unknown. According to the account accompanying the manuscript, the book was discovered inside a previously undocumented cave in <b>Western Ravenport</b>. The cave was reportedly found by accident, with the circumstances of its discovery remaining poorly documented. No author, publisher, or identifiable origin has been attributed to the book. The age of the manuscript is similarly uncertain, as its physical condition appears inconsistent with the circumstances surrounding its discovery. How the book came to be inside the cave, who placed it there, and why it was written remain unknown.',
    },
     {
      id: 'OA-0477',
      name: 'The Saint\'s Finger',
      price: 8500,
      category: 'Relic',
      availability: 'Limited',
      condition: 'Used',
      image: 'OA-0477.webp',
      origin: 'A preserved saint\'s finger said to <b>point toward places where humans were never meant to find anything</b>.',
    },
    {
      id: 'OA-0478',
      name: 'Steampunk Glasses',
      price: 770,
      category: 'Wearable Device',
      availability: 'Limited',
      condition: 'New',
      image: 'OA-0478.webp',
      origin: 'Created by an <b>absolute genius whose identity remains unknown</b>. The glasses are still being manufactured.',
    },
    {
  id: 'OA-0479',
  name: 'Eye Contacts',
  price: 670,
  category: 'Wearable Device',
  availability: 'Unavailable',
  condition: 'New',
  image: 'OA-0479.webp',
  origin: 'Created by an <b>unknown maker</b>, these contacts allow the wearer to <b>switch bodies with anyone who looks them directly in the eye</b>. The effect lasts until the wearer obtains another pair. <b>Each contact works only once</b>.',
},

    {
      id: 'OA-0480',
      name: 'Perfect Compass',
      price: 1200,
      category: 'Relic',
      availability: 'Limited',
      condition: 'New',
      image: 'OA-0480.webp',
      origin: 'Found aboard a <b>ship near Dothmodon</b>. Said to lead its holder toward <b>their perfect better half</b>. The last owner was never found when the compass was obtained.',
    },
    {
      id: 'OA-0481',
      name: 'Black Egg',
      price: 390,
      category: 'Biological Anomaly',
      availability: 'In Stock',
      condition: 'New',
      image: 'OA-0481.webp',
      origin: 'A black egg that remains <b>warm to the touch</b> and occasionally produces a <b>distinct heartbeat</b>.',
    },
    {
      id: 'OA-0482',
      name: 'Borrowed Shadow',
      price: 670,
      category: 'Anomaly',
      availability: 'Limited',
      condition: 'Unknown',
      image: 'OA-0482.webp',
      origin: 'A shadow <b>detached from its original owner</b> that still follows something. Buy it to discover what.',
    },
    {
      id: 'OA-0483',
      name: 'Erenstein Camera',
      price: 5440,
      category: 'Cursed Artifact',
      availability: 'In Stock',
      condition: 'New',
      image: 'OA-0483.webp',
      origin: 'Whoever sees a photograph taken with it will be <b>killed by the person depicted before midnight</b>.',
    },
    {
      id: 'OA-0484',
      name: 'Alien Doll',
      price: 7050,
      category: 'Occult Artifact',
      availability: 'Limited',
      condition: 'New',
      image: 'OA-0484.webp',
      origin: 'The doll <b>takes the form of the person its owner is attracted to</b>, turning fantasies into physical encounters. Note : If your desires are abnormal ,we are not at fault.',
    },
    {
      id: 'OA-0485',
      name: 'Honeypot',
      price: 10,
      category: 'Occult Relic',
      availability: 'Limited',
      condition: 'New',
      image: 'assets/items/oa-0485.webp',
      origin: 'Its owner wants rid of it, claiming the pot and its gold bring <b>endless mysteries into your life</b>.',
    },
    {
      id: 'OA-0486',
      name: 'The Pale Feather',
      price: 5,
      category: 'Curiosity',
      availability: 'Limited',
      condition: 'Used',
      image: 'OA-0486.webp',
      origin: 'A pale feather believed to have <b>fallen from something while flying</b>. Its origin remains unknown.',
    },
    {
      id: 'OA-0487',
      name: 'Soul',
      price: 15000,
      category: 'Occult Relic',
      availability: 'Purchased',
      condition: 'Used',
      image: 'OA-0487.webp',
      origin: 'A soul reportedly <b>captured after its owner died by suicide</b>, recovered by the mysterious <b>Suicide Hunters</b>.',
    },
    {
      id: 'OA-0488',
      name: 'Faceless Photo',
      price: 1,
      category: 'Anomalous Photograph',
      availability: 'Limited',
      condition: 'Used',
      image: 'OA-0488.webp',
      origin: 'Everyone in the photograph has a face <b>except the person holding it</b>. The absence never changes.',
    },
    {
      id: 'OA-0489',
      name: 'Mermaid',
      price: 20000,
      category: 'Supernatural Entity',
      availability: 'Limited',
      condition: 'Used',
      image: 'OA-0489.webp',
      origin: 'Said to grant <b>wealth through a deal</b>. Never look at its feminine features or become attracted to it. Many who follow their own opinions learn these simple advices painfully.',
    },
    {
      id: 'OA-0490',
      name: 'Carlos the Human',
      price: 13000,
      category: 'Human Specimen',
      availability: 'Limited',
      condition: 'Used',
      image: 'OA-0490.webp',
      origin: 'Carlos was <b>kidnapped from a beach</b> and reportedly possesses a <b>“third leg”</b> not used for walking. He is mostly bought by females ,it already explains a lot about him.',
    },
    {
      id: 'OA-0491',
      name: 'Eleanor\'s Panties',
      price: 900,
      category: 'Transformative Artifact',
      availability: 'In Stock',
      condition: 'Used',
      image: 'OA-0491.webp',
      origin: 'Wearing them causes the wearer\'s <b>body to transform into Eleanor\'s body</b>. It you find another Eleanor you better kill her before she kills you. We do take refunds. ',
    },


  ];

  const esc = (s) => String(s).replace(/[&<>"']/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  const slug = (s) => String(s).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

  const root = document.getElementById('item');
  if (!root) return;

  const wanted = (new URLSearchParams(location.search).get('id') || '').toUpperCase();
  const item = wanted ? ITEMS.find((i) => i.id.toUpperCase() === wanted) : ITEMS[0];

  if (!item) {
    root.innerHTML = '<div class="item-missing">ITEM NOT FOUND</div>';
    return;
  }

  document.title = `${item.name} — Occult Arcana`;

  // Crowns: whole numbers get thousands separators, e.g. 1,250
  const price = Number(item.price).toLocaleString('en-US');

  root.innerHTML = `
    <article class="item">
      <div class="item__media">
        <img src="${esc(item.image)}" alt="${esc(item.name)}" decoding="async">
        <span class="item__num">${esc(item.id)}</span>
      </div>

      <div class="item__body">
        <h1 class="item__title">${esc(item.name)}</h1>
        <p class="item__price">₡ ${price} <small>CROWNS</small></p>

        <dl class="item__facts">
          <div class="fact"><dt>Category</dt><dd>${esc(item.category)}</dd></div>
          <div class="fact"><dt>Availability</dt>
            <dd><span class="avail avail--${slug(item.availability)}">${esc(item.availability)}</span></dd></div>
          <div class="fact"><dt>Item ID</dt><dd class="mono">${esc(item.id)}</dd></div>
          <div class="fact"><dt>Condition</dt><dd>${esc(item.condition)}</dd></div>
        </dl>

        <section class="item__origin">
          <h2 class="item__label">Origin</h2>
          <p>${item.origin}</p>
        </section>

        <button type="button" class="item__buy" id="buy-btn">Purchase</button>
      </div>
    </article>`;

  const buyBtn = document.getElementById('buy-btn');

 if (item.availability === 'Purchased') {
    buyBtn.disabled = true;
    buyBtn.textContent = 'Purchased';
    buyBtn.classList.add('item__buy--purchased');
    return;
  }

  /* ---------- Special case: Wakeep Pills reveals an image ---------- */
  if (item.id.toUpperCase() === 'OA-0475') {
    const imgVeil = document.createElement('div');
    imgVeil.className = 'img-veil';
    imgVeil.setAttribute('role', 'dialog');
    imgVeil.setAttribute('aria-modal', 'true');
    imgVeil.setAttribute('aria-hidden', 'true');
    imgVeil.innerHTML = `
      <div class="img-veil__box">
        <button type="button" class="img-veil__close" id="img-veil-close" aria-label="Close">&times;</button>
        <img src="you.webp" alt="" decoding="async">
      </div>`;
    document.body.appendChild(imgVeil);

    const imgCloseBtn = document.getElementById('img-veil-close');
    let lastFocusImg = null;

    const openImgVeil = () => {
      lastFocusImg = document.activeElement;
      imgVeil.classList.add('is-open');
      imgVeil.setAttribute('aria-hidden', 'false');
      imgCloseBtn.focus();
    };
    const closeImgVeil = () => {
      imgVeil.classList.remove('is-open');
      imgVeil.setAttribute('aria-hidden', 'true');
      if (lastFocusImg) lastFocusImg.focus();
    };

    buyBtn.addEventListener('click', openImgVeil);
    imgCloseBtn.addEventListener('click', closeImgVeil);
    imgVeil.addEventListener('click', (e) => { if (e.target === imgVeil) closeImgVeil(); });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && imgVeil.classList.contains('is-open')) closeImgVeil();
    });

    return; // skip the text veil entirely for this item
  }

  /* ---------- Purchase-blocked dialog (everything else) ---------- */
  const MESSAGE = 'You cannot interact with this world.';

  const veil = document.createElement('div');
  veil.className = 'veil';
  veil.setAttribute('role', 'dialog');
  veil.setAttribute('aria-modal', 'true');
  veil.setAttribute('aria-hidden', 'true');
  veil.innerHTML = `
    <div class="veil__box">
      <div class="veil__mark" aria-hidden="true">&times;</div>
      <p class="veil__text" id="veil-text" data-text="${esc(MESSAGE)}">${esc(MESSAGE)}</p>
      <button type="button" class="veil__close" id="veil-close">CLOSE</button>
    </div>`;
  document.body.appendChild(veil);

  const closeBtn = document.getElementById('veil-close');
  const veilText = document.getElementById('veil-text');
  let lastFocus = null;

  const rand = (a, b) => a + Math.random() * (b - a);
  const FRAMES = [
    [-2.4,  9, 'none'],
    [ 3.6, -8, 'inset(0 0 52% 0)'],
    [-4.8,  3, 'inset(46% 0 0 0)'],
    [ 2.0, -5, 'none'],
  ];

  function glitchOnce() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const count = Math.random() < 0.5 ? 3 : 4;
    const flip = Math.random() < 0.5 ? -1 : 1;
    let i = 0;
    const step = () => {
      if (i >= count) {
        veilText.classList.remove('is-glitching');
        veilText.style.removeProperty('--gx');
        veilText.style.removeProperty('--gy');
        veilText.style.removeProperty('--gclip');
        return;
      }
      const [x, y, clip] = FRAMES[(i + Math.floor(rand(0, FRAMES.length))) % FRAMES.length];
      veilText.style.setProperty('--gx', (x * flip + rand(-0.6, 0.6)).toFixed(2) + '%');
      veilText.style.setProperty('--gy', (y + rand(-1.2, 1.2)).toFixed(2) + '%');
      veilText.style.setProperty('--gclip', clip);
      veilText.classList.add('is-glitching');
      i++;
      setTimeout(step, rand(30, 50));
    };
    step();
  }

  function openVeil() {
    lastFocus = document.activeElement;
    veil.classList.add('is-open');
    veil.setAttribute('aria-hidden', 'false');
    closeBtn.focus();
    glitchOnce();
  }

  function closeVeil() {
    veil.classList.remove('is-open');
    veil.setAttribute('aria-hidden', 'true');
    if (lastFocus) lastFocus.focus();
  }

  buyBtn.addEventListener('click', openVeil);
  closeBtn.addEventListener('click', closeVeil);
  veil.addEventListener('click', (e) => { if (e.target === veil) closeVeil(); });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && veil.classList.contains('is-open')) closeVeil();
  });
})();