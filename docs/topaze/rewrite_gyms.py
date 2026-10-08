# Réécrit les textes des 8 champions de Topaze (noms, types, badges, CT) à la place de ceux de Kanto.
import re,textwrap,os
R='data/maps/'
def wrap(par,w=33):
    return textwrap.wrap(par,w,break_long_words=False,break_on_hyphens=False)
def build(text):
    """text: paragraphes séparés par une ligne vide ; retourne le bloc .string"""
    pages=[]
    for par in text.strip().split('\n\n'):
        par=' '.join(par.split())
        lines=wrap(par)
        for i in range(0,len(lines),2): pages.append(lines[i:i+2])
    out=[]
    for pi,pg in enumerate(pages):
        for li,l in enumerate(pg):
            last=(pi==len(pages)-1 and li==len(pg)-1)
            sep='$' if last else ('\\p' if li==len(pg)-1 else '\\n')
            out.append('    .string "%s%s"'%(l,sep))
    return '\n'.join(out)
def setlabel(f,label,text=None,raw=None):
    p=R+f+'/text.inc'; s=open(p).read()
    m=re.search(r'^%s::\n(?:    \.string.*\n|\t\.string.*\n)+'%re.escape(f+'_Text_'+label),s,re.M)
    assert m,(f,label)
    body=raw if raw is not None else build(text)
    s=s[:m.start()]+'%s_Text_%s::\n%s\n'%(f,label,body)+s[m.end():]
    open(p,'w').write(s)
def sub(f,pairs,fn='text.inc'):
    p=R+f+'/'+fn; s=open(p).read()
    for a,b in pairs:
        assert a in s,(f,a); s=s.replace(a,b)
    open(p,'w').write(s)
BAD='{PAUSE_MUSIC}{PLAY_BGM}{MUS_OBTAIN_BADGE}{PAUSE 0xFE}{PAUSE 0x56}{RESUME_MUSIC}'

# ---------- 1. PYROPIA : KAY (Feu) ----------
g='PewterCity_Gym'
setlabel(g,'BrockIntro','''So, you made it through OPANIHRUM and the forest. I'm KAY, LEADER of PYROPIA GYM.

This town sleeps on a volcano. Heat, pressure, patience... that is how we live, and that is how my POKéMON fight.

They are all FIRE-type! Since the AURA changed everything ten years ago, even ordinary flames burn differently.

If you think you can take the heat, come on. Show me your best!{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}''')
setlabel(g,'BrockDefeat',raw='''    .string "Hah... I was burning too bright\\n"
    .string "and you stayed calm. Fair enough.\\p"
    .string "Take the PYROPE BADGE.\\p"
    .string "{FONT_NORMAL}{PLAYER} received the PYROPE BADGE\\n"
    .string "from KAY!%s\\p"
    .string "{FONT_MALE}The PYROPE BADGE makes your\\n"
    .string "POKéMON more powerful.\\p"
    .string "It also lets you use FLASH outside\\n"
    .string "of battle, if you carry the HM.$"'''%BAD)
setlabel(g,'ExplainTM39','''TM35 contains FLAMETHROWER.

A reliable stream of fire that may burn the target. Keep it for a POKéMON that can really use it.''')
setlabel(g,'BrockPostBattle','''Someone broke into the GRENALUX MUSEUM and took the GRENAT gem, I heard. TEAM ONYBRIS, they call themselves.

They say POKé BALLS are chains. Maybe so. But a chain you choose and a chain someone forces on you are not the same thing.

Go on to TOURMALIA. SYLVESTRE will not go easy on you.''')
setlabel(g,'LiamIntro','''Stop right there, kid!

You are ten thousand light-years from facing KAY!''')
setlabel(g,'LiamPostBattle','''You're pretty hot.
...But not as hot as KAY!''')
sub(g,[('LEADER: BROCK','LEADER: KAY')])
sub('PewterCity',[('LEADER: BROCK','LEADER: KAY'),('The Rock-Solid POKéMON TRAINER!','The Volcano Keeper!')])
sub('PewterCity',[("But PYROPIA GYM's BROCK isn't like","But PYROPIA GYM's KAY isn't like"),
  ("BROCK's looking for new","KAY is looking for new"),("go take on BROCK!","go take on KAY!")])
