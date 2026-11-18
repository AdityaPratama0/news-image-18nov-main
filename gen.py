#!/usr/bin/env python3
"""Draw the deterministic 45-story broadsheet."""
import html, math, os, subprocess, sys, tempfile
from collections import Counter
PAPER,INK,RED,GREY,WHITE="#f7f3e8","#161616","#8f1d1d","#7d7668","#fff"
C={"Europe":"#2f5d8a","Middle East":"#8a3a2f","Asia":"#b07a1e","Americas":"#4a6b3a","Africa":"#7a4a6b","Oceania":"#2f6b6b","Global":"#4a4a55"}
CARDS=[
("Middle East","IRAN WAR","Kuwait and Bahrain intercept Iranian drones","Iran's army says it targeted US forces at Ali Al Salem; an ADNOC ship was hit in Hormuz, one missing, 11 injured."),
("Asia","APEC SHENZHEN","Xi greets Trump as APEC opens","A Trump-Xi-Putin summit is set for Thursday; Xi urged AI and free-trade cooperation."),
("Americas","US POLITICS","Democrats pick Jeffries as House speaker","The caucus vote was 251-11; he is the first new Democratic speaker in a decade."),
("Europe","UKRAINE WAR","Russia fires 141 drones at Ukraine","126 were downed; 5 killed and 15 injured in a day; power was cut to more than 80 Rivne settlements."),
("Middle East","GAZA","Board of Peace warns the truce may collapse","Its first report to the Security Council says Israel blocked the civil administration."),
("Asia","DISASTER","Cyclone Akvan nears Andhra Pradesh","The IMD expects landfall around noon Friday; Odisha readies up to 204,070 people to evacuate."),
("Global","CLIMATE","COP31: 75 countries back the 35x35 power goal","Electricity is to be 35 percent of energy use by 2035; Johan Rockström warns of 2.8-3C."),
("Asia","LABOUR","Bangladesh garment protests shut 55 factories","Workers seek a Tk 30,000 minimum wage; the Dhaka-Mymensingh highway was blocked."),
("Africa","SUDAN WAR","Amnesty: RSF drone strikes killed 37 in El Obeid","It calls for a war-crimes inquiry; the RSF denies responsibility."),
("Global","CULTURE","GTA VI goes on sale after 13 years","A midnight launch began in New Zealand; Sensor Tower estimates 15m pre-release sales."),
("Europe","ECONOMY","UK inflation rises to 3.6%, a one-year high","October CPI rose from 3.5% as diesel hit a record, the ONS says."),
("Global","SPACE","Voyager 1 is one light-day from Earth","The probe is 25.9bn km out, 49 years after launch."),
("Europe","UKRAINE AID","EU proposes a 45bn euro loan for Ukraine","The money is for 2027, proposed as US support wavers.")]
BRIEFS=[
("Middle East","Tehran","Iran says it downed a US MQ-9 near Hormuz"),("Middle East","Riyadh","the coalition downs a Houthi cruise missile"),("Middle East","Jerusalem","the Knesset approves nine deputy speakers"),
("Asia","Manila","Trump hails a trade deal; Manila says none was signed"),("Asia","Seoul","Lee seeks China's help for peace on the peninsula"),("Asia","Tokyo","Japan posts a sixth straight monthly trade deficit"),("Asia","Lahore","the world's most polluted big city again, AQI 339"),("Asia","Kuala Lumpur","the ringgit hits a five-month low"),("Asia","Shenzhen","Xi and Lee conclude FTA services talks"),("Asia","Bangkok","a Chinese director is jailed over a collapsed tower"),("Asia","Singapore","Princess Aiko makes the first imperial visit in 20 years"),("Asia","Seoul","a court acquits the Daegu mayor in a martial-law case"),("Asia","Kashmir","a LeT militant is killed in the Kulgam siege"),("Asia","Naypyidaw","Myanmar's leader is reconsidering ASEAN ties"),("Asia","Da Nang","Russian Tu-95 bombers are parked at Da Nang"),
("Europe","Berlin","the coalition will cut the power tax and cap fuel prices"),("Europe","Germany","Berlin accuses Russia of chemical-weapons breaches"),("Europe","Cambridge",'"human" is named word of the year'),("Europe","Sofia","a sunk LPG tanker was hit by projectiles"),("Europe","The Hague","the ICJ sets its Rohingya genocide ruling for Thursday"),
("Americas","Washington","the Fed's minutes signal more hikes; gold falls under $3,800"),("Americas","New York","the Dow falls 0.8 percent; Nvidia shares fall 2.4 percent"),("Americas","San Francisco","Anthropic is set to price its IPO; trading starts Thursday"),("Americas","California","Waymo halts freeway rides after a state ban"),("Americas","Washington","the NSA confirms an outage on a classified network"),("Americas","Ottawa","Carney says China trade is no worry for Trump"),("Americas","Lima","Peru declares a fuel-supply emergency over El Nino"),
("Africa","Kinshasa","the WHO keeps DR Congo's Ebola outbreak a global emergency"),("Africa","Addis Ababa","Ethiopia and Eritrea mass troops on the border"),("Africa","Johannesburg","South Africa's inflation rises to 5.2 percent"),("Africa","Cape Town","SA Rugby seeks a full hearing on the Erasmus ban"),("Oceania","Sydney","Tame Impala sweeps the ARIA Awards")]
def E(s): return html.escape(str(s),quote=True)
def wd(s,z,b=False): return sum(.29 if c in " ilI.,:;'!|" else .88 if c in "MW@%&Q" else .56 for c in str(s))*z*(1.04 if b else 1)
def tx(s,x,y,z,cl="s",fill=None,b=False,anchor=None,maxw=None,space=None,minscale=.78):
    a=(f' fill="{fill}"' if fill else "")+(f' font-weight="700"' if b else "")+(f' text-anchor="{anchor}"' if anchor else "")+(f' letter-spacing="{space}"' if isinstance(space,str) else "")
    w=wd(s,z,b)
    if maxw and w>maxw:a+=f' textLength="{maxw:.1f}" lengthAdjust="spacingAndGlyphs"'
    return f'<text class="{cl}" x="{x}" y="{y}" font-size="{z}"{a}>{E(s)}</text>'
