#!/usr/bin/env python3
import html, os, sys, tempfile, subprocess, math
from collections import Counter
sys.path.append('/usr/lib/python3/dist-packages')
from PIL import ImageFont
SANS='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; SERIF='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
PAPER,INK,RED,GREY,WHITE='#f7f3e8','#161616','#8f1d1d','#7d7668','#ffffff'
C={'Europe':'#2f5d8a','Middle East':'#8a3a2f','Asia':'#b07a1e','Americas':'#4a6b3a','Africa':'#7a4a6b','Oceania':'#2f6b6b','Global':'#4a4a55'}
CARDS=[('Middle East','IRAN WAR','Kuwait, Bahrain intercept Iranian drones'),('Asia','APEC SHENZHEN','Xi greets Trump as APEC opens'),('Americas','US POLITICS','Democrats pick Jeffries as speaker'),('Europe','UKRAINE WAR','Russia fires 141 drones at Ukraine'),('Middle East','GAZA','Board of Peace: Gaza truce may collapse'),('Asia','DISASTER','Cyclone Akvan nears Andhra Pradesh'),('Global','CLIMATE','COP31: 75 countries back 35x35 goal'),('Asia','LABOUR','Bangladesh protests shut 55 factories'),('Africa','SUDAN WAR','RSF drone strikes killed 37 in El Obeid'),('Global','CULTURE','GTA VI goes on sale after 13 years'),('Europe','ECONOMY','UK inflation rises to 3.6%'),('Global','SPACE','Voyager 1 is one light-day from Earth'),('Europe','UKRAINE AID','EU proposes 45bn euro loan for Ukraine')]
BRIEFS=[('Middle East','Tehran','Iran says it downed a US MQ-9 near Hormuz'),('Middle East','Riyadh','the coalition downs a Houthi cruise missile'),('Middle East','Jerusalem','the Knesset approves nine deputy speakers'),('Asia','Manila','Trump hails a trade deal; Manila is vaguer'),('Asia','Seoul',"Lee seeks China's help for peace on the peninsula"),('Asia','Tokyo','Japan posts a sixth straight monthly trade deficit'),('Asia','Lahore',"the world's most polluted big city again, AQI 339"),('Asia','Kuala Lumpur','the ringgit hits a five-month low'),('Asia','Shenzhen','Xi and Lee conclude FTA services talks'),('Asia','Bangkok','a Chinese director is jailed over a collapsed tower'),('Asia','Singapore',"Aiko's first imperial visit in 20 years"),('Asia','Seoul','a court acquits the Daegu mayor in a martial-law case'),('Americas','Monterrey','Mexico edge Jamaica to set up a semi against the USA'),('Americas','Los Angeles','the Lakers win a ninth straight game'),('Oceania','Auckland','the tsunami advisory is lifted after a 60 cm surge'),('Europe','Berlin','the coalition will cut the power tax and cap fuel prices'),('Europe','Germany','Berlin accuses Russia of chemical breaches'),('Europe','Cambridge','human is named word of the year'),('Europe','Sofia','a sunk LPG tanker was hit by projectiles'),('Europe','The Hague','the ICJ sets its Rohingya ruling for Thursday'),('Americas','Washington','Fed minutes: more hikes; gold under $3,800'),('Americas','New York','the Dow falls 0.8%; Nvidia shares fall 2.4%'),('Americas','San Francisco','Anthropic to price its IPO; trading Thursday'),('Americas','California','Waymo halts freeway rides after a state ban'),('Americas','Washington','the NSA confirms a classified-network outage'),('Americas','Ottawa','Carney says China trade is no worry for Trump'),('Americas','Lima','Peru declares a fuel-supply emergency over El Nino'),('Africa','Kinshasa','the WHO keeps DR Congo Ebola a global emergency'),('Africa','Addis Ababa','Ethiopia and Eritrea mass troops on the border'),('Africa','Johannesburg',"South Africa's inflation rises to 5.2 percent"),('Africa','Cape Town','SA Rugby seeks a full hearing on the Erasmus ban'),('Oceania','Sydney','Tame Impala sweeps the ARIA Awards')]
LEDGER=[]
def measure(s,p,z): return ImageFont.truetype(p,round(z*64)).getlength(str(s))/64
def T(s,x,y,z,p=SANS,fill=INK,anchor='',box=None,extra=''):
 if box is not None:LEDGER.append((str(s),measure(s,p,z),box))
 fam={SANS:'DejaVu Sans',BOLD:'DejaVu Sans',SERIF:'DejaVu Serif'}[p]; wt=' font-weight="700"' if p!=SANS else ''
 return f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{z}" fill="{fill}"{wt}'+(f' text-anchor="{anchor}"' if anchor else '')+f' {extra}>{html.escape(str(s))}</text>'