sub(g,[('ITEM_TM39','ITEM_TM35')],'scripts.inc')

# ---------- 2. TOURMALIA : SYLVESTRE (Insecte/Plante) ----------
g='CeruleanCity_Gym'
setlabel(g,'MistyIntro','''Welcome to TOURMALIA GYM. I'm SYLVESTRE.

Forests hide a lot of things: spores, silk, stingers and roots that grip your ankles. My BUG and GRASS POKéMON learned it all from the woods.

You came a long way to lose, but I'll admit I like the nerve. Let's see what you've got!''')
setlabel(g,'MistyDefeat','''Well. That was a clean cut.

Fine. Take the TOURMALINE BADGE, you earned it.''')
setlabel(g,'ExplainCascadeBadge','''The TOURMALINE BADGE makes all POKéMON up to Lv. 30 obey.

That includes even outsiders you got in trades.

You can also use CUT anytime, out of battle, if you carry the HM. It clears small trees from your way.

Take my favorite TM too.''')
setlabel(g,'ExplainTM03','''TM19 contains GIGA DRAIN.

It saps the foe and heals you for half the damage. The forest way of fighting.''')
p=R+g+'/scripts.inc'; s=open(p).read(); s=s.replace('ITEM_TM03','ITEM_TM19'); open(p,'w').write(s)
setlabel(g,'GymGuyAdvice','''Yo! Champ in the making!

The LEADER, SYLVESTRE, uses BUG and GRASS-type POKéMON.

FIRE is great against both, FLYING hits bugs hard, and POISON is good against plants. ICE works too!''')
sub('CeruleanCity',[('LEADER: MISTY','LEADER: SYLVESTRE'),('The Tomboyish Mermaid!','The Warden of the Forest!')])

# ---------- 3. APATIA : HERA (Dragon/Vol) ----------
g='VermilionCity_Gym'
setlabel(g,'LtSurgeIntro','''I am HERA, LEADER of APATIA GYM, up here where the air is thin.

Only those who can stand the cold and the wind reach this high. My DRAGON and FLYING POKéMON were born for it.

Show me you can handle the altitude. Hit me with everything you've got!''')
setlabel(g,'LtSurgeDefeat','''Hah! You flew right through my guard.

I respect that. Take the APATITE BADGE!''')
setlabel(g,'ExplainThunderBadgeTakeThis','''The APATITE BADGE lets your POKéMON use FLY out of battle, if you carry the HM.

It also makes your POKéMON faster.

Take this too!''')
setlabel(g,'ExplainTM34','''TM02 contains DRAGON CLAW.

A savage slash that suits any POKéMON with real talons.''')
setlabel(g,'LtSurgePostBattle','''The mountain says what the sea doesn't: those with the strongest will stay in the air.

Keep climbing, kid. BOURG QUARTZ is next, and it's very cold there. Dress warmly.''')
setlabel(g,'GymGuyAdvice','''Yo, champ!

HERA uses DRAGON and FLYING POKéMON. Cold hurts her a lot: ICE is super effective on both types.

ROCK and FAIRY hurt too. ELECTRIC works on the FLYING ones, but DRAGONS shrug it off.''')
p=R+g+'/scripts.inc'; s=open(p).read(); s=s.replace('ITEM_TM34','ITEM_TM02'); open(p,'w').write(s)
sub('VermilionCity',[('LEADER: LT. SURGE','LEADER: HERA'),('The Lightning American!','The Queen of the Peaks!')])