def wrap(s,z,m,n=2):
    out=[]; q=""
    for w in s.split():
        t=(q+" "+w).strip()
        if q and wd(t,z)>m:out.append(q);q=w
        else:q=t
    if q:out.append(q)
    if len(out)>n:
        used=sum(len(x.split()) for x in out[:n]);out=out[:n];out[-1]+=" "+" ".join(s.split()[used:])
    return out
def P(d,c=INK,f="none",dash=""):
    return f'<path d="{d}" fill="{f}" stroke="{c}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"'+(f' stroke-dasharray="{dash}"' if dash else "")+'/>'
def scene(n,x,y,w,h,c):
    X=lambda a:x+a*w/180;Y=lambda a:y+a*h/74
    r=lambda a,b,ww,hh,fill:f'<rect x="{X(a)}" y="{Y(b)}" width="{ww*w/180}" height="{hh*h/74}" rx="3" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>'
    circ=lambda a,b,rr,fill:f'<circle cx="{X(a)}" cy="{Y(b)}" r="{rr*w/180}" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>'
    if n==1:return P(f'M{X(0)} {Y(61)}Q{X(45)} {Y(43)} {X(92)} {Y(61)}T{X(180)} {Y(54)}',c)+P(f'M{X(103)} {Y(53)}h{X(59)-X(0)}l{X(10)}-10h5',INK,c)+P(f'M{X(25)} {Y(15)}l10 9h-10zM{X(61)} {Y(8)}l10 9h-10zM{X(91)} {Y(20)}l10 9h-10z',INK,c)+P(f'M{X(35)} {Y(24)}Q{X(71)} {Y(42)} {X(117)} {Y(36)}',c,"none","5 5")+P(f'M{X(118)} {Y(25)}l5 8 9-5-2 10 10 3-9 5 3 9-10-3-5 8-1-10-10-2 9-5z',INK,c)
    if n==2:return r(58,48,64,14,c)+r(12,5,34,14,c)+r(134,5,34,14,c)+circ(48,25,7,INK)+circ(132,25,7,INK)+P(f'M{X(40)} {Y(48)}l4-15h10l8 15M{X(120)} {Y(48)}l6-15h10l7 15M{X(56)} {Y(39)}l18 8 16-8m34 0l-18 8-16-8M{X(12)} {Y(4)}v37m156-37v37')
    if n==3:return P(f'M{X(14)} {Y(58)}h75M{X(22)} {Y(58)}V32h60v26M{X(27)} {Y(32)}Q{X(52)} {Y(3)} {X(77)} {Y(32)}M{X(39)} {Y(32)}v26m14-26v26m14-26v26')+P(f'M{X(105)} {Y(18)}l26 16m-6-5l-12 22m-12 0h48',c)+r(151,17,17,37,c)+r(151,34,27,20,INK)
    if n==4:return P(f'M{X(20)} {Y(12)}l12 10H20zM{X(32)} {Y(22)}Q{X(63)} {Y(38)} {X(96)} {Y(24)}',c,"none","5 5")+P(f'M{X(91)} {Y(65)}l12-39 13 39m-21-15h17m-13-13h10m-7-11l8 39m4-23q20 15 35 3')+r(137,43,31,21,c)+P(f'M{X(134)} {Y(43)}l19-15 18 15M{X(144)} {Y(50)}v8m14-8v8')
    if n==5:return P(f'M{X(18)} {Y(63)}V14h58v17l-10 8 10 8v16m35 0V14H78M{X(60)} {Y(56)}q22-28 44-18m-22 7q-8-13-18-8m19 8q10-12 20-11',c)+P(f'M{X(130)} {Y(59)}l14-27 14 27zM{X(144)} {Y(42)}v9m0 4v1',INK,c)
    if n==6:return P(f'M{X(18)} {Y(48)}q22-38 53-17q18 14-2 27q-16 9-27-4q-9-11 8-16q14-3 18 7',c)+P(f'M{X(0)} {Y(64)}q13-17 26 0q13-17 26 0q13-17 26 0')+r(126,43,28,21,c)+P(f'M{X(121)} {Y(44)}l19-15 18 15m-10-14V14h18v10h-18')
    if n==7:return circ(48,38,28,c)+P(f'M{X(22)} {Y(32)}q12-5 20 4t15-3t18 5M{X(45)} {Y(11)}q-5 13 6 21t-1 29',PAPER)+P(f'M{X(108)} {Y(64)}V27m0 0l-14-14m14 14l18-9m-18 9l1-20')+r(145,16,12,42,WHITE)+r(149,31,4,23,c)+circ(151,58,8,c)
    if n==8:
        z=r(9,26,63,38,c)+P(f'M{X(9)} {Y(26)}l18-13v13l18-13v13M{X(25)} {Y(43)}h32v21H25z')+r(89,16,54,18,c)+P(f'M{X(89)} {Y(15)}v28m54-28v28')
        for q in (96,116,136,156):z+=circ(q,49,5,INK)+P(f'M{X(q-5)} {Y(65)}l5-11h7l5 11',INK,c)
        return z
    if n==9:return P(f'M{X(30)} {Y(9)}l12 10H30z',INK,c)+''.join(circ(q,52,12,c)+P(f'M{X(q-14)} {Y(49)}l14-12 14 12') for q in (27,61,95))+r(128,14,32,39,WHITE)+P(f'M{X(135)} {Y(26)}h18m-18 9h18m-18 9h12M{X(153)} {Y(51)}l18 14m-12-11a12 12 0 1 0-1 1')
    if n==10:return P(f'M{X(20)} {Y(48)}q0-24 21-24h30q21 0 21 24l-7 10q-7 7-13-7l-5-8H45l-5 8q-6 14-13 7zM{X(36)} {Y(35)}v13m-6-6h12',INK,c)+circ(69,38,4,INK)+circ(79,45,4,INK)+circ(123,27,18,WHITE)+P(f'M{X(123)} {Y(27)}V15m0 12l10 6M{X(101)} {Y(64)}h75V44h-25')
    if n==11:return r(20,13,43,51,c)+r(28,21,27,14,WHITE)+P(f'M{X(63)} {Y(25)}q18 0 18 17v13q0 8 8 8t8-8V29l-8-8M{X(104)} {Y(58)}l25-32 25 18m-25-18h17v17')+r(144,49,27,15,c)
    if n==12:return f'<ellipse cx="{X(76)}" cy="{Y(35)}" rx="{24*w/180}" ry="{8*h/74}" fill="{c}" stroke="{INK}" stroke-width="2.5"/>'+P(f'M{X(76)} {Y(35)}v21m0-21L51 16m25 19l31-16m-31 16h48m-48 8H45m62-24h20')+circ(151,52,13,c)+P(f'M{X(128)} {Y(45)}Q{X(113)} {Y(61)} {X(94)} {Y(54)}',c,"none","4 5")
    stars=''.join(f'<circle cx="{X(42+22*math.cos(k*math.pi/6))}" cy="{Y(32+22*math.sin(k*math.pi/6))}" r="2" fill="{PAPER}"/>' for k in range(12))
    return circ(42,32,25,c)+stars+tx("€",X(34),Y(43),29,"r",WHITE,True)+r(130,7,38,24,"#2f5d8a")+f'<rect x="{X(130)}" y="{Y(19)}" width="{38*w/180}" height="{12*h/74}" fill="#b07a1e"/>'+P(f'M{X(72)} {Y(49)}l24-10 15 8 19-7m-34-1l7 12m8-4l-8 8')
