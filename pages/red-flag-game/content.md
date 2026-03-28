<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
    background: linear-gradient(135deg, #2d1b1b 0%, #1a0f0f 100%);
    color: #e0e0e0;
    margin: 0;
    padding: 0;
    min-height: 100vh;
    line-height: 1.5;
}

.container {
    max-width: 700px;
    padding: 20px;
    margin: 0 auto;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

h1 {
    color: #ff4444;
    font-size: 3rem;
    font-weight: 800;
    text-align: center;
    margin: 0 0 0.5rem;
    text-shadow: 0 2px 20px rgba(255, 68, 68, 0.5);
}

h1.green-mode {
    color: #44ff88;
    text-shadow: 0 2px 20px rgba(68, 255, 136, 0.5);
}

.subtitle {
    text-align: center;
    color: #a0a0a0;
    margin-bottom: 3rem;
    font-size: 1.1rem;
}

.flag-card {
    background: rgba(255, 68, 68, 0.1);
    border: 2px solid rgba(255, 68, 68, 0.3);
    border-radius: 20px;
    padding: 3rem 2rem;
    margin-bottom: 2rem;
    text-align: center;
    backdrop-filter: blur(10px);
    min-height: 300px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    transition: all 0.3s;
}

.flag-card.green-mode {
    background: rgba(68, 255, 136, 0.1);
    border: 2px solid rgba(68, 255, 136, 0.3);
}

.flag-emoji {
    font-size: 5rem;
    margin-bottom: 1.5rem;
    animation: wave 2s ease-in-out infinite;
}

@keyframes wave {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(-10deg); }
    75% { transform: rotate(10deg); }
}

.flag-text {
    font-size: 1.8rem;
    font-weight: 700;
    color: #fff;
    line-height: 1.4;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    max-width: 600px;
}

.flag-text.initial {
    font-size: 1.3rem;
    color: #a0a0a0;
    font-weight: 500;
}

.button-group {
    display: flex;
    gap: 1rem;
    width: 100%;
    max-width: 600px;
    margin: 0 auto 1rem;
    flex-wrap: wrap;
    justify-content: center;
}

.generate-button {
    flex: 1;
    min-width: 150px;
    padding: 20px 30px;
    border: none;
    border-radius: 16px;
    background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
    color: white;
    font-size: 1.1rem;
    font-weight: 800;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: 0 8px 30px rgba(255, 68, 68, 0.4);
    text-transform: uppercase;
    letter-spacing: 1px;
}

