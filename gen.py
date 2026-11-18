#!/usr/bin/env python3
import html, os, sys, tempfile, subprocess, math
from collections import Counter
sys.path.append('/usr/lib/python3/dist-packages')
from PIL import ImageFont
SANS='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; SERIF='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
PAPER,INK,RED,GREY,WHITE='#f7f3e8','#161616','#8f1d1d','#7d7668','#ffffff'
C={'Europe':'#2f5d8a','Middle East':'#8a3a2f','Asia':'#b07a1e','Americas':'#4a6b3a','Africa':'#7a4a6b','Oceania':'#2f6b6b','Global':'#4a4a55'}
CARDS=[('Middle East','IRAN WAR','Kuwait and Bahrain intercept Iranian drones'),('Asia','APEC SHENZHEN','Xi greets Trump as APEC opens'),('Americas','US POLITICS','Democrats pick Jeffries as House speaker'),('Europe','UKRAINE WAR','Russia fires 141 drones at Ukraine'),('Middle East','GAZA','Board of Peace warns the truce may collapse'),('Asia','DISASTER','Cyclone Akvan nears Andhra Pradesh'),('Global','CLIMATE','COP31: 75 countries back the 35x35 power goal'),('Asia','LABOUR','Bangladesh garment protests shut 55 factories'),('Africa','SUDAN WAR','Amnesty: RSF drone strikes killed 37 in El Obeid'),('Global','CULTURE','GTA VI goes on sale after 13 years'),('Europe','ECONOMY','UK inflation rises to 3.6%, a one-year high'),('Global','SPACE','Voyager 1 is one light-day from Earth'),('Europe','UKRAINE AID','EU proposes a 45bn euro loan for Ukraine')]
BRIEFS=[('Middle East','Tehran','Iran says it downed a US MQ-9 near Hormuz'),('Middle East','Riyadh','the coalition downs a Houthi cruise missile'),('Middle East','Jerusalem','the Knesset approves nine deputy speakers'),('Asia','Manila','Trump hails a trade deal; Manila says none was signed'),('Asia','Seoul',"Lee seeks China's help for peace on the peninsula"),('Asia','Tokyo','Japan posts a sixth straight monthly trade deficit'),('Asia','Lahore',"the world's most polluted big city again, AQI 339"),('Asia','Kuala Lumpur','the ringgit hits a five-month low'),('Asia','Shenzhen','Xi and Lee conclude FTA services talks'),('Asia','Bangkok','a Chinese director is jailed over a collapsed tower'),('Asia','Singapore','Princess Aiko makes the first imperial visit in 20 years'),('Asia','Seoul','a court acquits the Daegu mayor in a martial-law case'),('Asia','Kashmir','a LeT militant is killed in the Kulgam siege'),('Asia','Naypyidaw',"Myanmar's leader is reconsidering ASEAN ties"),('Asia','Da Nang','Russian Tu-95 bombers are parked at Da Nang'),('Europe','Berlin','the coalition will cut the power tax and cap fuel prices'),('Europe','Germany','Berlin accuses Russia of chemical-weapons breaches'),('Europe','Cambridge','"human" is named word of the year'),('Europe','Sofia','a sunk LPG tanker was hit by projectiles'),('Europe','The Hague','the ICJ sets its Rohingya genocide ruling for Thursday'),('Americas','Washington',"the Fed's minutes signal more hikes; gold falls under $3,800"),('Americas','New York','the Dow falls 0.8 percent; Nvidia shares fall 2.4 percent'),('Americas','San Francisco','Anthropic is set to price its IPO; trading starts Thursday'),('Americas','California','Waymo halts freeway rides after a state ban'),('Americas','Washington','the NSA confirms an outage on a classified network'),('Americas','Ottawa','Carney says China trade is no worry for Trump'),('Americas','Lima','Peru declares a fuel-supply emergency over El Nino'),('Africa','Kinshasa',"the WHO keeps DR Congo's Ebola outbreak a global emergency"),('Africa','Addis Ababa','Ethiopia and Eritrea mass troops on the border'),('Africa','Johannesburg',"South Africa's inflation rises to 5.2 percent"),('Africa','Cape Town','SA Rugby seeks a full hearing on the Erasmus ban'),('Oceania','Sydney','Tame Impala sweeps the ARIA Awards')]
LEDGER=[]
def measure(s,p,z): return ImageFont.truetype(p,round(z*64)).getlength(str(s))/64
def fit(text,font_path,size,max_width):
 if measure(text,font_path,size)<=max_width:return text
 a=text.split()
 while a:
  t=' '.join(a)+'…'
  if measure(t,font_path,size)<=max_width:return t
  a.pop()
 return '…'