def dotmap():
    try:rows=open("/tmp/mask.txt").read().splitlines()
    except OSError:rows=[]
    z=[]
    for yy,row in enumerate(rows[:45]):
        for xx,ch in enumerate(row[:90]):
            if ch=="#":z.append(f'<circle cx="{35+xx*2.75:.1f}" cy="{720+yy*1.32:.1f}" r=".72" fill="{GREY}"/>')
    pins=[(202,742),(239,748),(88,739),(176,724),(211,736),(247,759),(145,746),(226,754),(169,764),(286,772),(153,721),(57,751),(185,730)]
    for n,(x,y) in enumerate(pins,1):z+=[f'<circle cx="{x}" cy="{y}" r="5.2" fill="{RED}" stroke="{PAPER}" stroke-width="1.2"/>',tx(n,x,y+2.4,6.2,"s",WHITE,True,"middle")]
    return ''.join(z)
def svg():
    counts=Counter(x[0] for x in CARDS+BRIEFS); tabs=sorted(C,key=lambda r:(-counts[r],list(C).index(r)))
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024"><rect width="1024" height="1024" fill="{PAPER}"/><style>.s{{font-family:"DejaVu Sans",sans-serif;fill:{INK}}}.r{{font-family:"DejaVu Serif",serif;fill:{INK};font-weight:700}}</style><path d="M32 12H992M32 34H992" stroke="{INK}" stroke-width=".8"/>',tx("THE WORLD'S NEWS IN ONE PICTURE",32,28,10.5,"s",None,True,None,None,"1.4"),tx("45 STORIES · 7 REGIONS · 13 ILLUSTRATED · ALL FROM WEDNESDAY",992,28,10.5,"s",RED,True,"end",520),'<text class="r" x="40" y="98" font-size="60" textLength="944" lengthAdjust="spacingAndGlyphs">Wednesday 18 November 2026</text>',f'<path d="M32 114H992" stroke="{INK}" stroke-width=".8"/>']
    x=32
    for i,r in enumerate(tabs):
        w=960*counts[r]/45 if i<6 else 992-x;o += [f'<rect x="{x}" y="120" width="{w}" height="28" fill="{C[r]}"/>',tx(f"{r.upper()} {counts[r]}",x+w/2,138,10.5,"s",WHITE,True,"middle",w-7)];x+=w
    x=32
    for i,(num,label) in enumerate([("55","factories shut"),("141","drones fired at Ukraine"),("37","killed in El Obeid"),("3.6%","UK inflation"),("204,070","ready to evacuate"),("11,300","Ebola cases")]):
        w=wd(num+" "+label,9.4,True)+18
        if x+w>992:break
        o += [tx(num,x,168,9.4,"s",RED,True),tx(label,x+wd(num,9.4,True)+6,168,9.4)];x+=w
        if i<5:o.append(f'<path d="M{x-7} 158V171" stroke="{GREY}" stroke-width=".6"/>')
    pos=[(32+i*315,180,306,88) for i in range(3)]+[(32+i*189,347,180,74) for i in range(5)]+[(32+i*189,514,180,74) for i in range(5)]
    for n,((region,kicker,head,fact),(x,y,w,ih)) in enumerate(zip(CARDS,pos),1):
        c=C[region];o += [f'<rect x="{x}" y="{y}" width="{w}" height="158" fill="none" stroke="{GREY}" stroke-width=".8"/><clipPath id="c{n}"><rect x="{x}" y="{y}" width="{w}" height="{ih}"/></clipPath><g clip-path="url(#c{n})">',scene(n,x,y,w,ih,c),f'</g><rect x="{x}" y="{y+ih}" width="{w}" height="13" fill="{c}"/>',tx(kicker,x+5,y+ih+9.7,8.5,"s",WHITE,True,None,w-10,".5")]
        hs=17 if n<4 else 13.5;lines=wrap(head,hs,w-10)
        for j,line in enumerate(lines):o.append(tx(line,x+5,y+ih+28+j*(hs+1),hs,"r",None,True,None,w-10))
        fy=y+ih+33+len(lines)*(hs+1)
        for j,line in enumerate(wrap(fact,8.6,w-10)):o.append(tx(line,x+5,fy+j*10,8.6,"s",GREY,None,None,w-10,.72))
        o += [f'<rect x="{x}" y="{y}" width="17" height="17" fill="{RED}"/>',tx(n,x+8.5,y+12,10,"s",WHITE,True,"middle")]
    o += [tx("WHERE IT HAPPENED",32,714,8.5,"s",None,True,None,None,"1"),dotmap(),f'<rect x="332" y="706" width="660" height="86" fill="{WHITE}"/><rect x="332" y="706" width="3" height="86" fill="{RED}"/>']
    date="DATE CHECK  Left out because first reported before 18 November: Nvidia's $115.8bn quarter, the Prague train crash, Mongolia's president resigning, Cyclone Akvan's formation on 16 November. Every story here happened or was first reported on Wednesday 18 November 2026; contested claims are attributed."
    for j,line in enumerate(wrap(date,8.6,638,4)):o.append(tx(line,345,723+j*15.5,8.6,"s",None,j==0,None,638,.7))
    o += [tx("ALSO ON WEDNESDAY 18 NOVEMBER",32,801,10.5,"s",RED,True,None,None,"1.3"),f'<path d="M32 806H992" stroke="{INK}" stroke-width=".8"/>']
    for idx,(region,place,desc) in enumerate(BRIEFS,14):
        k=idx-14;col=k//11;row=k%11;x=32+col*329;y=823+row*13.8;pw=wd(place,9.2,True)
        o += [tx(idx,x,y,9.2,"s",RED,True),tx(place,x+19,y,9.2,"s",None,True),tx(desc,x+23+pw,y,9.2,"s",None,None,None,290-pw,None,.68),f'<path d="M{x} {y+4}H{x+313}" stroke="{GREY}" stroke-opacity=".2" stroke-width=".7"/>']
    o += [f'<path d="M32 974H992" stroke="{INK}" stroke-width=".8"/>',tx("Every story happened or was first reported on 18 November 2026. Sources: Reuters, AP, AFP, BBC, Al Jazeera. Original flat-vector illustrations.",32,992,8.4,"s",None,None,None,790),tx("18 NOVEMBER 2026",992,992,8.4,"s",None,True,"end"),"</svg>"]
    return ''.join(o)
def main():
    out=sys.argv[1] if len(sys.argv)>1 else "entry.png"
    with tempfile.NamedTemporaryFile(suffix=".svg",delete=False) as f:f.write(svg().encode());name=f.name
    try:subprocess.run(["rsvg-convert","-w","1024","-h","1024","-o",out,name],check=True)
    finally:os.unlink(name)
if __name__=="__main__":main()