.generate-button.green {
    background: linear-gradient(135deg, #44ff88 0%, #00cc55 100%);
    box-shadow: 0 8px 30px rgba(68, 255, 136, 0.4);
}

.generate-button.both {
    background: linear-gradient(135deg, #ff4444 0%, #44ff88 100%);
    box-shadow: 0 8px 30px rgba(255, 136, 102, 0.4);
}

.generate-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(255, 68, 68, 0.6);
}

.generate-button.green:hover {
    box-shadow: 0 12px 40px rgba(68, 255, 136, 0.6);
}

.generate-button.both:hover {
    box-shadow: 0 12px 40px rgba(255, 136, 102, 0.6);
}

.generate-button:active {
    transform: translateY(-1px);
}

.counter {
    text-align: center;
    margin-top: 2rem;
    color: #666;
    font-size: 0.9rem;
}

.share-section {
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.share-button {
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
    padding: 12px 24px;
    border: 2px solid rgba(255, 68, 68, 0.3);
    border-radius: 12px;
    background: rgba(255, 68, 68, 0.05);
    color: #ff4444;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
    display: none;
}

.share-button:hover {
    background: rgba(255, 68, 68, 0.15);
    border-color: rgba(255, 68, 68, 0.5);
}

.share-button.visible {
    display: block;
}

@media (max-width: 640px) {
    h1 {
        font-size: 2.2rem;
    }

    .flag-emoji {
        font-size: 4rem;
    }

    .flag-text {
        font-size: 1.4rem;
    }

    .generate-button {
        font-size: 1.1rem;
        padding: 18px 32px;
    }
}
</style>

<html>
<div class="container">
    <h1 id="mainTitle">🚩 Flag Generator</h1>
    <p class="subtitle" id="subtitle">Discover what you're probably ignoring (or celebrating) in your dating life</p>

    <div class="flag-card" id="flagCard">
        <div class="flag-emoji" id="flagEmoji">🚩</div>
        <div class="flag-text initial" id="flagText">
            Click below to reveal a random flag
        </div>
    </div>

    <div class="button-group">
        <button class="generate-button" id="redBtn">Red Flags</button>
        <button class="generate-button green" id="greenBtn">Green Flags</button>
        <button class="generate-button both" id="bothBtn">Both</button>
    </div>

    <div class="share-section">
        <button class="share-button" id="shareBtn">Share This Flag</button>
    </div>

    <div class="counter" id="counter">
        Flags generated: 0
    </div>
</div>

<script>
const RED_FLAGS = [
    // Dating & Relationship Behaviors
    "Still texts their ex 'just to check in'",
    "Has never been single for more than 2 weeks since high school",
    "Calls you crazy for having normal human emotions",
    "Talks about their ex in bed",
    "Says 'I'm brutally honest' but can't handle any criticism",
    "Posts thirst traps while in a relationship with you",
    "Gets jealous when you talk to the waiter",
    "Still has active dating apps 'just for the ego boost'",
    "Compares you to their ex constantly",
    "Says all their exes are crazy",
    "Ghosts you for days then acts like nothing happened",
    "Only texts you after 10pm",
    "Won't let you meet their friends after 6 months",
    "Has you saved in their phone as 'Pizza Place' or something random",
    "Gets mad when you don't respond within 5 minutes",
    "Flirts with others in front of you to make you jealous",
    "Says 'I don't believe in labels' after months of dating",
    "Keeps gifts from their ex on display",
    "Refuses to post you on social media but posts everything else",
    "Says 'if you can't handle me at my worst' unironically",

    // Sexual Red Flags
    "Doesn't wash their hands before sex",
    "Jackhammers for 30 seconds then asks if you came",
    "Tries to initiate anal without asking first",
    "Gets all their sex education from porn",
    "Refuses to reciprocate oral sex",
    "Says 'I don't do foreplay'",
    "Thinks the clitoris is a myth",
    "Only wants sex when they're drunk",
    "Dirty talks like they're reading a bad fanfiction",
    "Treats your body like they're kneading dough",
    "Gets genuinely angry if you don't finish",
    "Asks 'are you done yet?' mid-sex",
    "Thinks missionary with the lights off is kinky",
    "Won't get tested for STIs",
    "Removes the condom without asking",
    "Has never made a partner orgasm and doesn't care",
    "Finishes and immediately rolls over and snores",
    "Keeps comparing your body to porn stars",
    "Refuses to shower before expecting oral",
    "Uses teeth during oral and won't take feedback",

    // Personal Hygiene
    "Only showers when they're going out",
    "Their bedroom smells like a gym bag died",
    "Wears the same underwear multiple days in a row",
    "Has visible crust on their sheets",
    "Doesn't wash their ass properly",
    "Doesn't own a toothbrush",
    "Their car is a biohazard",
    "Has fungal toenails they refuse to treat",
    "Leaves skid marks on the regular",
    "Doesn't wash their hands after using the bathroom",
    "Has a musty smell they think is 'natural musk'",
    "Reuses towels for months without washing",
    "Their breath could kill a plant",
    "Doesn't clean under their nails",
    "Has crusty discharge in their eyes all day",

    // Financial Red Flags
    "Has 6 maxed out credit cards",
    "Gambles away their paycheck",
    "Expects you to pay for everything",
    "Has never filed taxes",
    "Spends rent money on designer clothes",
    "Has an NFT collection they won't shut up about",
    "Joins every MLM scheme they encounter",
    "Borrowed money from you and bought weed with it",
    "Has $50k in student loans for a degree they never finished",
    "Lives with their parents but spends $500/month on Door Dash",
    "Has no savings at age 35",
    "Gets payday loans regularly",
    "Thinks investing means buying lottery tickets",
    "Owes money to dangerous people",
    "Files for bankruptcy every few years like it's a hobby",

    // Social & Communication
    "Is rude to service workers",
    "Doesn't tip",
    "Talks about themselves for 3 hours straight",
    "Interrupts you constantly",
    "One-ups every story you tell",
    "Makes everything a competition",
    "Uses the R-word casually",
    "Says 'no offense but' before something deeply offensive",
    "Trauma dumps on the first date",
    "Doesn't have a single close friend",
    "All their friends are people they want to sleep with",
    "Gives you the silent treatment instead of communicating",
    "Yells during every disagreement",
    "Makes you feel guilty for having boundaries",
    "Never apologizes, just says 'sorry you feel that way'",

    // Technology & Social Media
    "Has anime girls as their profile picture on everything",
    "Comments 'looking good' on every attractive person's posts",
    "Posts vague-booking about your arguments",
    "Has a finsta for thirst trapping",
    "Slides into DMs while dating you",
    "Their camera roll is 90% screenshots of arguments",
    "Tweets their entire life story including your business",
    "Has burner accounts to stalk people",
    "Posts every meal with the caption 'foodie'",
    "Their TikTok is all thirst traps",

    // Work & Career
    "Has been fired from 15 jobs",
    "Thinks working is for suckers",
    "Their 'business' is selling essential oils",
    "Constantly has a new 'startup idea' but never executes",
    "Brags about committing workers comp fraud",
    "Hasn't held a job for more than 3 months",
    "Their career goal is becoming TikTok famous",
    "Calls in sick every Monday",
    "Got fired for stealing and thinks it's funny",
    "Is 40 with no job, no education, and no ambition",

    // Family Dynamics
    "Their mom still does their laundry at age 30",
    "Has never lived outside their parents' house",
    "Mommy picks out their clothes",
    "Lets their mom talk shit about you",
    "Their family is in a cult",
    "Borrows money from elderly relatives and never pays back",
    "Their parents don't know you exist after a year of dating",
    "Chose their mom's side when she insulted you",
    "Expects you to cook like their mother",
    "Has a creepy obsession with a sibling",

    // Mental Health & Emotional
    "Refuses therapy but clearly needs it",
    "Uses their mental illness as an excuse to treat you like shit",
    "Threatens suicide when you try to leave",
    "Goes through your phone while you sleep",
    "Makes burner accounts to spy on you",
    "Punches walls during arguments",
    "Blames all their problems on their ex from 10 years ago",
    "Has untreated paranoia but won't get help",
    "Weaponizes their tears to manipulate you",
    "Says they'll change but never does",

    // Living Situation & Habits
    "Has a piss jug collection",
    "Leaves dishes in the sink until they grow mold",
    "Never cleans the bathroom",
    "Hoards trash in their room",
    "Has bugs in their apartment and won't deal with it",
    "Smokes inside and the walls are yellow",
    "Leaves food out until it rots",
    "Doesn't do laundry until they're out of clothes",
    "Has a mattress on the floor with no sheets",
    "Their place smells like a dumpster",

    // Food & Eating
    "Chews with their mouth open aggressively",
    "Doesn't eat vegetables because they're 'for rabbits'",
    "Only eats chicken nuggets and fries",
    "Talks with a full mouth constantly",
    "Makes sexual noises while eating",
    "Eats your food without asking",
    "Has never cooked a meal in their life",
    "Thinks ketchup is spicy",
    "Refuses to try any new foods",
    "Eats like they're in a competitive eating contest",

    // Past Relationships
    "Has 4 kids with 4 different people",
    "Cheated on everyone they've ever dated",
    "Got engaged 6 times",
    "Still lives with their ex 'for financial reasons'",
    "Has a restraining order from their ex",
    "Fucked your friend before you started dating",
    "Their ex warned you about them",
    "Was caught cheating and blamed you for not being enough",
    "Met you while they were still in a relationship",
    "Has a pregnant ex they're ignoring",

    // Character & Values
    "Lies about small things for no reason",
    "Steals from their workplace",
    "Is cruel to animals",
    "Makes fun of homeless people",
    "Is openly racist/homophobic/transphobic",
    "Thinks age is just a number",
    "Scams elderly people for fun",
    "Laughs at other people's pain",
    "Has zero empathy for anyone",
    "Bullies people online",

    // Extra Harsh & Creative Ones
    "Says they're an alpha male unironically",
    "Listens to Andrew Tate podcasts",
    "Their Spotify playlist is called 'sad boi hours' and it's 47 hours long",
    "Collects katanas but has never trained in martial arts",
    "Wears fedoras and says 'm'lady'",
    "Has a waifu pillow they're emotionally attached to",
    "Their Discord status is always 'Do Not Disturb'",
    "Calls women 'females'",
    "Uses 'sigma male' in their bio",
    "Has a podcast nobody listens to",
    "Thinks they're an entrepreneur but they dropship from AliExpress",
    "Their personality is their Zodiac sign",
    "Believes in hustle culture but doesn't have a job",
    "Chews tobacco and spits in a cup they carry around",
    "Vapes indoors at your place",
    "Their entire personality is weed",
    "Thinks being an asshole is a personality trait",
    "Says 'I'm just built different'",
    "Has a face tattoo of their own name spelled wrong",
    "Their bio says 'CEO of my own life'",

    // More Dating Specific
    "Brings their mom on dates",
    "Asks to split the bill then orders the most expensive thing",
    "Shows up to dates in pajamas",
    "Takes phone calls during dinner",
    "Talks about marriage on the first date",
    "Asks for nudes before knowing your last name",
    "Sends dick pics unrequested",
    "Their opening line is 'hey beautiful wanna fuck'",
    "Shows up drunk to dates",
    "Forgets your name mid-date",

    // Sexual Extended
    "Thinks jackhammering harder will make up for lack of rhythm",
    "Asks 'did you cum?' while you're clearly not having a good time",
    "Their idea of dirty talk is just saying 'fuck' repeatedly",
    "Finishes then says 'your turn' and goes on their phone",
    "Thinks porn moans are real",
    "Tries positions they saw in porn without warming up",
    "Gets performance anxiety then blames you",
    "Can only finish to very specific weird porn",
    "Their sex playlist is Nickelback",
    "Calls it 'making love' every single time",

    // Oddly Specific
    "Collects toenail clippings in a jar",
    "Smells their fingers after scratching anything",
    "Has a concerning amount of taxidermy in their room",
    "Talks to their car like it's a person",
    "Keeps their baby teeth in a box",
    "Still uses a nightlight at age 28",
    "Has a life-sized cardboard cutout of themselves",
    "Names their muscles",
    "Keeps a diary of everyone who wronged them",
    "Has a spreadsheet ranking everyone they've slept with",

    // Modern Dating
    "Has 'entrepreneur' in their bio but works at Subway",
    "Their Instagram is just gym selfies and motivational quotes",
    "Sends 'wyd' at 2am on a Tuesday",
    "Leaves you on read for days then quadruple texts",
    "Their Tinder bio is their height and 'just ask'",
    "Uses outdated photos from when they were 50 pounds lighter",
    "Brings up their ex every 10 minutes",
    "Takes mirror selfies at the gym between sets",
    "Their bio says 'no drama' but they're pure chaos",
    "Ghosts you then comes back months later with 'sorry I was busy'",

    // Personality Flaws
    "Has main character syndrome",
    "Thinks being mean is flirting",
    "Never admits when they're wrong",
    "Gaslights you about things they literally just said",
    "Thinks boundaries are controlling",
    "Pouts when they don't get their way",
    "Gives you the ick on purpose",
    "Tests you constantly",
    "Reads your messages but waits hours to respond to seem busy",
    "Love bombs you then goes cold randomly",

    // Beyond Redemption
    "Has a secret second family",
    "Is wanted in three states",
    "Faked their own death once",
    "Is in a pyramid scheme and trying to recruit you",
    "Stole from a charity",
    "Has been to prison for something they definitely did",
    "Catfished someone for 5 years",
    "Scammed their own grandmother",
    "Is running from child support payments",
    "Has a warrant out for their arrest",

    // Beige Flags (Questionable but not dealbreakers)
    "Claps when the plane lands",
    "Wears socks with sandals unironically",
    "Still uses an iPod Classic",
    "Drinks milk with ice cubes",
    "Eats pizza with a fork and knife",
    "Watches TikToks on full volume in public",
    "Says 'we' when talking about their sports team",
    "Has a favorite parking spot and gets upset if someone takes it",
    "Refers to themselves in third person",
    "Takes their shoes off on airplanes",
    "Microwaves fish at work",
    "Doesn't season their food at all",
    "Uses speaker phone for every call in public",
    "Still quotes Borat",
    "Has strong opinions about fonts",
    "Thinks they're a DJ because they have a Spotify playlist",
    "Wears sunglasses indoors",
    "Brings acoustic guitar to parties",
    "Does voices for all their pets",
    "Collects something weird like hotel key cards",
    "Uses 🤣 emoji unironically",
    "Asks 'is this seat taken?' when it clearly isn't",
    "Says 'living my best life' constantly",
    "Takes photos of every meal for Instagram",
    "Has a very specific morning routine that can't be disrupted",
    "Pronounces it 'expresso'",
    "Walks slow in the middle of the sidewalk",
    "Breathes loudly through their mouth",
    "Hums constantly without realizing",
    "Laughs at their own jokes before the punchline",

    // Traditional/Outdated Views
    "Thinks women belong in the kitchen",
    "Says men shouldn't cry",
    "Believes a man should always pay for everything",
    "Thinks women shouldn't work after marriage",
    "Says 'boys will be boys' to excuse bad behavior",
    "Believes women should always wear makeup",
    "Thinks men can't be raped",
    "Says marriage is only between a man and woman",
    "Believes women who have sex are sluts but men are studs",
    "Thinks a woman's place is taking care of kids",
    "Says real men don't do housework",
    "Believes you need permission from dad to propose",
    "Thinks women shouldn't have male friends",
    "Says wives should obey their husbands",
    "Believes women are too emotional to lead",
    "Thinks asking for consent ruins the mood",
    "Says depression isn't real, just be happy",
    "Believes therapy is for weak people",
    "Thinks participation trophies ruined a generation",
    "Says 'back in my day' about everything",
    "Believes young people are all lazy",
    "Thinks mental illness is just seeking attention",
    "Says women who don't want kids are selfish",
    "Believes men who do yoga are gay",
    "Thinks pink is only for girls",
    "Says real men drink beer, not cocktails",
    "Believes women provoke assault by what they wear",
    "Thinks you can pray away the gay",
    "Says 'it's just a joke' after being offensive",
    "Believes hitting kids is good parenting",

    // Kink & Sexual Compatibility
    "Has a foot fetish but makes it everyone's problem",
    "Wants you to call them daddy but gets mad if you laugh",
    "Into age play but brings it up at family dinner",
    "Has a mommy kink and actually calls you mommy in public",
    "Wants to be dominated but won't communicate what they like",
    "Into pet play but expects you to be their pet 24/7",
    "Has a breeding kink but no desire for actual kids",
    "Lactation fetish and keeps asking when you'll get pregnant",
    "Into financial domination and actually expects you to pay their bills",
    "Has unusual kinks but refuses to discuss boundaries first",
    "Wants threesomes but gets jealous immediately",
    "Into choking but learned everything from porn",
    "Has intense fantasies but won't discuss safety or consent",
    "Wants to try pegging but makes it weird and awkward",
    "Into furry stuff and expects you to participate",
    "Has a vore fetish and won't stop talking about it",
    "Inflation fetish and their entire camera roll is concerning",
    "Into sounding but has no idea about safety",
    "Wants to bring a third but only talks to them, not you",
    "Has a humiliation kink but actually has no self-esteem",
    "Into wax play but uses regular candles not body-safe ones",
    "Wants you to dominate them but doesn't accept any of your rules",
    "Has a cuckold fantasy but would actually be devastated",
    "Into impact play but doesn't believe in aftercare",
    "Has a diaper fetish and leaves them around the house",
    "Wants roleplay scenarios but makes them uncomfortable",
    "Into latex but doesn't clean any of their gear",
    "Has breeding kink and tries to stealth during sex",
    "Wants to do rope bondage but watched one YouTube video",
    "Into blood play with zero understanding of safety",
    "Has a tickle fetish and won't stop even when you're clearly uncomfortable",
    "Wants to do knife play with actual sharp knives",
    "Into water sports but doesn't shower after",
    "Has a clown fetish and owns a full costume",
    "Wants to film everything but won't discuss consent",
    "Into exhibitionism and doesn't care if you're comfortable",
    "Has fantasy scenarios and takes them way too far",
    "Wants to explore power dynamics but skips negotiation",
    "Into orgasm denial but actually just doesn't make you finish",
    "Has a food fetish and wastes so much food",
    "Wants you to wear fursuit in bed",
    "Into electro-play with sketchy Amazon equipment",
    "Has a giantess fetish and won't shut up about it",
    "Wants to explore BDSM but thinks it means abuse",
    "Into primal play but is actually just aggressive",
    "Has a pregnancy fetish but you're both men",
    "Wants to try prostate stuff but is too insecure",
    "Into public play and doesn't care about getting arrested",
    "Has a vampire fetish and actually tries to drink blood",
    "Wants to do master/slave dynamic 24/7 without discussion",

    // More Beige Flags
    "Double dips their chips",
    "Leaves one square of toilet paper on the roll",
    "Doesn't use turn signals",
    "Replies 'K' to long messages",
    "Doesn't put the shopping cart back",
    "Reheats fish in the microwave",
    "Chews ice loudly",
    "Leaves their Bluetooth speaker on in public",
    "Says 'no offense' then says something offensive",
    "Uses 'your' instead of 'you're'",
    "Doesn't pick up their dog's shit",
    "Parks across two spaces",
    "Doesn't say thank you when you hold the door",
    "Takes the last slice without asking",
    "Leaves time on the microwave",
    "Doesn't rerack weights at the gym",
    "Clips their nails in public",
    "Talks during movies",
    "Spoils shows without warning",
    "Stands on the left side of the escalator",
    "Asks 'are you on your period?' when you're annoyed",
    "Says 'calm down' during arguments",
    "Leaves voice memos instead of texting",
    "FaceTimes in public bathrooms",
    "Plays music from their phone without headphones on public transit",
    "Coughs without covering their mouth",
    "Doesn't wash hands after bathroom",
    "Leaves wet towels on the bed",
    "Doesn't close cabinets or drawers",
    "Eats loudly with mouth open",

    // Kink Communication Failures
    "Brings up their kinks at inappropriate times",
    "Shares their fetish with your family at dinner",
    "Posts about kink stuff on main social media",
    "Tries to convert vanilla friends to their lifestyle",
    "Doesn't respect safe words",
    "Pushes boundaries without consent",
    "Kink shames you for your preferences",
    "Expects you to be into everything they're into",
    "Doesn't believe in limits",
    "Gets defensive when you have boundaries",
    "Thinks 50 Shades is an instruction manual",
    "Wants to be your dom but has no idea how",
    "Calls themselves an alpha in bed",
    "Uses kink as an excuse to be abusive",
    "Doesn't understand the difference between BDSM and abuse",

    // Dating App Specific
    "Has 'ask me' for every profile question",
    "All their photos are group shots",
    "Only has photos with sunglasses and hats",
    "Bio is just their Instagram handle",
    "Lists their height in every photo caption",
    "Has 'fluent in sarcasm' in bio",
    "Says 'I don't know why I'm on here'",
    "Only photos are with fish they caught",
    "Every picture has a Snapchat filter",
    "Bio says 'here for a good time not a long time'",
    "Lists 'school of hard knocks' as education",
    "Has 'entrepreneur' but no actual business",
    "Only photos are in their car",
    "Bio is entirely emojis",
    "Has their ex cropped out of every photo",

    // More Kinks & Fetishes
    "Has a balloon fetish and the popping sound makes them cum",
    "Into macrophilia and constantly talks about being crushed",
    "Has a sneeze fetish and films you when you're sick",
    "Armpit fetish and wants to lick them without asking",
    "Into transformation fetish and roleplays turning into furniture",
    "Has a belly button fetish and won't stop poking yours",
    "Objectification kink but treats you like actual furniture outside the bedroom",
    "Into quicksand fetish and shows you videos constantly",
    "Has a medical fetish but uses actual medical equipment wrong",
    "Statue fetish and wants you to freeze mid-activity",
    "Into hypnosis kink but actually thinks they can control minds",
    "Has unusual trigger fetishes and won't stop trying to activate them",
    "Muscle worship but only talks about themselves at the gym",
    "Into feederism and gets upset when you try to eat healthy",
    "Has a burping/farting fetish and encourages it constantly",
    "Inflation fetish taken to dangerous levels with pumps",
    "Into tentacle porn and owns way too many tentacle dildos",
    "Has a giantess fetish and photoshops you crushing cities",
    "Has extreme fetishes but won't discuss safety or boundaries",
    "Into unusual play without proper safety discussions",
    "Has a fart fetish and wants you to fart on command",
    "Pregnancy fetish and fake cries when you get your period",
    "Into insect play and brings actual bugs into bed",
    "Has a hair fetish and steals your hairbrush bristles",
    "Wants extreme bathroom play for real",
    "Into cake sitting and wastes so much food",
    "Has a smoking fetish but you don't smoke",
    "Dental fetish and gets hard at the dentist office",
    "Into controversial roleplay without understanding the issues",
    "Has a hiccup fetish and tries to scare you constantly",
    "Wants sissy play but makes it offensive",
    "Into mind control hypnosis and genuinely thinks it works",
    "Has a mermaid fetish and wants you in a tail 24/7",
    "Has breath control interests with zero safety precautions",
    "Into puppy play but takes it too literally",
    "Has dark fantasies and doesn't understand they should stay fantasy",
    "Wants intense roleplay that crosses comfort lines",
    "Into taboo scenarios without proper discussion",
    "Has a fisting fetish but won't use lube",
    "Wants to do shibari but uses hardware store rope",
    "Into edge play with no safe words or limits",
    "Has a sweat fetish and smells your gym clothes",
    "Lactation kink and tries to induce it without consent",
    "Into breath play alone with no safety",
    "Has a wedgie fetish from childhood",
    "Wants to do knifeplay with actual kitchen knives",
    "Into medical play and bought a speculum off Amazon",
    "Has a vore fetish and their art folder is concerning",
    "Wants you to trample them but doesn't understand weight distribution",
    "Into intense roleplay and makes it way too realistic",
    "Has a robot fetish and wants you to be emotionless",
    "Wants gang bang but gets jealous of everyone there",

    // BDSM Done Wrong
    "Calls themselves a dom but it's just abuse with extra steps",
    "Wants a sub but actually wants a slave with no limits",
    "Does impact play with no warmup or aftercare",
    "Uses 'I'm a dom' to justify controlling behavior outside scenes",
    "Wants TPE but has never discussed it properly",
    "Thinks being a brat means being actually disrespectful",
    "Uses degradation but it's just their real opinion",
    "Wants power exchange but skips all the consent negotiation",
    "Claims to be a master but has never studied BDSM",
    "Punishes for real mistakes not agreed-upon infractions",
    "Wants 24/7 dynamic after one week of dating",
    "Thinks subspace means you consent to anything",
    "Does intense play with zero safety training",
    "Leaves marks in visible places without permission",
    "Uses pain as actual punishment not sensation play",
    "Wants to collar you without understanding the commitment",
    "Does rope bondage but never learned about nerve damage",
    "Thinks aftercare is optional",
    "Wants permanent marks on the first date",
    "Uses degrading language outside negotiated scenes",
    "Demands submission without earning trust",
    "Thinks BDSM means they can do whatever they want",
    "Wants to be worshipped but gives nothing in return",
    "Does wax play with regular candles not body-safe wax",
    "Thinks hard limits are just suggestions",
    "Ignores yellow safewords",
    "Wants intense play with no safety knowledge",
    "Uses bondage but doesn't check circulation",
    "Does temperature play with frozen/boiling items",
    "Wants to do needle play with sewing needles",

    // Kink Compatibility Issues
    "Is vanilla but lies about being kinky to get laid",
    "Kink shames your fetishes while expecting you to do theirs",
    "Only into receiving never giving",
    "Wants you to dominate them but criticizes everything you do",
    "Has a humiliation kink but actually has trauma they haven't processed",
    "Into praise kink but fishing for compliments 24/7",
    "Wants degradation but cries when you do it",
    "Says they're a switch but only ever tops/bottoms",
    "Into roleplay but can't stay in character",
    "Wants rough sex but doesn't communicate what they like",
    "Has fantasies but won't discuss boundaries",
    "Expects you to read their mind about what they want",
    "Says they're experienced but knows nothing about safety",
    "Wants to try everything but has no patience",
    "Into orgasm control but just doesn't make you cum",
    "Has a daddy kink but calls you daddy at Thanksgiving",
    "Wants to be choked but doesn't know safe choking doesn't exist",
    "Into sensation play but only cares about their sensations",
    "Has breeding kink but refuses to wear condoms",
    "Wants to explore poly but just wants to cheat with permission",
    "Into exhibitionism but will actually get you arrested",
    "Has size kink but body shames you",
    "Wants threesomes but has rules only for you not them",
    "Into free use but doesn't grasp consent",
    "Has a degradation kink and calls you slurs without asking",
    "Wants to be your sugar daddy but is actually broke",
    "Into ageplay but makes it creepy not cute",
    "Has corruption kink and targets actual inexperienced people",
    "Wants to film content but won't sign releases",
    "Into findom but it's just financial abuse",

    // Sex Toy Red Flags
    "Uses sex toys but never cleans them",
    "Wants to use their ex's toys on you",
    "Buys the cheapest toys with toxic materials",
    "Uses household items as sex toys unsafely",
    "Shares sex toys without barriers",
    "Stores toys in a gross pile",
    "Uses silicone toys with silicone lube",
    "Wants to use a hitachi magic wand on high immediately",
    "Buys you a toy in their favorite color not yours",
    "Uses numbing lube to avoid communication",
    "Wants to use a cock ring but won't read instructions",
    "Uses butt plugs without flared bases",
    "Wants to use e-stim but bought sketchy equipment",
    "Has a toy collection but they're all crusty",
    "Uses sex furniture but it's falling apart",

    // Communication Red Flags
    "Says 'I don't need to ask, I can tell what you want'",
    "Thinks talking about sex ruins the spontaneity",
    "Gets offended when you give feedback",
    "Assumes porn sex is real sex",
    "Won't discuss STI status before sex",
    "Thinks consent is a mood killer",
    "Says you're overthinking when you want to negotiate",
    "Refuses to tell you what they like",
    "Gets mad when you don't automatically know their preferences",
    "Won't respect your no the first time you say it",
    "Thinks asking for consent means you don't want it",
    "Uses 'blue balls' to guilt you into sex",
    "Says 'if you loved me you would'",
    "Pouts when you're not in the mood",
    "Makes you feel bad for having boundaries"
];

const GREEN_FLAGS = [
    // Sweet Green Flags
    "Remembers small details about things you mentioned weeks ago",
    "Brings you soup when you're sick without being asked",
    "Texts you they got home safe",
    "Asks about your day and actually listens",
    "Respects your boundaries without making it weird",
    "Celebrates your wins like they're their own",
    "Admits when they're wrong and apologizes sincerely",
    "Makes you coffee/tea exactly how you like it",
    "Lets you sleep in and brings you breakfast in bed",
    "Defends you when you're not around",
    "Notices when you're quiet and checks if you're okay",
    "Remembers your allergies without you having to remind them",
    "Keeps your favorite snacks stocked",
    "Watches shows you like even if they're not into them",
    "Holds your hand in public proudly",
    "Introduces you to everyone as their partner with excitement",
    "Supports your hobbies even if they don't understand them",
    "Gives you space when you need it without taking it personally",
    "Remembers important dates (not just birthdays)",
    "Leaves you cute notes randomly",
    "Actually helps with chores without being asked",
    "Plans thoughtful dates, not just dinner and a movie",
    "Compliments you on things beyond your appearance",
    "Makes you laugh when you're stressed",
    "Respects your sleep schedule",
    "Shares the last bite of their favorite food with you",
    "Tells their family and friends about you warmly",
    "Gets excited about your interests",
    "Remembers your comfort order at restaurants",
    "Checks in during the day just because",
    "Actually listens to your feedback and makes changes",
    "Hypes you up to other people",
    "Sends you memes they think you'll like",
    "Comfortable with comfortable silence",
    "Respects your relationship with your family",
    "Makes an effort with your friends",
    "Plans for a future that includes you",
    "Supports your career goals",
    "Doesn't make you feel guilty for having alone time",
    "Shows affection in your love language",
    "Compromises without keeping score",
    "Makes you feel safe, physically and emotionally",
    "Never makes you question if they're into you",
    "Trusts you without being controlling",
    "Communicates openly about feelings",
    "Takes care of you when you're drunk/high",
    "Doesn't hold grudges over small things",
    "Makes you feel like the only person in the room",
    "Surprised you with something you mentioned wanting",
    "Respects your 'no' immediately",

    // Impressive Green Flags
    "Goes to therapy and actually works on themselves",
    "Has close friendships they maintain",
    "Tips service workers generously",
    "Handles conflict maturely without yelling",
    "Takes accountability for their mistakes",
    "Has healthy boundaries with exes",
    "Financially responsible and talks about money openly",
    "Supports your independence",
    "Can cook an actual meal from scratch",
    "Cleans up after themselves without being asked",
    "Handles your emotions with care and patience",
    "Has hobbies and passions outside of you",
    "Encourages you to pursue your goals",
    "Never makes you feel bad for your mental health struggles",
    "Actually changes behavior after you express concerns",
    "Treats service workers with respect",
    "Has a good relationship with their family",
    "Takes 'no' gracefully without pouting",
    "Splits costs fairly or takes turns paying",
    "Communicates their needs clearly",
    "Validates your feelings even when they don't understand",
    "Has dealt with their trauma in healthy ways",
    "Respects your career as much as their own",
    "Can admit 'I don't know' instead of making things up",
    "Actually reads books (not just says they do)",
    "Maintains good hygiene consistently",
    "Has follow-through on promises",
    "Shows up when they say they will",
    "Can handle constructive criticism",
    "Apologizes to service workers when wrong",
    "Doesn't need to be drunk to be affectionate",
    "Respects all your identities",
    "Actively anti-racist/anti-bigotry",
    "Believes and supports survivors",
    "Votes and stays politically informed",
    "Checks their privilege",
    "Listens to feedback about being offensive",
    "Calls out their friends' bad behavior",
    "Financially independent",
    "Has a passport and uses it",
    "Reads the news beyond headlines",
    "Can navigate conflict without running away",
    "Makes major decisions together with you",
    "Respects your pronouns and corrects others",
    "Knows how to genuinely apologize (no 'but')",
    "Takes initiative in planning and household tasks",
    "Has emotional intelligence",
    "Can regulate their emotions",
    "Understands consent is enthusiastic and ongoing",
    "Makes you feel heard and valued",

    // Wild/Exotic Green Flags
    "Willing to try new foods and cuisines",
    "Down for spontaneous adventures",
    "Has a valid passport and wants to use it",
    "Can handle spicy food",
    "Knows how to parallel park",
    "Has taken a solo trip before",
    "Can name all 50 states",
    "Knows basic first aid/CPR",
    "Has changed a tire before",
    "Can swim and isn't afraid of the ocean",
    "Comfortable camping/being in nature",
    "Has been to therapy and recommends it",
    "Knows how to use tools/fix basic things",
    "Can handle bugs without freaking out",
    "Has a skincare routine",
    "Drinks water regularly",
    "Actually uses sunscreen",
    "Can dance and doesn't care who's watching",
    "Speaks multiple languages",
    "Has traveled solo internationally",
    "Can read a map without GPS",
    "Knows how to start a fire (safely)",
    "Has done psychedelics responsibly",
    "Comfortable with karaoke",
    "Can drive stick shift",
    "Has gone skinny dipping",
    "Down for road trips with no fixed plan",
    "Comfortable being naked around you",
    "Has interesting stories from past adventures",
    "Will try your weird food combinations",
    "Can handle their alcohol",
    "Has done something that scared them",
    "Comfortable with public speaking",
    "Has performed or done stand-up",
    "Can handle rollercoasters",
    "Has been in a mosh pit",
    "Knows how to surf/ski/skate",
    "Has jumped off something high into water",
    "Comfortable with their sexuality",
    "Has gone to music festivals",
    "Can pitch a tent",
    "Has been backpacking",
    "Comfortable with nudist beaches",
    "Has done an open mic night",
    "Can shotgun a beer",
    "Has done karaoke sober",
    "Willing to try new kinks/explore sexually",
    "Has definedpersonal boundaries and kinks",
    "Communicates desires clearly in bed",
    "Enthusiastic about foreplay",
    "Asks what you like sexually",
    "Wants you to orgasm as much as they do",
    "Comfortable talking about sex",
    "Has invested in quality sex toys",
    "Believes in aftercare",
    "Knows that consent is sexy",
    "Can take sexual feedback without ego",
    "Has read actual books about sex",
    "Understands anatomy (including the clitoris)",
    "Gets tested for STIs regularly",
    "Carries condoms and doesn't complain about using them",
    "Open to trying new positions",
    "Doesn't shame your kinks or fantasies",
    "Makes sex fun and playful, not just serious",
    "Can laugh during sex when things get awkward",
    "Initiates in creative ways",
    "Pays attention to your body language",
    "Respects your boundaries during sex",
    "Wants to learn what makes you feel good",
    "Doesn't treat porn as a manual",
    "Understands sex isn't just penetration",
    "Actually enjoys giving oral",
    "Has a safeword and respects it",
    "Checks in during intense moments",
    "Can separate kink from real life",
    "Understands aftercare is important",
    "Has researched safe BDSM practices",
    "Respects hard limits without questioning",
    "Communicates their limits clearly too",
    "Knows the difference between BDSM and abuse",
    "Takes your pleasure seriously",
    "Doesn't finish and immediately ignore you",
    "Willing to experiment but respects 'no'",
    "Can handle toys without feeling threatened",
    "Understands that lube is essential",
    "Knows that bigger isn't always better",
    "Communicates when something doesn't feel good",
    "Can be dominant OR submissive depending on mood",
    "Respects that you're not always in the mood",
    "Makes you feel sexy and desired",
    "Puts effort into seduction",
    "Understands sexual compatibility matters",
    "Willing to explore your fantasies",
    "Has their own fantasies they share",
    "Knows that sex changes and evolves in relationships",
    "Doesn't pressure you into anything",
    "Makes STI testing a normal conversation",
    "Actually knows where the clit is",
    "Understands that 'no' can happen at any point",
    "Respects your body autonomy completely",
    "Makes you feel comfortable being vulnerable",
];

let currentFlag = null;
let flagCount = 0;
let currentMode = 'red'; // 'red', 'green', or 'both'

const flagText = document.getElementById('flagText');
const redBtn = document.getElementById('redBtn');
const greenBtn = document.getElementById('greenBtn');
const bothBtn = document.getElementById('bothBtn');
const shareBtn = document.getElementById('shareBtn');
const counter = document.getElementById('counter');
const mainTitle = document.getElementById('mainTitle');
const subtitle = document.getElementById('subtitle');
const flagCard = document.getElementById('flagCard');
const flagEmoji = document.getElementById('flagEmoji');

function generateFlag(mode) {
    currentMode = mode;
    let selectedFlag;
    let isGreen;

    if (mode === 'red') {
        const randomIndex = Math.floor(Math.random() * RED_FLAGS.length);
        selectedFlag = RED_FLAGS[randomIndex];
        isGreen = false;
    } else if (mode === 'green') {
        const randomIndex = Math.floor(Math.random() * GREEN_FLAGS.length);
        selectedFlag = GREEN_FLAGS[randomIndex];
        isGreen = true;
    } else { // both
        const useGreen = Math.random() > 0.5;
        if (useGreen) {
            const randomIndex = Math.floor(Math.random() * GREEN_FLAGS.length);
            selectedFlag = GREEN_FLAGS[randomIndex];
            isGreen = true;
        } else {
            const randomIndex = Math.floor(Math.random() * RED_FLAGS.length);
            selectedFlag = RED_FLAGS[randomIndex];
            isGreen = false;
        }
    }

    currentFlag = selectedFlag;

    // Update UI based on flag type
    if (isGreen) {
        flagCard.classList.add('green-mode');
        mainTitle.classList.add('green-mode');
        flagEmoji.textContent = '✅';
        flagText.textContent = selectedFlag;
    } else {
        flagCard.classList.remove('green-mode');
        mainTitle.classList.remove('green-mode');
        flagEmoji.textContent = '🚩';
        flagText.textContent = selectedFlag;
    }

    flagText.classList.remove('initial');
    shareBtn.classList.add('visible');

    // Update counter
    flagCount++;
    counter.textContent = `Flags generated: ${flagCount}`;

    // Small animation
    flagCard.style.transform = 'scale(0.98)';
    setTimeout(() => {
        flagCard.style.transform = 'scale(1)';
    }, 100);
}

function shareFlag() {
    if (!currentFlag) return;

    const isGreen = flagCard.classList.contains('green-mode');
    const flagType = isGreen ? '✅ Green Flag' : '🚩 Red Flag';
    const shareText = `${flagType}: ${currentFlag}`;

    if (navigator.share) {
        navigator.share({
            title: 'Flag Generator',
            text: shareText,
            url: window.location.href
        }).catch(() => {
            // Fallback to clipboard
            copyToClipboard(shareText);
        });
    } else {
        copyToClipboard(shareText);
    }
}

function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            shareBtn.textContent = '✓ Copied to Clipboard!';
            setTimeout(() => {
                shareBtn.textContent = 'Share This Flag';
            }, 2000);
        });
    }
}

redBtn.addEventListener('click', () => generateFlag('red'));
greenBtn.addEventListener('click', () => generateFlag('green'));
bothBtn.addEventListener('click', () => generateFlag('both'));
shareBtn.addEventListener('click', shareFlag);
</script>
</html>