# ---------- 4. BOURG QUARTZ : GRIM (Glace) ----------
g='CeladonCity_Gym'
setlabel(g,'ErikaIntro','''...Oh. A challenger. I am GRIM.

BOURG QUARTZ is quiet under the snow. My ICE POKéMON like it that way, and so do I.

Do not be fooled by the silence. A blizzard is only calm until it moves.

Come, then.''')
setlabel(g,'ErikaDefeat','''...Thawed out, have I?

You are strong. I concede. Take the QUARTZ BADGE.''')
setlabel(g,'ExplainRainbowBadgeTakeThis','''The QUARTZ BADGE makes POKéMON up to Lv. 50 obey.

It also lets POKéMON use STRENGTH in and out of battle, if you carry the HM.

Please also take this with you.''')
setlabel(g,'ExplainTM19','''TM13 contains ICE BEAM.

It freezes slowly, but surely. I find that suits me.''')
setlabel(g,'ErikaPostBattle','''The cold keeps old memories fresh. ONYBRIS... I have heard what they ask of the world.

I understand the dream. I do not forgive the way.

Go on. AMETHIOLITE is waiting.''')
p=R+g+'/scripts.inc'; s=open(p).read(); s=s.replace('ITEM_TM19','ITEM_TM13'); open(p,'w').write(s)
sub('CeladonCity',[('LEADER: ERIKA','LEADER: GRIM'),('The Nature-Loving Princess!','The Frozen Recluse!')])

# ---------- 5. AMETHIOLITE : ACHLYS (Poison) ----------
g='FuchsiaCity_Gym'
setlabel(g,'KogaIntro','''Welcome to AMETHIOLITE GYM. I am ACHLYS.

Venom is not cruelty. It is patience. A little, then a little more, and the fight is already won.

My POKéMON are POISON-types, like the violet mist of this town. Do you have the nerve to breathe it?

Let us begin!''')
setlabel(g,'KogaDefeat','''Hm. You cleaned the toxin out of your own team. Impressive.

Here. Take the AMETHYST BADGE.''')
setlabel(g,'KogaExplainSoulBadge','''Now that you have the AMETHYST BADGE, the DEFENSE of your POKéMON rises.

It also lets you SURF outside of battle, if you carry the HM.

Ah! Take this, too!''')
setlabel(g,'KogaExplainTM06','''TM06 contains TOXIC.

It poisons the foe and gets worse every turn. Poison, as I said, is patience.''')
setlabel(g,'KogaPostBattle','''The AURA twisted us all... but poison stayed poison. Some things hold.

You are ready for HEMATOWN. Its LEADER hides in the dark. Keep your eyes sharp.''')
sub('FuchsiaCity',[('LEADER: KOGA','LEADER: ACHLYS'),('The Poisonous Ninja Master','The Violet Venom Witch!')])

# ---------- 6. HEMATOWN : NOX (Ténèbre) ----------
g='SaffronCity_Gym'
setlabel(g,'SabrinaIntro','''You find your way here in the dark, challenger. Good.

I am NOX. HEMATOWN never sees the sun, and neither do my DARK POKéMON.

They hide, they steal, they strike where you do not look. Let me show you!''')
setlabel(g,'SabrinaDefeat','''So you can fight what you cannot see.

Take the HEMATITE BADGE.''')
setlabel(g,'ExplainMarshBadgeTakeThis','''The HEMATITE BADGE makes your POKéMON obey up to Lv. 70.

It also lets you use ROCK SMASH outside of battle, if you carry the HM.

Take this too.''')
setlabel(g,'ExplainTM04','''TM46 contains THIEF.

It snatches the foe's item. That is rude. But effective.''')
setlabel(g,'SabrinaPostBattle','''Light fades when too many people want it.

There is one more LEADER before the road ends. And a certain wish still floating out there.''')
p=R+g+'/scripts.inc'; s=open(p).read(); s=s.replace('ITEM_TM04','ITEM_TM46'); open(p,'w').write(s)
sub('SaffronCity',[('LEADER: SABRINA','LEADER: NOX'),('The Master of PSYCHIC POKéMON!','The Shadow of the City!')])

