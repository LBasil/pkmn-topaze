# Corrections de pronoms / lore autour des champions (suite de rewrite_gyms.py)
import re
exec(open('docs/topaze/rewrite_gyms.py').read().split('# ---------- 1. PYROPIA')[0])
sub('CeruleanCity_Gym',[("She won't lose to someone like you!","He won't lose to someone like you!")])
sub('SaffronCity_Gym',[('but she has earned my respect.','but he has earned my respect.'),
  ("NOX is young, but she's also","NOX is young, but he's also"),("You won't reach her easily!","You won't reach him easily!")])
sub('FuchsiaCity_Gym',[("ACHLYS might appear close, but he's","ACHLYS might appear close, but she's"),("to reach him.","to reach her.")])
sub('VermilionCity_Gym',[
 ("When I was in the Army, HERA\\n","I trained on the peaks with HERA.\\n"),
 ("was my strict CO.\\p","She was my strict teacher.\\p"),
 ("He was a hard taskmaster.","She was a hard taskmaster."),
 ("HERA was always famous for\\n","HERA was always famous for\\n"),
 ("his cautious nature in the Army.","her cautious nature up in the cold."),
 ("HERA said he hid door","HERA said she hid door"),
 ("the GYM himself.","the GYM herself."),
 ("He set up double locks everywhere.","She set up double locks everywhere.")])
sub('CinnabarIsland_Gym',[("The hotheaded EDDIE is a FIRE\\n","The hotheaded EDDIE is an ELECTRIC\\n"),
 ("Douse his spirits with water!\\p","Ground-types shrug off his shocks!\\p"),
 ("BURN HEALS, too.","PARALYZ HEALS, too."),("You beat that firebrand!","You beat that live wire!")])
sub('Route4',[("BOULDERBADGE","PYROPE BADGE"),("KAY is cool. He's not just tough.","KAY is cool. She's not just tough."),
 ("People like and respect him.","People like and respect her."),("like him.$","like her.$")])
sub('CeladonCity_GameCorner',[("She is a user of GRASS-type\\n","She is a user of ICE-type\\n"),
 ("POKéMON, and at one with nature.","POKéMON, and at one with the snow."),
 ("She might appear docile because of\\n","She might appear docile because of\\n"),("her flower arranging…","her quiet manner…")])
