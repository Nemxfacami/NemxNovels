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

{
  id: 'OA-0492',
  name: 'Unknown Love Tattoo',
  price: 890,
  category: 'Artifact',
  availability: 'Limited',
  condition: 'New',
  image: 'OA-0492.webp',
  origin: 'The <i>Unknown Love Tattoo</i> is an anomalous tattoo attributed exclusively to <b>Dan Donalds</b>, a tattooist whose whereabouts are unknown. Unlike ordinary tattoos, the mark cannot be purchased as a physical item. Upon purchase, Donalds will locate the buyer personally and apply the tattoo himself. Once applied, the tattoo causes any person the wearer specifically asks Donalds to mark with it to develop an immediate and permanent romantic attachment to the wearer. The affected individual remains completely devoted to the wearer and appears to remain under their influence indefinitely. The tattoo cannot be removed through conventional means. If the affected person loses the limb on which the tattoo was placed, the mark will subsequently appear on another part of their body. More concerningly, death does not appear to terminate the effect. Individuals who die while affected by the tattoo reportedly remain in love with the wearer even after death, with several accounts claiming that the attachment persists in the form of a <i>spiritual presence</i>. Donalds is known to possess numerous other anomalous tattoos, although <i>Unknown Love Tattoo</i> is reportedly the only one he currently offers for sale due to its comparatively mild consequences and lack of <b>severe physical side effects</b>.'
},
{
  id: 'OA-0493',
  name: '3 Wishes Jinn',
  price: 1250,
  category: 'Relic',
  availability: 'Available',
  condition: 'Unknown',
  image: 'OA-0493.webp',
  origin: 'The <i>3 Wishes Jinn</i> is believed to be an ancient entity imprisoned within a concealed cavern somewhere in the <b>Dothmodon Wild Desert</b>. The circumstances surrounding his imprisonment, as well as the identity of those responsible, remain unknown. Unlike most entities listed within Occult Arcana, the Jinn is not transported to the buyer. Instead, upon purchase, the buyer is reportedly <i>magically transported directly into the cave</i> where the Jinn remains imprisoned. Once there, the Jinn will grant the visitor <b>three wishes</b>. The nature and limitations of these wishes have never been fully documented, as no reliable account exists detailing what happens after all three wishes have been granted. Buyers are advised to consider their wording carefully.'
},
{
  id: 'OA-0494',
  name: 'Diogenes',
  price: 'After the Job',
  category: 'Assassin',
  availability: 'Available',
  condition: 'Unknown',
  image: 'OA-0494.webp',
  origin: '<i>Diogenes</i> is a well-known assassin whose reputation extends far beyond the living world. For the right price, he will <b>take care of anyone</b> the buyer names, regardless of where that individual may be found—even in <i>Hell</i>. His methods, identity, and means of crossing between realms remain unknown. Diogenes is also capable of carrying out contracts against beings residing in <b>Heaven</b>, although such assignments come with an unusual condition. Following a successful contract in Heaven, Diogenes requires <b>ten months to recover his holiness</b> before he is willing to accept another heavenly assignment. His fee is never stated in advance. Buyers are informed that the <i>price is determined after the job</i>.'
},
{
  id: 'OA-0495',
  name: 'Love Potion',
  price: 12000,
  category: 'Potion',
  availability: 'In Stock',
  condition: 'New',
  image: 'OA-0495.webp',
  origin: 'The <i>Love Potion</i> is a proprietary product manufactured by the <b>Sosadium Company</b> in <b>Havenfall</b>. Only a single drop is required to produce its intended effect. Whoever consumes the potion will develop genuine romantic feelings toward the person who administered it, although the effect does not cause <i>obsession</i> when used in the recommended quantity. Administering more than a single drop may produce significantly stronger and less predictable results. The potion may also be diluted in any other liquid without reducing its effectiveness; a diluted serving containing the equivalent of <b>one drop</b> produces the same outcome as a single undiluted drop. <b>Warning:</b> The potion must only be administered orally. Do not pour or apply it directly onto the skin, as the effects of dermal exposure remain undocumented.'
},
{
  id: 'OA-0496',
  name: 'Necklace of Cylus',
  price: 11000,
  category: 'Relic',
  availability: 'Unavailable',
  condition: 'Used',
  image: 'OA-0496.webp',
  origin: 'The <i>Necklace of Cylus</i> is an anomalous necklace capable of compelling another person to carry out <b>any task specified by its wearer</b>. Once the command has been completed, the affected individual immediately returns to their normal state and appears to have no lasting awareness of the influence exerted upon them. The artifact is subject to one particularly dangerous limitation: if the commanded task is <i>physically or otherwise impossible for the individual to accomplish</i>, the person will die rather than resist the command. For this reason, all instructions must be achievable within a period of <b>one month or less</b>. The precise origin of the necklace and the identity of <b>Cylus</b> remain unknown.'
},
{
  id: 'OA-0497',
  name: 'Invitation Card',
  price: 3000,
  category: 'Artifact',
  availability: 'Limited',
  condition: 'Unknown',
  image: 'OA-0497.webp',
  origin: 'The <i>Invitation Card</i> was discovered deep within a forest during an <b>anaconda hunting expedition</b> conducted by <b>Rodrigo Marinez</b>. The circumstances surrounding its presence in the forest remain unexplained, and no information regarding its intended recipient or purpose has been recovered. It remains uncertain whether the card possesses any supernatural properties at all. Despite this, its existence has attracted the attention of numerous <i>wizards and occult practitioners</i>, many of whom are reportedly interested in acquiring one for themselves. Rodrigo, however, has repeatedly expressed his desire to <b>never have the card in his possession</b>, although the reason for this reluctance remains undisclosed.'
},