# ---------- 7. CHRONDROLIA : EDDIE (Électrique) ----------
g='CinnabarIsland_Gym'
setlabel(g,'BlaineIntro','''Hah! Welcome to CHRONDROLIA GYM!

I am EDDIE, and I am wired! My ELECTRIC POKéMON light up this whole yellow city.

Before you get to them, answer my quiz or beat my trainers! Either way, you will feel the shock!

Come on, let's turn up the voltage!''')
setlabel(g,'BlaineDefeat','''Whoa! You short-circuited me!

That was a good fight! Take the TOPAZ BADGE!''')
setlabel(g,'FireBlastIsUltimateFireMove','''TM24 contains THUNDERBOLT.

The ultimate sparky move. It may even paralyze the target!''')
setlabel(g,'ExplainVolcanoBadge','''The TOPAZ BADGE makes your POKéMON obey up to Lv. 90.

It also lets you use WATERFALL, if you carry the HM.

Here, you can have this, too!''')
setlabel(g,'BlainePostBattle','''Hah! That was electric!

You are nearly at the top. OPANIHRUM's LEADER is back, and she is not one to bend easily.''')
p=R+g+'/scripts.inc'; s=open(p).read(); s=s.replace('ITEM_TM38','ITEM_TM24'); open(p,'w').write(s)
sub('CinnabarIsland',[('LEADER: BLAINE','LEADER: EDDIE')])

# ---------- 8. OPANIHRUM : HEPHA (Acier) ----------
g='ViridianCity_Gym'
setlabel(g,'GiovanniIntro','''So the gate opens at last. I am HEPHA.

I forge my own steel. It does not rust, it does not bend, and it does not forget.

My POKéMON are STEEL-types, born in the black opal furnaces under this city.

Do you think you can break what I made? Come and try!''')
setlabel(g,'GiovanniDefeat','''Hmph... A crack. Just one.

You are the first to leave one in a long while. Take the OPAL BADGE.''')
setlabel(g,'ExplainEarthBadgeTakeThis','''The OPAL BADGE makes every POKéMON obey, regardless of level.

It is the last stone on your road to the POKéMON LEAGUE.

Take this, too.''')
setlabel(g,'ExplainTM26','''TM47 contains STEEL WING.

A strong, fast strike. Honest metal.''')
setlabel(g,'GiovanniPostBattle','''All eight stones are in your hands, or soon will be.

Remember what the opal teaches: the darker it is, the more colors it hides.

The LEAGUE awaits.''')
p=R+g+'/scripts.inc'; s=open(p).read(); s=s.replace('ITEM_TM26','ITEM_TM47'); open(p,'w').write(s)

# ---------- CT recues ----------
for g,old,new,who in [('PewterCity_Gym','TM39','TM35','KAY'),('CeruleanCity_Gym','TM03','TM19','SYLVESTRE'),('VermilionCity_Gym','TM34','TM02','HERA'),
    ('CeladonCity_Gym','TM19','TM13','GRIM'),('SaffronCity_Gym','TM04','TM46','NOX'),('CinnabarIsland_Gym','TM38','TM24','EDDIE'),('ViridianCity_Gym','TM26','TM47','HEPHA')]:
    p=R+g+'/text.inc'; t=open(p).read(); t=t.replace('{PLAYER} received '+old,'{PLAYER} received '+new); open(p,'w').write(t)
# ---------- noms des badges ----------
p='src/strings.c'; s=open(p).read()
for a,b in [('BOULDER','PYROPE'),('CASCADE','TOURMALINE'),('THUNDER','APATITE'),('RAINBOW','QUARTZ'),('SOUL','AMETHYST'),('MARSH','HEMATITE'),('VOLCANO','TOPAZ'),('EARTH','OPAL')]:
    s=s.replace('_("%sBADGE")'%a,'_("%s BADGE")'%b)
open(p,'w').write(s)