def R(x,y,w,h,c,rx=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}"/>'
def P(points,c):return f'<polygon points="{points}" fill="{c}"/>'
def O(x,y,r,c):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
def wrap(text,font_path,size,max_width):
 out=[];q=''
 for word in text.split():
  t=(q+' '+word).strip()
  if q and measure(t,font_path,size)>max_width:out.append(q);q=word
  else:q=t
 if q:out.append(q)
 return out
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
 elif n==2:
  z+=R(X(5),Y(12),w*.18,h*.34,RED)+P(f'{X(14)},{Y(17)} {X(16)},{Y(23)} {X(22)},{Y(23)} {X(17)},{Y(27)} {X(19)},{Y(34)} {X(14)},{Y(30)} {X(9)},{Y(34)} {X(11)},{Y(27)} {X(6)},{Y(23)} {X(12)},{Y(23)}',c)
  z+=R(X(77),Y(12),w*.18,h*.34,'#2f5d8a')+R(X(82),Y(17),w*.09,h*.035,WHITE)+R(X(82),Y(25),w*.09,h*.035,WHITE)+R(X(82),Y(33),w*.09,h*.035,WHITE)
  z+=O(X(31),Y(34),h*.11,INK)+O(X(69),Y(34),h*.11,INK)+P(f'{X(20)},{Y(72)} {X(25)},{Y(47)} {X(37)},{Y(47)} {X(44)},{Y(72)}',INK)+P(f'{X(56)},{Y(72)} {X(63)},{Y(47)} {X(75)},{Y(47)} {X(80)},{Y(72)}',INK)
  z+=f'<path d="M{X(35)} {Y(51)}L{X(49)} {Y(61)}M{X(65)} {Y(51)}L{X(51)} {Y(61)}" stroke="{c}" stroke-width="8" stroke-linecap="round"/>'+O(X(50),Y(61),h*.055,INK)+R(X(37),Y(67),w*.26,h*.13,c)
 elif n==3:
  z+=R(X(8),Y(35),w*.32,h*.43,c)+R(X(11),Y(31),w*.26,h*.08,INK)+R(X(14),Y(16),w*.012,h*.19,INK)+P(f'{X(15)},{Y(16)} {X(27)},{Y(20)} {X(15)},{Y(25)}',RED)
  z+=O(X(50),Y(73),h*.095,c)+f'<rect x="{X(31)}" y="{Y(45)}" width="{w*.38}" height="{h*.075}" rx="2" fill="{INK}" transform="rotate(27 {X(50)} {Y(49)})"/><rect x="{X(44)}" y="{Y(34)}" width="{w*.1}" height="{h*.36}" rx="2" fill="{INK}" transform="rotate(-48 {X(49)} {Y(52)})"/>'
  z+=R(X(76),Y(24),w*.075,h*.54,c)+R(X(87),Y(43),w*.075,h*.35,RED)+T('56',X(79.75),Y(20),7,BOLD,INK,'middle')+T('44',X(90.75),Y(39),7,BOLD,INK,'middle')
 elif n==5:z+=R(X(7),Y(12),w*.38,h*.7,c)+R(X(57),Y(12),w*.36,h*.7,c)+P(f'{X(44)},{Y(12)} {X(53)},{Y(33)} {X(45)},{Y(49)} {X(57)},{Y(64)} {X(48)},{Y(82)}',INK)+P(f'{X(18)},{Y(75)} {X(42)},{Y(48)} {X(67)},{Y(32)} {X(49)},{Y(56)}',WHITE)+P(f'{X(72)},{Y(76)} {X(83)},{Y(52)} {X(94)},{Y(76)}',INK)
 elif n==6:
  z+=f'<path d="M{X(8)} {Y(52)}C{X(8)} {Y(17)} {X(57)} {Y(10)} {X(62)} {Y(38)}C{X(65)} {Y(62)} {X(28)} {Y(69)} {X(25)} {Y(43)}C{X(23)} {Y(27)} {X(48)} {Y(24)} {X(49)} {Y(39)}C{X(50)} {Y(49)} {X(37)} {Y(51)} {X(36)} {Y(41)}" fill="none" stroke="{c}" stroke-width="6" stroke-linecap="round"/>'+O(X(37),Y(40),h*.045,INK)
  z+=f'<path d="M{X(2)} {Y(62)}Q{X(23)} {Y(56)} {X(43)} {Y(63)}T{X(73)} {Y(62)}M{X(2)} {Y(72)}Q{X(20)} {Y(65)} {X(38)} {Y(72)}T{X(70)} {Y(71)}M{X(2)} {Y(82)}Q{X(18)} {Y(75)} {X(34)} {Y(82)}T{X(64)} {Y(81)}" fill="none" stroke="{INK}" stroke-width="3"/>'
  z+=f'<path d="M{X(0)} {Y(89)}Q{X(40)} {Y(84)} {X(72)} {Y(90)}" fill="none" stroke="{c}" stroke-width="3"/>'+R(X(78),Y(63),w*.16,h*.24,c)+P(f'{X(74)},{Y(64)} {X(85)},{Y(49)} {X(96)},{Y(58)} {X(91)},{Y(64)}',INK)
 elif n==7:z+=O(X(23),Y(49),h*.3,c)+P(f'{X(4)},{Y(43)} {X(18)},{Y(35)} {X(29)},{Y(46)} {X(43)},{Y(39)} {X(43)},{Y(54)} {X(23)},{Y(59)} {X(10)},{Y(53)}',WHITE)+R(X(56),Y(36),w*.025,h*.49,INK)+P(f'{X(57)},{Y(37)} {X(48)},{Y(16)} {X(59)},{Y(31)} {X(73)},{Y(19)}',c)+R(X(82),Y(17),w*.055,h*.52,WHITE)+O(X(85),Y(73),h*.09,RED)+O(X(93),Y(18),h*.1,c)
 elif n==8:z+=R(X(4),Y(38),w*.43,h*.49,c)+P(f'{X(4)},{Y(38)} {X(16)},{Y(22)} {X(16)},{Y(38)} {X(29)},{Y(22)} {X(29)},{Y(38)}',INK)+R(X(15),Y(57),w*.24,h*.3,INK)+R(X(52),Y(17),w*.35,h*.2,c)+R(X(53),Y(16),w*.025,h*.5,INK)+R(X(85),Y(16),w*.025,h*.5,INK)+''.join(O(X(q),Y(72),h*.06,INK)+R(X(q-2),Y(78),w*.04,h*.14,c) for q in (58,70,82,94))
 elif n==10:z+=P(f'{X(7)},{Y(70)} {X(15)},{Y(35)} {X(28)},{Y(25)} {X(47)},{Y(25)} {X(60)},{Y(35)} {X(68)},{Y(70)} {X(58)},{Y(82)} {X(48)},{Y(67)} {X(27)},{Y(67)} {X(17)},{Y(82)}',c)+R(X(24),Y(45),w*.15,h*.05,INK)+R(X(29),Y(40),w*.05,h*.15,INK)+O(X(50),Y(43),h*.045,INK)+O(X(57),Y(52),h*.045,INK)+O(X(83),Y(38),h*.2,WHITE)+R(X(82),Y(20),w*.025,h*.2,INK)+R(X(83),Y(37),w*.1,h*.035,INK)
 elif n==11:z+=R(X(8),Y(15),w*.28,h*.67,c)+R(X(14),Y(23),w*.16,h*.18,WHITE)+R(X(31),Y(27),w*.05,h*.44,INK)+O(X(36),Y(70),h*.07,INK)+P(f'{X(50)},{Y(80)} {X(70)},{Y(42)} {X(78)},{Y(54)} {X(93)},{Y(20)} {X(88)},{Y(55)} {X(77)},{Y(50)}',RED)+R(X(72),Y(67),w*.21,h*.17,c)
 elif n==12:
  z+=R(X(21),Y(35),w*.19,h*.22,c)+f'<path d="M{X(21)} {Y(42)}Q{X(4)} {Y(15)} {X(10)} {Y(51)}Q{X(16)} {Y(52)} {X(21)} {Y(42)}" fill="{INK}"/>'+R(X(39),Y(43),w*.29,h*.035,INK)+R(X(27),Y(55),w*.025,h*.23,INK)
  z+=''.join(O(X(q),Y(r),h*.025,INK) for q,r in ((8,70),(16,22),(35,16),(48,28),(60,13),(71,31)))
  z+=f'<path d="M{X(42)} {Y(66)}H{X(88)}" fill="none" stroke="{c}" stroke-width="2.5" stroke-dasharray="3 4"/><path d="M{X(55)} {Y(61)}V{Y(71)}M{X(66)} {Y(61)}V{Y(71)}M{X(77)} {Y(61)}V{Y(71)}" stroke="{INK}" stroke-width="2"/>'+O(X(93),Y(66),h*.1,'#2f5d8a')+P(f'{X(88)},{Y(64)} {X(92)},{Y(61)} {X(96)},{Y(64)} {X(94)},{Y(69)} {X(90)},{Y(69)}',WHITE)
 else:z+=O(X(20),Y(43),h*.29,c)+''.join(O(X(20+17*math.cos(k*math.pi/6)),Y(43)+17*math.sin(k*math.pi/6),1.5,WHITE) for k in range(12))+R(X(64),Y(14),w*.27,h*.44,'#2f5d8a')+R(X(64),Y(36),w*.27,h*.22,'#b07a1e')+P(f'{X(43)},{Y(69)} {X(58)},{Y(55)} {X(70)},{Y(62)} {X(83)},{Y(50)} {X(95)},{Y(57)} {X(83)},{Y(65)} {X(70)},{Y(70)} {X(57)},{Y(63)}',INK)
 return z
