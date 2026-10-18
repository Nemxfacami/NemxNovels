// LoversCase characters - Seven Steps of Death (Havenfall).
// Used by the discover page.
// "traits" = the character's own 0-100 ratings (same 10 traits as the user).
// "wants"  = what this character wants in a partner (0-100 targets for the user's traits) - 2-4 per character.
// "role"   = the short label shown above the name.
// Photos live in /havenfall/sevensteps/ as <name>.webp. Add a character by copying a block.

const LC_PHOTO_PATH = "";

const LC_CHARACTERS = [
  {
    name:"Raymond<br>Kazersdale", handle:"@raymond.kazersdale", age:28, location:"Havenfall, Kingsmere",
    role:"The Heir",
    bio:"Tell me you read the newspaper too, because I'm very good at holding one. Water over wine, always. Please do not wake me by pouring it on my face.",
    traits:{loyalty:80,selfPreservation:55,trust:40,suspicion:72,autonomy:65,control:50,riskTaking:60,empathy:70,forgiveness:55,revenge:40},
    wants:{loyalty:85,trust:70,empathy:65},
    photos:[LC_PHOTO_PATH + "raymond.webp"]
  },
  {
    name:"Alex<br>Kazersdale", handle:"@alex.kazersdale", age:25, location:"Havenfall, Kingsmere",
    role:"The Boss",
    bio:"I run a very tight dungeon. Biker friends, a short temper, and a permanent shortage of honey. My brother is a work in progress.",
    traits:{loyalty:75,selfPreservation:60,trust:25,suspicion:80,autonomy:90,control:85,riskTaking:85,empathy:35,forgiveness:20,revenge:75},
    wants:{loyalty:80,autonomy:85,riskTaking:75},
    photos:[LC_PHOTO_PATH + "alex.webp"]
  },
  {
    name:"Arabella<br>Cavendish", handle:"@arabella.cavendish", age:29, location:"Havenfall, Helen's Field",
    role:"The Crown Jewel",
    bio:"I never raise my voice. I simply look at you until you start wondering what I'm thinking. Daddy's wine collector, and nobody's fool.",
    traits:{loyalty:60,selfPreservation:70,trust:35,suspicion:70,autonomy:75,control:70,riskTaking:55,empathy:55,forgiveness:45,revenge:50},
    wants:{loyalty:75,trust:60,autonomy:70},
    photos:[LC_PHOTO_PATH + "arabella.webp"]
  },
  {
    name:"Hugo<br>Cavendish", handle:"@hugo.cavendish", age:61, location:"Havenfall, Helen's Field",
    role:"The Gold Dealer",
    bio:"Boots on the desk, gold in the vault. My attention has an admission fee. If you want it, come and collect it.",
    traits:{loyalty:55,selfPreservation:85,trust:20,suspicion:85,autonomy:85,control:90,riskTaking:60,empathy:30,forgiveness:25,revenge:70},
    wants:{loyalty:90,selfPreservation:60,trust:40},
    photos:[LC_PHOTO_PATH + "hugo.webp"]
  },
  {
    name:"Lucille", handle:"@lucille", age:31, location:"Havenfall, Edenus",
    role:"The Tracker",
    bio:"I find people for a living. I have never confused 'perhaps' with 'immediately'. Flirt with me and I might suggest the shower.",
    traits:{loyalty:50,selfPreservation:65,trust:40,suspicion:65,autonomy:85,control:60,riskTaking:85,empathy:55,forgiveness:35,revenge:55},
    wants:{riskTaking:80,autonomy:80,loyalty:70},
    photos:[LC_PHOTO_PATH + "lucille.webp"]
  },
  {
    name:"Cobb<br>Doyley", handle:"@cobb.doyley", age:37, location:"Havenfall, Edenus",
    role:"The Hunter",
    bio:"Left-handed, well dressed, and already decided how the day ends. I don't chat. My brother does that for both of us.",
    traits:{loyalty:85,selfPreservation:60,trust:35,suspicion:75,autonomy:55,control:65,riskTaking:65,empathy:30,forgiveness:25,revenge:55},
    wants:{loyalty:85,trust:40,riskTaking:65},
    photos:[LC_PHOTO_PATH + "cobb.webp"]
  },
  {
    name:"Carl<br>Doyley", handle:"@carl.doyley", age:37, location:"Havenfall, Edenus",
    role:"The Charmer",
    bio:"I have the kind of smile that makes strangers answer questions they didn't plan to. Saving up for a retirement house in Helen's Fields. Not yet, but soon.",
    traits:{loyalty:85,selfPreservation:55,trust:55,suspicion:50,autonomy:60,control:40,riskTaking:60,empathy:60,forgiveness:50,revenge:35},
    wants:{empathy:70,loyalty:80,forgiveness:60},
    photos:[LC_PHOTO_PATH + "carl.webp"]
  },
  {
    name:"Max", handle:"@max", age:51, location:"Havenfall, Kingsmere",
    role:"The Sergeant",
    bio:"Sergeant of a very particular dungeon. I take the blame so everyone else doesn't have to. The water project is going great, thanks for asking.",
    traits:{loyalty:90,selfPreservation:55,trust:55,suspicion:50,autonomy:40,control:45,riskTaking:40,empathy:60,forgiveness:65,revenge:20},
    wants:{empathy:70,forgiveness:70,loyalty:75},
    photos:[LC_PHOTO_PATH + "max.webp"]
  },
  {
    name:"Dizzy<br>Dean", handle:"@dizzy.dean", age:45, location:"Havenfall, Kingsmere",
    role:"The Kingpin",
    bio:"I understand money. I own the gym, the games, and a few engineers behind it. Always dreamed of the end of the world; it would be good for business.",
    traits:{loyalty:15,selfPreservation:90,trust:15,suspicion:70,autonomy:85,control:85,riskTaking:85,empathy:10,forgiveness:15,revenge:70},
    wants:{riskTaking:80,autonomy:60,loyalty:70},
    photos:[LC_PHOTO_PATH + "dean.webp"]
  },
  {
    name:"Thomas<br>Pembroke", handle:"@thomas.pembroke", age:22, location:"Havenfall, Helen's Fields",
    role:"The Thief",
    bio:"Right place, wrong van. I may have accidentally started a gold coin problem. Looking for someone who forgives easily.",
    traits:{loyalty:40,selfPreservation:75,trust:55,suspicion:35,autonomy:70,control:25,riskTaking:85,empathy:45,forgiveness:55,revenge:30},
    wants:{forgiveness:75,riskTaking:70,loyalty:55},
    photos:[LC_PHOTO_PATH + "thomas.webp"]
  },
  {
    name:"Theo<br>Pembroke", handle:"@theo.pembroke", age:48, location:"Havenfall, Helen's Fields",
    role:"The Patriarch",
    bio:"A cabin, a rocking chair and a yard full of chickens. I walk into other people's yards with my sharks, and I expect the same respect in mine.",
    traits:{loyalty:75,selfPreservation:60,trust:45,suspicion:60,autonomy:70,control:75,riskTaking:40,empathy:45,forgiveness:40,revenge:55},
    wants:{loyalty:85,trust:60,control:50},
    photos:[LC_PHOTO_PATH + "theo.webp"]
  },
  {
    name:"Adultery<br>Hazelnut", handle:"@adultery.hazelnut", age:31, location:"Havenfall, Kingsmere",
    role:"The Driver",
    bio:"Yes, that is my real name. No, I will not laugh at the joke. I'll drive anything anywhere for twenty gold coins.",
    traits:{loyalty:50,selfPreservation:70,trust:35,suspicion:70,autonomy:75,control:40,riskTaking:65,empathy:35,forgiveness:40,revenge:30},
    wants:{autonomy:70,riskTaking:60,trust:50},
    photos:[LC_PHOTO_PATH + "adultery.webp"]
  },
  {
    name:"Philip<br>Hatter", handle:"@philip.hatter", age:24, location:"Havenfall, Kingsmere",
    role:"The Hatter",
    bio:"Hatter by name, sleeper by talent. I'll lean on your hedge, nap through the chaos, and grin when I wake up. Forget me and I will look offended.",
    traits:{loyalty:65,selfPreservation:55,trust:55,suspicion:45,autonomy:60,control:30,riskTaking:65,empathy:55,forgiveness:60,revenge:30},
    wants:{loyalty:70,empathy:60,riskTaking:60},
    photos:[LC_PHOTO_PATH + "philip.webp"]
  }
];