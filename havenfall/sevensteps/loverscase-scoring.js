// LoversCase shared scoring + storage helpers (used by the quiz, results and discover pages).

const LC_TRAITS = [
  { key: 'loyalty',         label: 'Loyalty' },
  { key: 'selfPreservation', label: 'Self-preservation' },
  { key: 'trust',           label: 'Trust' },
  { key: 'suspicion',       label: 'Suspicion' },
  { key: 'autonomy',        label: 'Autonomy' },
  { key: 'control',         label: 'Control' },
  { key: 'riskTaking',      label: 'Risk-taking' },
  { key: 'empathy',         label: 'Empathy' },
  { key: 'forgiveness',     label: 'Forgiveness' },
  { key: 'revenge',         label: 'Revenge' }
];

const LC_STORAGE_KEY = 'loverscase_profile';

// answers = array of chosen choice indexes, one per question (same order as LC_QUESTIONS)
function lcCalcScores(questions, answers) {
  const scores = {};
  LC_TRAITS.forEach(t => { scores[t.key] = 50; });
  answers.forEach((choiceIndex, qi) => {
    const choice = questions[qi] && questions[qi].choices[choiceIndex];
    if (!choice) return;
    for (const trait in choice.effects) {
      scores[trait] += choice.effects[trait];
    }
  });
  LC_TRAITS.forEach(t => {
    scores[t.key] = Math.max(0, Math.min(100, scores[t.key]));
  });
  return scores;
}

// Saving replaces any older rating, so retaking the test always wipes the previous result.
function lcSaveProfile(scores, answers) {
  try {
    localStorage.removeItem(LC_STORAGE_KEY);
    localStorage.setItem(LC_STORAGE_KEY, JSON.stringify({
      scores: scores,
      answers: answers,
      takenAt: new Date().toISOString()
    }));
    return true;
  } catch (e) {
    return false;
  }
}

function lcLoadProfile() {
  try {
    const raw = localStorage.getItem(LC_STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (e) {
    return null;
  }
}

function lcClearProfile() {
  try { localStorage.removeItem(LC_STORAGE_KEY); } catch (e) {}
}

// ---------------------------------------------------------------------------
// MATCHING MODEL
//   50%  trait alignment      - how similar the two people are on the "similarity" traits
//   30%  relationship dynamics - cross-trait clashes (control vs autonomy, etc.)
//   20%  character preferences - what THIS character wants in a partner (character.wants)
// ---------------------------------------------------------------------------
const LC_WEIGHTS = { alignment: 0.5, dynamics: 0.3, preferences: 0.2 };

// These are best when the two people are close
const LC_SIMILARITY_TRAITS = ['loyalty', 'trust', 'empathy', 'forgiveness', 'autonomy'];

const LC_TRAIT_ADJECTIVE = {
  loyalty: 'loyal', trust: 'trusting', empathy: 'empathetic', forgiveness: 'forgiving', autonomy: 'independent'
};

// Friction = (one person's "from" trait x the other person's "to" trait) / 100.
// High control meeting high autonomy = big friction. The worse direction counts.
const LC_CROSS_PAIRS = [
  { from: 'control',    to: 'autonomy',         clash: (a, b) => a + ' need for control may clash with ' + b + ' need for independence.' },
  { from: 'suspicion',  to: 'trust',            clash: (a, b) => a + ' suspicion may wear on ' + b + ' trusting nature.' },
  { from: 'revenge',    to: 'forgiveness',      clash: (a, b) => a + ' tendency to hold grudges may not sit well with ' + b + ' forgiving side.' },
  { from: 'riskTaking', to: 'selfPreservation', clash: (a, b) => a + ' appetite for risk may worry ' + b + ' cautious side.' }
];

// user = the user's scores object, ch = a character from loverscase-characters.js
function lcMatch(user, ch) {
  const name = ch.name.split('<br>')[0];
  const avg = arr => arr.reduce((s, v) => s + v, 0) / arr.length;
  const label = k => LC_TRAITS.find(t => t.key === k).label.toLowerCase();

  // 1) trait alignment
  const gaps = LC_SIMILARITY_TRAITS.map(k => ({
    key: k,
    diff: Math.abs(user[k] - ch.traits[k]),
    userHigher: user[k] > ch.traits[k]
  }));
  const alignment = avg(gaps.map(g => 100 - g.diff));

  // 2) relationship dynamics
  let worst = null;
  const dynScores = LC_CROSS_PAIRS.map(p => {
    const userToChar = user[p.from] * ch.traits[p.to] / 100;
    const charToUser = ch.traits[p.from] * user[p.to] / 100;
    const friction = Math.max(userToChar, charToUser);
    if (!worst || friction > worst.friction) {
      worst = { pair: p, friction: friction, userIsSource: userToChar >= charToUser };
    }
    return 100 - friction;
  });
  const dynamics = avg(dynScores);

  // 3) what this character wants in a partner
  const wantKeys = Object.keys(ch.wants || {});
  const preferences = wantKeys.length
    ? avg(wantKeys.map(k => 100 - Math.abs(user[k] - ch.wants[k])))
    : alignment;

  const percent = Math.round(
    alignment * LC_WEIGHTS.alignment + dynamics * LC_WEIGHTS.dynamics + preferences * LC_WEIGHTS.preferences
  );

  // ---- wording ----
  const closest = gaps.slice().sort((a, b) => a.diff - b.diff).filter(g => g.diff <= 15).slice(0, 2);
  const matchText = closest.length
    ? 'You and ' + name + ' are closely matched on ' + closest.map(g => label(g.key)).join(' and ') + '.'
    : 'You and ' + name + ' are quite different on the core traits.';

  const frictions = [];
  const biggest = gaps.slice().sort((a, b) => b.diff - a.diff)[0];
  if (biggest.diff >= 20) {
    const adj = LC_TRAIT_ADJECTIVE[biggest.key];
    frictions.push(biggest.userHigher
      ? 'You are considerably more ' + adj + ' than ' + name + '.'
      : name + ' is considerably more ' + adj + ' than you.');
  }
  if (worst.friction >= 55) {
    frictions.push(worst.userIsSource
      ? worst.pair.clash('Your', name + "'s")
      : worst.pair.clash(name + "'s", 'your'));
  }
  if (!frictions.length) frictions.push('No major friction points.');

  let tier, dynamicText;
  if (percent >= 85)      { tier = 'Strong compatibility'; dynamicText = 'You two tend to see relationships the same way.'; }
  else if (percent >= 70) { tier = 'Good compatibility';   dynamicText = 'You have a solid base, with a few differences to work through.'; }
  else if (percent >= 55) { tier = 'Mixed compatibility';  dynamicText = 'You click in some ways and clash in others.'; }
  else                    { tier = 'Low compatibility';    dynamicText = 'You approach relationships very differently.'; }

  return {
    percent: percent, tier: tier,
    alignment: Math.round(alignment), dynamics: Math.round(dynamics), preferences: Math.round(preferences),
    matchText: matchText, frictions: frictions, dynamicText: dynamicText
  };
}