def T(s,x,y,z,p=SANS,fill=INK,anchor='',box=None,extra=''):
 if box is not None:s=fit(str(s),p,z,box);LEDGER.append((s,measure(s,p,z),box))
 fam={SANS:'DejaVu Sans',BOLD:'DejaVu Sans',SERIF:'DejaVu Serif'}[p]; wt=' font-weight="700"' if p!=SANS else ''
 return f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{z}" fill="{fill}"{wt}'+(f' text-anchor="{anchor}"' if anchor else '')+f' {extra}>{html.escape(str(s))}</text>'
def R(x,y,w,h,c,rx=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}"/>'
def P(points,c):return f'<polygon points="{points}" fill="{c}"/>'
def O(x,y,r,c):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
def wrap(s,p,z,w,n):
 out=[];q=''
 for word in s.split():
  t=(q+' '+word).strip()
  if q and measure(t,p,z)>w:out.append(q);q=word
  else:q=t
 if q:out.append(q)
 if len(out)>n:out=out[:n];out[-1]=fit(' '.join(out[-1:]),p,z,w) if not out[-1] else fit(out[-1]+'…',p,z,w)
 return out[:n]
def scene(n,x,y,w,h,c):
 X=lambda q:x+w*q/100;Y=lambda q:y+h*q/100
 z=R(x,y,w,h,PAPER)
 # Each icon is a story-specific, fill-only pictogram; only routes may be stroked.
 if n in (1,4,9):
  z+=P(f'{X(12)},{Y(18)} {X(25)},{Y(25)} {X(12)},{Y(32)}',INK)+P(f'{X(64)},{Y(22)} {X(77)},{Y(29)} {X(64)},{Y(36)}',INK)
  z+=P(f'{X(0)},{Y(78)} {X(25)},{Y(58)} {X(52)},{Y(78)} {X(75)},{Y(61)} {X(100)},{Y(78)} {X(100)},{Y(100)} {X(0)},{Y(100)}',c)
  if n==1:z+=R(X(58),Y(70),w*.32,h*.13,INK)+P(f'{X(49)},{Y(42)} {X(54)},{Y(52)} {X(65)},{Y(49)} {X(59)},{Y(59)} {X(67)},{Y(68)} {X(56)},{Y(63)} {X(49)},{Y(72)} {X(51)},{Y(60)} {X(40)},{Y(55)} {X(52)},{Y(54)}',WHITE)
  elif n==4:z+=P(f'{X(43)},{Y(91)} {X(50)},{Y(43)} {X(58)},{Y(91)}',INK)+R(X(72),Y(66),w*.22,h*.25,INK)
  else:z+=O(X(23),Y(72),h*.13,INK)+O(X(48),Y(72),h*.13,INK)+R(X(73),Y(31),w*.17,h*.45,WHITE)+O(X(86),Y(70),h*.12,c)
  z+=f'<path d="M{X(20)} {Y(31)} Q{X(43)} {Y(52)} {X(65)} {Y(37)}" fill="none" stroke="{c}" stroke-width="2.5" stroke-dasharray="5 5"/>'
 elif n==2:z+=R(X(35),Y(68),w*.3,h*.16,c)+R(X(6),Y(8),w*.2,h*.28,c)+R(X(74),Y(8),w*.2,h*.28,c)+O(X(32),Y(43),h*.09,INK)+O(X(68),Y(43),h*.09,INK)+P(f'{X(24)},{Y(68)} {X(28)},{Y(51)} {X(36)},{Y(51)} {X(46)},{Y(68)}',INK)+P(f'{X(54)},{Y(68)} {X(64)},{Y(51)} {X(72)},{Y(51)} {X(76)},{Y(68)}',INK)+R(X(44),Y(54),w*.12,h*.07,WHITE)
 elif n==3:z+=P(f'{X(5)},{Y(77)} {X(12)},{Y(48)} {X(28)},{Y(17)} {X(45)},{Y(48)} {X(51)},{Y(77)}',c)+R(X(11),Y(48),w*.34,h*.29,INK)+R(X(59),Y(25),w*.08,h*.48,c)+P(f'{X(53)},{Y(28)} {X(70)},{Y(15)} {X(76)},{Y(24)} {X(59)},{Y(38)}',INK)+R(X(75),Y(57),w*.2,h*.14,c)
 elif n==5:z+=R(X(7),Y(12),w*.38,h*.7,c)+R(X(57),Y(12),w*.36,h*.7,c)+P(f'{X(44)},{Y(12)} {X(53)},{Y(33)} {X(45)},{Y(49)} {X(57)},{Y(64)} {X(48)},{Y(82)}',INK)+P(f'{X(18)},{Y(75)} {X(42)},{Y(48)} {X(67)},{Y(32)} {X(49)},{Y(56)}',WHITE)+P(f'{X(72)},{Y(76)} {X(83)},{Y(52)} {X(94)},{Y(76)}',INK)
 elif n==6:z+=O(X(34),Y(42),h*.31,c)+O(X(34),Y(42),h*.19,PAPER)+O(X(40),Y(38),h*.07,INK)+P(f'{X(0)},{Y(77)} {X(14)},{Y(62)} {X(29)},{Y(77)} {X(44)},{Y(62)} {X(59)},{Y(77)} {X(74)},{Y(62)} {X(100)},{Y(80)} {X(100)},{Y(100)} {X(0)},{Y(100)}',c)+R(X(76),Y(54),w*.17,h*.29,INK)+P(f'{X(72)},{Y(55)} {X(84)},{Y(42)} {X(97)},{Y(55)}',WHITE)
 elif n==7:z+=O(X(23),Y(49),h*.3,c)+P(f'{X(4)},{Y(43)} {X(18)},{Y(35)} {X(29)},{Y(46)} {X(43)},{Y(39)} {X(43)},{Y(54)} {X(23)},{Y(59)} {X(10)},{Y(53)}',WHITE)+R(X(56),Y(36),w*.025,h*.49,INK)+P(f'{X(57)},{Y(37)} {X(48)},{Y(16)} {X(59)},{Y(31)} {X(73)},{Y(19)}',c)+R(X(82),Y(17),w*.055,h*.52,WHITE)+O(X(85),Y(73),h*.09,RED)+O(X(93),Y(18),h*.1,c)
 elif n==8:z+=R(X(4),Y(38),w*.43,h*.49,c)+P(f'{X(4)},{Y(38)} {X(16)},{Y(22)} {X(16)},{Y(38)} {X(29)},{Y(22)} {X(29)},{Y(38)}',INK)+R(X(15),Y(57),w*.24,h*.3,INK)+R(X(52),Y(17),w*.35,h*.2,c)+R(X(53),Y(16),w*.025,h*.5,INK)+R(X(85),Y(16),w*.025,h*.5,INK)+''.join(O(X(q),Y(72),h*.06,INK)+R(X(q-2),Y(78),w*.04,h*.14,c) for q in (58,70,82,94))
 elif n==10:z+=P(f'{X(7)},{Y(70)} {X(15)},{Y(35)} {X(28)},{Y(25)} {X(47)},{Y(25)} {X(60)},{Y(35)} {X(68)},{Y(70)} {X(58)},{Y(82)} {X(48)},{Y(67)} {X(27)},{Y(67)} {X(17)},{Y(82)}',c)+R(X(24),Y(45),w*.15,h*.05,INK)+R(X(29),Y(40),w*.05,h*.15,INK)+O(X(50),Y(43),h*.045,INK)+O(X(57),Y(52),h*.045,INK)+O(X(83),Y(38),h*.2,WHITE)+R(X(82),Y(20),w*.025,h*.2,INK)+R(X(83),Y(37),w*.1,h*.035,INK)
 elif n==11:z+=R(X(8),Y(15),w*.28,h*.67,c)+R(X(14),Y(23),w*.16,h*.18,WHITE)+R(X(31),Y(27),w*.05,h*.44,INK)+O(X(36),Y(70),h*.07,INK)+P(f'{X(50)},{Y(80)} {X(70)},{Y(42)} {X(78)},{Y(54)} {X(93)},{Y(20)} {X(88)},{Y(55)} {X(77)},{Y(50)}',RED)+R(X(72),Y(67),w*.21,h*.17,c)
 elif n==12:z+=O(X(31),Y(38),h*.11,c)+P(f'{X(31)},{Y(38)} {X(12)},{Y(17)} {X(44)},{Y(31)}',INK)+R(X(28),Y(38),w*.06,h*.35,INK)+R(X(9),Y(67),w*.39,h*.06,c)+O(X(87),Y(74),h*.13,c)+f'<path d="M{X(47)} {Y(52)} Q{X(65)} {Y(73)} {X(77)} {Y(68)}" fill="none" stroke="{c}" stroke-width="2.5" stroke-dasharray="4 5"/>'
 else:z+=O(X(20),Y(43),h*.29,c)+''.join(O(X(20+17*math.cos(k*math.pi/6)),Y(43)+17*math.sin(k*math.pi/6),1.5,WHITE) for k in range(12))+R(X(64),Y(14),w*.27,h*.44,'#2f5d8a')+R(X(64),Y(36),w*.27,h*.22,'#b07a1e')+P(f'{X(43)},{Y(69)} {X(58)},{Y(55)} {X(70)},{Y(62)} {X(83)},{Y(50)} {X(95)},{Y(57)} {X(83)},{Y(65)} {X(70)},{Y(70)} {X(57)},{Y(63)}',INK)
 return z