def dotmap():
 try:rows=open('/tmp/mask.txt').read().splitlines()
 except OSError:rows=[]
 z=''.join(O(40+xx*2.8,666+yy*1.75,.7,GREY) for yy,row in enumerate(rows[:45]) for xx,ch in enumerate(row[:90]) if ch=='#')
 pins=[(200,683),(238,692),(91,685),(174,673),(211,686),(249,705),(145,690),(224,700),(168,715),(286,726),(152,669),(58,699),(184,677)]
 for n,(x,y) in enumerate(pins,1):z+=O(x,y,5.2,RED)+T(n,x,y+2.3,6.2,BOLD,WHITE,'middle',10.4)
 return z
def tab_widths(order,counts):
 proportional=[944*counts[a]/45 for a in order]
 minimum=[measure(f'{a.upper()} {counts[a]}',BOLD,10.5)+14 for a in order]
 widths=[max(p,m) for p,m in zip(proportional,minimum)]
 excess=sum(widths)-944
 while excess>1e-9:
  adjustable=[i for i,w in enumerate(widths) if w>minimum[i]+1e-9]
  room=sum(widths[i]-minimum[i] for i in adjustable)
  assert room+1e-9>=excess
  for i in adjustable:
   widths[i]-=excess*(widths[i]-minimum[i])/room
  excess=sum(widths)-944
 widths[-1]+=944-sum(widths)
 return widths
