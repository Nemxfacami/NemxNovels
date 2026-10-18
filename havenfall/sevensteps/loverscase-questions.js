// LoversCase question bank.
// Each choice has "effects": points added to (or removed from) the user's traits. Everyone starts at 50 / 100.
// To add a question, copy a block, change the text, and set the effects. The quiz + scoring update automatically.

const LC_QUESTIONS = [
  {
    id: "q1",
    scenario: ["Alice and Bob are stranded in the desert. Alice is injured and cannot walk. If Bob carries Alice to safety, they both have a 31% chance of survival. If Bob leaves Alice behind, his own chance of survival increases by 9%."],
    ask: "What do you think Bob should do?",
    choices: [
      { text: "Bob should leave Alice.", effects: { selfPreservation: 10, loyalty: -10, riskTaking: -5, empathy: -5 } },
      { text: "Bob should stay with Alice, regardless of the odds.", effects: { loyalty: 12, empathy: 8, selfPreservation: -8, riskTaking: 5 } },
      { text: "Bob should try to carry Alice, even if it reduces their chances of survival.", effects: { loyalty: 8, empathy: 10, riskTaking: 10, selfPreservation: -5 } },
      { text: "Bob should let Alice decide whether he leaves her.", effects: { autonomy: 12, control: -10, loyalty: 4 } },
      { text: "Bob should convince Alice that leaving her is the best thing he can do.", effects: { control: 10, selfPreservation: 8, autonomy: -8, loyalty: -4 } },
    ]
  },
  {
    id: "q2",
    scenario: ["You are kidnapped and taken to a jungle you've never been to. You don't know where you are, and you aren't alone.", "One of the other people who was kidnapped decides to rebel and plans an escape. He claims to have extensive knowledge of jungles and believes he can lead everyone to safety."],
    ask: "What would you do?",
    choices: [
      { text: "Follow him. He might actually be able to lead you out.", effects: { trust: 10, riskTaking: 8, suspicion: -5 } },
      { text: "Tell your captors about his plan so they see you as trustworthy.", effects: { selfPreservation: 12, loyalty: -12, trust: -5 } },
      { text: "Keep quiet and refuse to get involved.", effects: { riskTaking: -5, suspicion: 3, control: -2 } },
      { text: "Convince the others that he's lying and stop them from following him.", effects: { control: 12, suspicion: 8, trust: -5 } },
    ]
  },
  {
    id: "q3",
    scenario: ["You are walking home alone at night when a stranger approaches you. He says someone is following him and asks you to let him walk with you because he is afraid.", "You look behind him but don't see anyone."],
    ask: "What would you do?",
    choices: [
      { text: "Let him walk with you.", effects: { trust: 10, empathy: 8, riskTaking: 6, suspicion: -6 } },
      { text: "Tell him to call the police and keep walking.", effects: { selfPreservation: 6, empathy: 2, suspicion: 4, control: 3 } },
      { text: "Ignore him completely.", effects: { selfPreservation: 8, empathy: -8, trust: -4 } },
      { text: "Stay nearby but keep your distance.", effects: { empathy: 4, suspicion: 5, selfPreservation: 4, riskTaking: 2 } },
      { text: "Ask him questions first to determine whether he's telling the truth.", effects: { suspicion: 8, control: 6, trust: -2 } },
    ]
  },
  {
    id: "q4",
    scenario: ["Your partner confesses that they did something terrible before you met them.", "They swear nobody was hurt, but they refuse to tell you what they did."],
    ask: "What would you do?",
    choices: [
      { text: "Accept that it's their past and don't ask further.", effects: { trust: 10, forgiveness: 8, autonomy: 4, suspicion: -8 } },
      { text: "Demand to know what happened.", effects: { control: 10, suspicion: 6, trust: -4 } },
      { text: "Give them time and wait until they're ready.", effects: { empathy: 8, forgiveness: 6, trust: 4, control: -4 } },
      { text: "Investigate without telling them.", effects: { suspicion: 12, control: 8, trust: -10, riskTaking: 4 } },
      { text: "End the relationship because they are hiding something.", effects: { selfPreservation: 10, trust: -6, forgiveness: -8, suspicion: 6 } },
    ]
  },
  {
    id: "q5",
    scenario: ["Your closest friend disappears without explanation.", "Three days later, they contact you privately and say:", "\"I'm safe. Don't tell anyone where I am.\"", "You know their family and the police are looking for them."],
    ask: "What would you do?",
    choices: [
      { text: "Tell their family immediately.", effects: { loyalty: -8, control: 6, empathy: 4 } },
      { text: "Tell the police.", effects: { loyalty: -10, control: 8, selfPreservation: 4, trust: -4 } },
      { text: "Keep their secret.", effects: { loyalty: 12, trust: 8, riskTaking: 6, control: -4 } },
      { text: "Ask them why they disappeared before deciding.", effects: { empathy: 6, suspicion: 4, trust: 4 } },
      { text: "Tell someone you trust but keep their location secret.", effects: { loyalty: 5, trust: 3, selfPreservation: 4, control: 3 } },
    ]
  },
  {
    id: "q6",
    scenario: ["You meet someone who seems almost perfect.", "They're kind, intelligent, attractive, funny, and incredibly interested in you.", "But there's one strange thing:", "Nobody who knows them seems willing to talk about their past."],
    ask: "What would you do?",
    choices: [
      { text: "Ignore it unless they give you a reason not to trust them.", effects: { trust: 10, suspicion: -8, riskTaking: 5 } },
      { text: "Ask them directly about their past.", effects: { trust: 3, control: 4, autonomy: 4 } },
      { text: "Investigate them yourself.", effects: { suspicion: 10, control: 8, trust: -6, riskTaking: 4 } },
      { text: "Ask their friends what they know.", effects: { suspicion: 6, control: 5, trust: -3, autonomy: -2 } },
      { text: "Walk away because the mystery itself is a warning.", effects: { selfPreservation: 10, riskTaking: -8, suspicion: 6, trust: -4 } },
    ]
  },
  {
    id: "q7",
    scenario: ["You discover that the person you're dating has secretly been keeping a detailed record of everything you've told them since you met.", "They have written down your likes, dislikes, fears, family problems, private stories, and things you've said when you thought nobody was paying attention."],
    ask: "What do you do?",
    choices: [
      { text: "Ask them why they've been keeping the record.", effects: { trust: 6, forgiveness: 5, empathy: 4, suspicion: -2 } },
      { text: "Read everything they've written.", effects: { control: 8, suspicion: 6, riskTaking: 6, autonomy: 2 } },
      { text: "Confront them and demand that they delete it.", effects: { autonomy: 10, control: 8, selfPreservation: 5 } },
      { text: "Say nothing and continue observing them.", effects: { suspicion: 12, control: 6, trust: -8, riskTaking: 3 } },
      { text: "End the relationship immediately.", effects: { selfPreservation: 10, forgiveness: -8, trust: -8, autonomy: 6 } },
    ]
  },
  {
    id: "q8",
    scenario: ["Someone offers you undeniable proof that your partner has betrayed you.", "They have the evidence with them, but they tell you:", "\"You don't want to see this.\""],
    ask: "What do you do?",
    choices: [
      { text: "Look at the evidence.", effects: { riskTaking: 8, control: 4, suspicion: 4 } },
      { text: "Refuse to look and confront your partner instead.", effects: { control: 8, trust: 4, riskTaking: 3 } },
      { text: "Ask them to explain what happened first.", effects: { trust: 10, forgiveness: 6, empathy: 4, suspicion: -6 } },
      { text: "Take the evidence but wait before looking at it.", effects: { control: 6, suspicion: 5, selfPreservation: 5, riskTaking: -3 } },
      { text: "Walk away and never ask about it.", effects: { selfPreservation: 10, autonomy: 4, trust: -4, riskTaking: -8, forgiveness: -2 } },
    ]
  },
  {
    id: "q9",
    scenario: ["You love someone so deeply that you believe the two of you are perfect together. Then another person begins pulling them away from you.", "You haven't been betrayed. Your partner hasn't promised you anything. They simply seem to be falling for someone else."],
    ask: "What would you do?",
    choices: [
      { text: "Fight for their love.", effects: { loyalty: 8, riskTaking: 8, control: 6 } },
      { text: "Tell them how you feel and let them choose.", effects: { autonomy: 10, trust: 8, empathy: 6, control: -6 } },
      { text: "Confront the person pursuing them.", effects: { control: 10, revenge: 6, riskTaking: 6, empathy: -4 } },
      { text: "Try to make the other person lose interest in them.", effects: { control: 12, revenge: 10, empathy: -10, trust: -4 } },
      { text: "Step aside and let your partner choose, even if it breaks your heart.", effects: { autonomy: 8, empathy: 10, selfPreservation: -6, control: -8, forgiveness: 4 } },
    ]
  },
  {
    id: "q10",
    scenario: [],
    ask: "If you had the power to shape someone into the person you wanted them to be, which trait would you want them to have most?",
    choices: [
      { text: "Kindness", effects: { empathy: 6, forgiveness: 4, control: 3 } },
      { text: "Loyalty", effects: { loyalty: 8, control: 5, suspicion: 2 } },
      { text: "Honesty", effects: { trust: 6, suspicion: 4, control: 3 } },
      { text: "Confidence", effects: { autonomy: 6, riskTaking: 5, control: 3 } },
      { text: "Patience", effects: { forgiveness: 5, empathy: 3, control: 3, revenge: -4 } },
      { text: "Empathy", effects: { empathy: 8, forgiveness: 3, control: 3 } },
    ]
  },
  {
    id: "q11",
    scenario: ["Imagine you had the power to shape someone into the person you wanted them to be.", "You choose their traits, and eventually you discover the truth:", "You never had that power.", "The person was kidnapped from their home and subjected to extreme pain and suffering until they became the person you wanted."],
    ask: "What would you do?",
    choices: [
      { text: "Help them escape and return to their old life.", effects: { empathy: 12, control: -12, autonomy: 6, selfPreservation: -4 } },
      { text: "Accept them as they are now, even though they were created through suffering.", effects: { control: 12, empathy: -10, selfPreservation: 6 } },
    ]
  },
  {
    id: "q12",
    scenario: ["You catch your partner cheating on you with someone you know.", "Your partner admits what they did and promises they will never do it again."],
    ask: "What would you do?",
    choices: [
      { text: "Forgive your partner and try to rebuild the relationship.", effects: { forgiveness: 12, trust: 6, loyalty: 6, revenge: -8, selfPreservation: -4 } },
      { text: "Cheat on your partner too.", effects: { revenge: 12, forgiveness: -8, loyalty: -10, riskTaking: 6 } },
      { text: "Leave your partner.", effects: { selfPreservation: 8, autonomy: 6, forgiveness: -6, revenge: -2 } },
      { text: "Vow to punish both of them yourself.", effects: { revenge: 14, control: 8, forgiveness: -12, empathy: -6, riskTaking: 6 } },
    ]
  },
];