def dotmap():
 try:rows=open('/tmp/mask.txt').read().splitlines()
 except OSError:rows=[]
 z=''.join(O(40+xx*2.8,666+yy*1.75,.7,GREY) for yy,row in enumerate(rows[:45]) for xx,ch in enumerate(row[:90]) if ch=='#')
 pins=[(200,683),(238,692),(91,685),(174,673),(211,686),(249,705),(145,690),(224,700),(168,715),(286,726),(152,669),(58,699),(184,677)]
 for n,(x,y) in enumerate(pins,1):z+=O(x,y,5.2,RED)+T(n,x,y+2.3,6.2,BOLD,WHITE,'middle',8)
 return z
def svg():
 LEDGER.clear();o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024">{R(0,0,1024,1024,PAPER)}<path d="M40 12H984M40 34H984" stroke="{INK}" stroke-width=".8"/>',T("THE WORLD'S NEWS IN ONE PICTURE",40,27,10.5,SANS,INK,box=400),T('45 STORIES · 7 REGIONS · 13 ILLUSTRATED · ALL FROM WEDNESDAY',984,27,10.5,BOLD,RED,'end',560)]
 # This fixed text length keeps the year inside the right margin (40 + 944 = 984).
 o += [f'<text x="40" y="96" font-family="DejaVu Serif" font-weight="700" font-size="58" fill="{INK}" textLength="944" lengthAdjust="spacingAndGlyphs">Wednesday 18 November 2026</text>',f'<path d="M40 112H984" stroke="{INK}" stroke-width=".8"/>']
 counts=Counter(a for a,_,_ in CARDS+BRIEFS); order=sorted(C,key=lambda a:(-counts[a],list(C).index(a)));x=40
 for i,a in enumerate(order):
  w=944*counts[a]/45 if i<6 else 984-x;o += [R(x,120,w,28,C[a]),T(f'{a.upper()} {counts[a]}',x+w/2,138,10.5,BOLD,WHITE,'middle',w-8)];x+=w
 ticker=[('55','factories shut'),('141','drones fired at Ukraine'),('37','killed in El Obeid'),('3.6%','UK inflation'),('204,070','ready to evacuate'),('11,300','Ebola cases')]
 gap=12; total=sum(measure(a,BOLD,9.4)+4+measure(b,SANS,9.4) for a,b in ticker)+gap*5
 assert total<=944
 tx=40
 for i,(figure,label) in enumerate(ticker):
  fw=measure(figure,BOLD,9.4);lw=measure(label,SANS,9.4)
  o += [T(figure,tx,160,9.4,BOLD,RED,box=fw+.1),T(label,tx+fw+4,160,9.4,SANS,INK,box=lw+.1)]
  tx+=fw+4+lw
  if i<5:o.append(f'<path d="M{tx+gap/2} 151V163" stroke="{GREY}" stroke-width=".6"/>');tx+=gap
 pos=[(32+i*315,180,306,92) for i in range(3)]+[(32+i*189,340,180,86) for i in range(5)]+[(32+i*189,500,180,86) for i in range(5)]
 for n,((reg,kick,head),(x,y,w,ih)) in enumerate(zip(CARDS,pos),1):
  o += [f'<rect x="{x}" y="{y}" width="{w}" height="150" fill="none" stroke="{GREY}" stroke-width=".8"/>',scene(n,x,y,w,ih,C[reg]),R(x,y+ih,w,14,C[reg]),T(kick,x+5,y+ih+10.5,8.5,BOLD,WHITE,box=w-10)]
  hs=17 if n<4 else 13
  for j,line in enumerate(wrap(head,SERIF,hs,w-16,2)):o.append(T(line,x+8,y+ih+14+hs+j*hs*1.15,hs,SERIF,INK,box=w-16))
  o += [R(x,y,16,16,RED),T(n,x+8,y+11.5,9.5,BOLD,WHITE,'middle',14)]
 o += [T('WHERE IT HAPPENED',40,656,8.5,BOLD,INK,box=300),dotmap(),R(356,660,628,100,WHITE),R(356,660,3,100,RED)]
 date="DATE CHECK  Left out because first reported before 18 November: Nvidia's $115.8bn quarter, the Prague train crash, Mongolia's president resigning. Every story here happened or was first reported on Wednesday 18 November 2026; contested claims are attributed."
 for j,line in enumerate(wrap(date,SANS,8.6,607,3)):o.append(T(line,369,681+j*16,8.6,BOLD if j==0 else SANS,INK,box=607))
 o += [T('ALSO ON WEDNESDAY 18 NOVEMBER',40,780,10.5,BOLD,RED,box=500,extra='letter-spacing="1"'),f'<path d="M40 788H984" stroke="{INK}" stroke-width=".8"/>']
 for num,(reg,place,desc) in enumerate(BRIEFS,14):
  k=num-14;col=k//11;row=k%11;x=40+col*323;y=804+row*15.4;nw=measure(str(num)+' ',BOLD,9.2);pw=measure(place+' ',BOLD,9.2)
  o += [T(str(num)+' ',x,y,9.2,BOLD,RED,box=nw+.1),T(place+' ',x+nw,y,9.2,BOLD,INK,box=pw+.1),T(desc,x+nw+pw,y,9.2,SANS,INK,box=297-nw-pw),f'<path d="M{x} {y+4}H{x+297}" stroke="{GREY}" stroke-opacity=".15" stroke-width=".7"/>']
 o += [f'<path d="M40 964H984" stroke="{INK}" stroke-width=".8"/>',T('Every story happened or was first reported on 18 November 2026. Sources: Reuters, AP, AFP, BBC, Al Jazeera. Original flat-vector illustrations.',40,982,8.4,SANS,INK,box=790),T('18 NOVEMBER 2026',984,982,8.4,BOLD,INK,'end',150),'</svg>']
 worst=max((w/b for _,w,b in LEDGER),default=0); item=max(LEDGER,key=lambda q:q[1]/q[2]);print(f'worst ratio: {worst:.4f} ({item[0]})');assert worst<=1
 return ''.join(o)
def main():
 out=sys.argv[1] if len(sys.argv)>1 else 'entry.png'
 with tempfile.NamedTemporaryFile(suffix='.svg',delete=False) as f:f.write(svg().encode());name=f.name
 try:subprocess.run(['rsvg-convert','-w','1024','-h','1024','-o',out,name],check=True)
 finally:os.unlink(name)
if __name__=='__main__':main()
