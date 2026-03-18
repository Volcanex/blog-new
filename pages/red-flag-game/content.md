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

.generate-button {
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
    padding: 20px 40px;
    border: none;
    border-radius: 16px;
    background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
    color: white;
    font-size: 1.3rem;
    font-weight: 800;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: 0 8px 30px rgba(255, 68, 68, 0.4);
    text-transform: uppercase;
    letter-spacing: 1px;
}

.generate-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(255, 68, 68, 0.6);
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
    <h1>🚩 Red Flag Generator</h1>
    <p class="subtitle">Discover what you're probably ignoring in your dating life</p>

    <div class="flag-card" id="flagCard">
        <div class="flag-emoji">🚩</div>
        <div class="flag-text initial" id="flagText">
            Click below to reveal a random red flag
        </div>
    </div>

    <button class="generate-button" id="generateBtn">Generate Red Flag</button>

    <div class="share-section">
        <button class="share-button" id="shareBtn">Share This Red Flag</button>
    </div>

    <div class="counter" id="counter">
        Red flags generated: 0
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
    "Into age play but doesn't understand boundaries",
    "Has a mommy kink and actually calls you mommy in public",
    "Wants to be dominated but won't communicate what they like",
    "Into pet play but expects you to be their pet 24/7",
    "Has a breeding kink but no desire for actual kids",
    "Lactation fetish and keeps asking when you'll get pregnant",
    "Into financial domination and actually expects you to pay their bills",
    "Has a piss kink and doesn't ask first",
    "Wants threesomes but gets jealous immediately",
    "Into choking but learned everything from porn",
    "Has a rape fantasy but doesn't understand consent negotiation",
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
    "Wants you to pretend to be their step-sibling during sex",
    "Into latex but doesn't clean any of their gear",
    "Has an impregnation kink and pokes holes in condoms",
    "Wants to do rope bondage but watched one YouTube video",
    "Into blood play with zero understanding of safety",
    "Has a tickle fetish and won't stop even when you're clearly uncomfortable",
    "Wants to do knife play with actual sharp knives",
    "Into water sports but doesn't shower after",
    "Has a clown fetish and owns a full costume",
    "Wants to film everything but won't discuss consent",
    "Into exhibitionism and doesn't care if you're comfortable",
    "Has a teacher/student fantasy and takes it way too far",
    "Wants to do consensual non-consent but skips the negotiation",
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
    "Has a sneezing fetish and pepper-sprays you to trigger it",
    "Muscle worship but only talks about themselves at the gym",
    "Into feederism and gets upset when you try to eat healthy",
    "Has a burping/farting fetish and encourages it constantly",
    "Inflation fetish taken to dangerous levels with pumps",
    "Into tentacle porn and owns way too many tentacle dildos",
    "Has a giantess fetish and photoshops you crushing cities",
    "Vomit fetish and tries to trigger your gag reflex",
    "Into scat play without proper safety discussions",
    "Has a fart fetish and wants you to fart on command",
    "Pregnancy fetish and fake cries when you get your period",
    "Into insect play and brings actual bugs into bed",
    "Has a hair fetish and steals your hairbrush bristles",
    "Wants to be a human toilet for real",
    "Into cake sitting and wastes so much food",
    "Has a smoking fetish but you don't smoke",
    "Dental fetish and gets hard at the dentist office",
    "Into race play with zero understanding of why it's problematic",
    "Has a hiccup fetish and tries to scare you constantly",
    "Wants to be turned into a sissy but makes it transphobic",
    "Into mind control hypnosis and genuinely thinks it works",
    "Has a mermaid fetish and wants you in a tail 24/7",
    "Drowning fetish with zero safety precautions",
    "Into puppy play but shits on the floor",
    "Has a snuff fantasy and doesn't understand it should stay fantasy",
    "Wants extreme age gap roleplay that's way too realistic",
    "Into raceplay and says actually racist shit",
    "Has a fisting fetish but won't use lube",
    "Wants to do shibari but uses hardware store rope",
    "Into edge play with no safe words or limits",
    "Has a sweat fetish and smells your gym clothes",
    "Lactation kink and tries to induce it without consent",
    "Into erotic asphyxiation alone with no safety",
    "Has a wedgie fetish from childhood",
    "Wants to do knifeplay with actual kitchen knives",
    "Into medical play and bought a speculum off Amazon",
    "Has a vore fetish and their art folder is concerning",
    "Wants you to trample them but doesn't understand weight distribution",
    "Into necro roleplay and makes it way too realistic",
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
    "Wants CNC but skips all the consent negotiation",
    "Claims to be a master but has never studied BDSM",
    "Punishes for real mistakes not agreed-upon infractions",
    "Wants 24/7 dynamic after one week of dating",
    "Thinks subspace means you consent to anything",
    "Does breath play with zero safety training",
    "Leaves marks in visible places without permission",
    "Uses pain as actual punishment not sensation play",
    "Wants to collar you without understanding the commitment",
    "Does rope bondage but never learned about nerve damage",
    "Thinks aftercare is optional",
    "Wants to brand you on the first date",
    "Uses degrading language outside negotiated scenes",
    "Demands submission without earning trust",
    "Thinks BDSM means they can hit you whenever",
    "Wants to be worshipped but gives nothing in return",
    "Does wax play with regular candles not body-safe wax",
    "Thinks hard limits are just suggestions",
    "Ignores yellow safewords",
    "Wants blood play with no bloodborne pathogen knowledge",
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

let currentFlag = null;
let flagCount = 0;

const flagText = document.getElementById('flagText');
const generateBtn = document.getElementById('generateBtn');
const shareBtn = document.getElementById('shareBtn');
const counter = document.getElementById('counter');

function generateFlag() {
    // Get random flag
    const randomIndex = Math.floor(Math.random() * RED_FLAGS.length);
    currentFlag = RED_FLAGS[randomIndex];

    // Update display
    flagText.textContent = currentFlag;
    flagText.classList.remove('initial');

    // Show share button
    shareBtn.classList.add('visible');

    // Update counter
    flagCount++;
    counter.textContent = `Red flags generated: ${flagCount}`;

    // Small animation
    const card = document.getElementById('flagCard');
    card.style.transform = 'scale(0.98)';
    setTimeout(() => {
        card.style.transform = 'scale(1)';
    }, 100);
}

function shareFlag() {
    if (!currentFlag) return;

    const shareText = `🚩 Red Flag: ${currentFlag}`;

    if (navigator.share) {
        navigator.share({
            title: 'Red Flag Generator',
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
                shareBtn.textContent = 'Share This Red Flag';
            }, 2000);
        });
    }
}

generateBtn.addEventListener('click', generateFlag);
shareBtn.addEventListener('click', shareFlag);
</script>
</html>