def svg():
 LEDGER.clear();o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024">{R(0,0,1024,1024,PAPER)}<path d="M40 12H984M40 34H984" stroke="{INK}" stroke-width=".8"/>',T("THE WORLD'S NEWS IN ONE PICTURE",40,27,10.5,SANS,INK,box=400),T('45 STORIES · 7 REGIONS · 13 ILLUSTRATED · ALL FROM WEDNESDAY',984,27,10.5,BOLD,RED,'end',560)]
 # Measured DejaVu Serif Bold at 54px: 927px wide.
 o += [f'<text x="48.5" y="96" font-family="DejaVu Serif" font-weight="700" font-size="54" fill="{INK}">Wednesday 18 November 2026</text>',f'<path d="M40 112H984" stroke="{INK}" stroke-width=".8"/>']
 counts=Counter(a for a,_,_ in CARDS+BRIEFS); order=sorted(C,key=lambda a:(-counts[a],list(C).index(a)));x=40
 widths=tab_widths(order,counts);print('tab widths:', ' '.join(f'{a}={w:.2f}' for a,w in zip(order,widths)))
 for a,w in zip(order,widths):
  o += [R(x,120,w,28,C[a]),T(f'{a.upper()} {counts[a]}',x+w/2,138,10.5,BOLD,WHITE,'middle',w-14)];x+=w
 ticker=[('55','factories shut'),('141','drones fired at Ukraine'),('37','killed in El Obeid'),('3.6%','UK inflation')]
 assert len(ticker)==4
 gap=24; total=sum(measure(a,BOLD,9.6)+4+measure(b,SANS,9.6) for a,b in ticker)+gap*(len(ticker)-1)
 if total>944:ticker=ticker[:-1];total=sum(measure(a,BOLD,9.6)+4+measure(b,SANS,9.6) for a,b in ticker)+gap*(len(ticker)-1)
 assert len(ticker)==4
 assert total<=944
 tx=40
 for i,(figure,label) in enumerate(ticker):
  fw=measure(figure,BOLD,9.6);lw=measure(label,SANS,9.6)
  o += [T(figure,tx,160,9.6,BOLD,RED,box=fw+.1),T(label,tx+fw+4,160,9.6,SANS,INK,box=lw+.1)]
  tx+=fw+4+lw
  if i<len(ticker)-1:o.append(f'<path d="M{tx+gap/2} 151V163" stroke="{GREY}" stroke-width=".6"/>');tx+=gap
 pos=[(32+i*315,180,306,92) for i in range(3)]+[(32+i*189,340,180,86) for i in range(5)]+[(32+i*189,500,180,86) for i in range(5)]
 for n,((reg,kick,head),(x,y,w,ih)) in enumerate(zip(CARDS,pos),1):
  o += [f'<rect x="{x}" y="{y}" width="{w}" height="150" fill="none" stroke="{GREY}" stroke-width=".8"/>',scene(n,x,y,w,ih,C[reg]),R(x,y+ih,w,14,C[reg]),T(kick,x+5,y+ih+10.5,8.5,BOLD,WHITE,box=w-10)]
  hs=19 if n<4 else 13.5
  lines=wrap(head,SERIF,hs,w-16)
  while len(lines)>2 and hs>11:
   hs-=.5;lines=wrap(head,SERIF,hs,w-16)
  assert len(lines)<=2
  for j,line in enumerate(lines):o.append(T(line,x+8,y+ih+14+hs+j*hs*1.15,hs,SERIF,INK,box=w-16))
  o += [R(x,y,16,16,RED),T(n,x+8,y+11.5,9.5,BOLD,WHITE,'middle',16)]
 o += [T('WHERE IT HAPPENED',40,656,8.5,BOLD,INK,box=300),dotmap(),R(356,660,628,100,WHITE),R(356,660,3,100,RED)]
 date="DATE CHECK  Left out because first reported before 18 November: Nvidia's $115.8bn quarter, the Prague train crash, Mongolia's president resigning. Every story here happened or was first reported on Wednesday 18 November 2026; contested claims are attributed."
 for j,line in enumerate(wrap(date,BOLD,8.6,607)):o.append(T(line,369,681+j*16,8.6,BOLD if j==0 else SANS,INK,box=607))
 o += [T('ALSO ON WEDNESDAY 18 NOVEMBER',40,780,10.5,BOLD,RED,box=500,extra='letter-spacing="1"'),f'<path d="M40 788H984" stroke="{INK}" stroke-width=".8"/>']
 for num,(reg,place,desc) in enumerate(BRIEFS,14):
  k=num-14;col=k//11;row=k%11;x=40+col*323;y=804+row*15.4;nw=measure(str(num)+' ',BOLD,8);pw=measure(place+' ',BOLD,8);dw=measure(desc,SANS,8)
  if nw+pw+dw>297:
   print(f'brief {num} too wide: {nw+pw+dw:.2f}px: {place} {desc}',file=sys.stderr);raise SystemExit(1)
  o += [T(str(num)+' ',x,y,8,BOLD,RED,box=nw+.1),T(place+' ',x+nw,y,8,BOLD,INK,box=pw+.1),T(desc,x+nw+pw,y,8,SANS,INK,box=dw+.1),f'<path d="M{x} {y+4}H{x+297}" stroke="{GREY}" stroke-opacity=".15" stroke-width=".7"/>']
 o += [f'<path d="M40 964H984" stroke="{INK}" stroke-width=".8"/>',T('Every story happened or was first reported on 18 November 2026. Sources: Reuters, AP, AFP, BBC, Al Jazeera. Original flat-vector illustrations.',40,982,8.4,SANS,INK,box=790),T('18 NOVEMBER 2026',984,982,8.4,BOLD,INK,'end',150),'</svg>']
 worst=max((w/b for _,w,b in LEDGER),default=0); item=max(LEDGER,key=lambda q:q[1]/q[2]);print(f'worst ratio: {worst:.4f} ({item[0]})');assert worst<=1
 result=''.join(o);assert '…' not in result and '...' not in result
 return result
def main():
 out=sys.argv[1] if len(sys.argv)>1 else 'entry.png'
 with tempfile.NamedTemporaryFile(suffix='.svg',delete=False) as f:f.write(svg().encode());name=f.name
 try:subprocess.run(['rsvg-convert','-w','1024','-h','1024','-o',out,name],check=True)
 finally:os.unlink(name)
if __name__=='__main__':main()