{
  id: 'OA-0498',
  name: 'Second Heart',
  price: 7000,
  category: 'Relic',
  availability: 'Limited',
  condition: 'New',
  image: 'OA-0498.webp',
  origin: 'The <i>Second Heart</i> was reportedly recovered from an <b>Anunnaki</b> specimen believed to have possessed three functioning hearts. The circumstances under which the specimen was discovered, as well as the identity of those responsible for recovering the organ, remain undocumented. According to the records accompanying the artifact, implantation of the Second Heart into a human host can dramatically extend the recipient’s lifespan. Those who successfully undergo the procedure are said to live for an <b>additional 2,000 years</b> beyond the normal human lifespan. The procedure itself carries no listed charge, with the <i>surgery provided free of charge</i> to any approved buyer. The long-term effects of possessing two hearts, however, remain insufficiently documented.'
},
{
  id: 'OA-0499',
  name: 'Key of Doors',
  price: 15000,
  category: 'Artifact',
  availability: 'Limited',
  condition: 'Unknown',
  image: 'OA-0499.webp',
  origin: 'The <i>Key of Doors</i> is an unidentified artifact capable of opening <b>any door</b>, regardless of its lock, material, location, or apparent purpose. What lies beyond the door, however, is rarely what the user should expect. Rather than simply unlocking the intended destination, the key can cause a door to open into <i>another location entirely</i>. All known destinations appear to exist within the <b>present time</b>; the key does not appear to permit travel into the past or future. Reports describe doors opening into distant cities, abandoned buildings, private residences, remote wilderness, underground chambers, and locations that should be physically inaccessible from the door being opened. The destination appears to be determined by unknown conditions, and there is currently no reliable method of selecting where a particular door will lead. A door opened with the key will function normally once opened, but closing and reopening it may produce an entirely different destination. Several attempts to document its destinations have ended with the investigators being unable to locate their original entry point. The <i>Key of Doors</i> has no known manufacturer, owner, or recorded date of origin.'
},
{
  id: 'OA-0500',
  name: 'Hell Escape Card',
  price: 55000,
  category: 'Artifact',
  availability: 'Limited',
  condition: 'Unknown',
  image: 'OA-0500.webp',
  origin: 'The <i>Hell Escape Card</i> is an unidentified artifact whose creator and original purpose remain completely unknown. The card was not discovered, purchased, or recovered through any documented expedition. Instead, <b>Occult Arcana</b> received it unexpectedly, having found the card placed directly at the organization’s entrance as an apparent <i>gift from an unknown sender</i>. No individual has claimed responsibility for delivering it, and no reliable record exists of how the card reached the location without being detected. The card contains no visible markings identifying its creator, although its name has led researchers to believe that it may possess some connection to <b>Hell</b> or provide a means of escaping it. Whether this interpretation is accurate remains unconfirmed. Occult Arcana has been unable to determine how the card works, who it was intended for, or why it was left at their door. Its true function remains classified as <i>unknown</i>.'
},
{
  id: 'OA-0501',
  name: 'Naughty John Joy',
  price: 9000,
  category: 'Device',
  availability: 'In Stock',
  condition: 'New',
  image: 'OA-0501.webp',
  origin: 'The <i>Naughty John Joy</i> is an anomalous adult device reportedly manufactured by an unidentified company within the <b>adult toy industry</b>. The device is produced in multiple sizes and is designed exclusively for male users. Unlike conventional products of its kind, the object appears to be <i>biologically alive</i>, although its exact biological composition remains unknown. Its primary function appears to be the extraction and collection of <b>semen</b> from its user rather than blood or other bodily fluids. The device has shown no confirmed purpose beyond this function, and its method of operation remains poorly understood. The identity of the company responsible for manufacturing it has not yet been discovered, and <b>Occult Arcana researchers are still attempting to trace its origin</b>.'
},
{
  id: 'OA-0502',
  name: 'Milkanum',
  price: 200,
  category: 'Food',
  availability: 'In Stock',
  condition: 'New',
  image: 'OA-0502.webp',
  origin: 'The <i>Milkanum</i> is, according to all available examinations, simply <b>ordinary milk</b>. No unusual properties, anomalous effects, or unexplained ingredients have been identified. Despite this, the product has somehow found its way into the <i>Occult Arcana</i> catalogue and is currently being offered for sale. Researchers remain uncertain why the item was submitted in the first place, although several have suggested that its apparent normality may itself be worth investigating.'
},
{
  id: 'OA-0503',
  name: 'Depresso Tea',
  price: 400,
  category: 'Potion',
  availability: 'In Stock',
  condition: 'New',
  image: 'OA-0503.webp',
  origin: 'The <i>Depresso Tea</i> is an anomalous beverage with an unusually simple reported effect. Anyone who consumes it is said to experience a complete and <b>permanent relief from depression</b>. According to available accounts, the effect does not gradually diminish, nor can the condition reportedly return after consumption. The mechanism responsible for this effect remains unknown, and no reliable explanation has been established for how an ordinary-looking tea could produce such a profound psychological change. Despite its apparent effectiveness, <i>Depresso Tea</i> remains classified as an anomalous substance, with further testing currently restricted.'
},
{
  id: 'OA-0504',
  name: 'Skull of Roth',
  price: 5000,
  category: 'Relic',
  availability: 'Limited',
  condition: 'Unknown',
  image: 'OA-0504.webp',
  origin: 'The <i>Skull of Roth</i> was recovered from an ancient <b>pyramid</b> whose location has never been publicly disclosed. The identity of Roth, and the circumstances that led to the skull being placed within the structure, remain unknown. The artifact appears to possess no unusual properties until it is held directly by a living individual. If the holder speaks the phrase <b>"Rothacus Rathanos El&#39; Yelim"</b>, the skull reportedly induces a vivid vision depicting the user&#39;s <i>future life</i>. The duration and accuracy of these visions vary between individuals, and it remains unclear whether the scenes represent a predetermined future or merely one possible outcome. Attempts to repeat the ritual immediately after receiving a vision have produced inconsistent results. Occult Arcana has been unable to determine who originally created the ritual or what the name <i>Roth</i> refers to.'
},
{
  id: 'OA-0505',
  name: 'Clone Seeds',
  price: 23000,
  category: 'Artifact',
  availability: 'In Stock',
  condition: 'New',
  image: 'OA-0505.webp',
  origin: 'The <i>Clone Seeds</i> are a bio-anomalous product developed by the <b>Sosadium Company</b>. To activate a seed, it must be planted in soil and kept completely free of conventional water. Instead, the planted seed must be exposed to <b>urine three times a day</b>. Under these conditions, the plant will reportedly reach full maturity in less than a month. Once fully grown, the plant produces a single human clone corresponding to the individual who cultivated it. The resulting clone is said to be an almost exact biological duplicate of its source, although the long-term stability of the clone remains undocumented. Sosadium has provided no public explanation for how the seed acquires the biological information necessary to produce a human duplicate.'
},
{
  id: 'OA-0506',
  name: 'Womenslator',
  price: 12000,
  category: 'Device',
  availability: 'In Stock',
  condition: 'New',
  image: 'OA-0506.webp',
  origin: 'The <i>Womenslator</i> is a proprietary device developed by <b>Davenport</b> and designed to interpret the emotional and cognitive states of female subjects. When activated, the device reportedly translates not only the subject’s spoken words but also provides the user with information regarding <b>what she is thinking and the exact emotions she is experiencing</b> at the time. The device does not appear to require the subject’s cooperation, and its readings are presented directly to the user in an easily understandable form. Davenport has released no information regarding the technology behind the device, leaving researchers uncertain whether it relies on advanced psychological analysis, anomalous perception, or something considerably stranger.'
},
{
  id: 'OA-0507',
  name: 'No Scars Razor',
  price: 3000,
  category: 'Artifact',
  availability: 'Limited',
  condition: 'Unknown',
  image: 'OA-0507.webp',
  origin: 'The <i>No Scars Razor</i> was recovered from a crime scene where a person was found dead in a large pool of blood. Strangely, the body showed <b>no visible scars or wounds</b>, despite the amount of blood surrounding it. The razor was taken into Occult Arcana custody for examination. When used to cut a person, the blade causes normal bleeding, but approximately <b>10 minutes after the injury is inflicted, the wound completely closes</b>. No scar, mark, or other evidence of the injury remains. The exact mechanism behind the healing effect is unknown, as is the identity of the person who originally owned the razor.'
},
{
  id: 'OA-0508',
  name: 'Idiot Virus',
  price: 19000,
  category: 'Biological Artifact',
  availability: 'Limited',
  condition: 'New',
  image: 'OA-0508.webp',
  origin: 'The <i>Idiot Virus</i> was recovered from an abandoned scientist bunker in <i>Helen&#39;s Fields</i>. The bunker contained numerous abandoned experiments, but the most concerning discovery was a syringe containing an unidentified biological agent. When the syringe was opened, airborne particles escaped into the surrounding air. Anyone who inhaled the particles reportedly experienced a severe and permanent decline in cognitive ability, becoming unable to properly learn, retain knowledge, or acquire new information. <b>Once affected, the condition appears to be irreversible.</b> The original scientist responsible for the experiment, as well as the intended purpose of the virus, remains unknown.'
},
{
  id: 'OA-0509',
  name: 'Time Travelling Watch',
  price: 21000,
  category: 'Artifact',
  availability: 'Limited',
  condition: 'New',
  image: 'OA-0509.webp',
  origin: 'The <i>Time Travelling Watch</i> was discovered on the wrist of a corpse found in the <i>Hobo Alleys</i> of Southern Ravenport. The body showed no obvious explanation for how the watch came into its possession. Whoever wears it can send their <b>soul and consciousness to any point in time</b>, while retaining all memories and knowledge from their original life. However, the wearer cannot take their physical body with them. Their consciousness instead arrives within the body of another person living in that period. The original body remains behind, empty of its occupant. Returning to the living is considerably more complicated: the wearer must either convince another person to put on the watch, allowing the consciousness to return, or <b>take possession of another person&#39;s body</b>. How the watch determines its destination, and what happened to its previous owner, remain unknown.'
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