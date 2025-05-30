# Darwin's Playground

**Avtorji:** David Jerman, Andraž Škof.


## Ključne besede

1. Večagentni sistemi,
2. Simulacija prilagajanja,
3. Optimizacija strategij,
4. Q-Learning,
5. Učenje s krepitvijo.


## Povzetek

Projekt razvija večagentni sistem, kjer so osnovne vrste bitij plenilci in žrtve (rastlinojedci).
Glavni fokus je na žrtvah in njihovih preživetvenih strategijah v dinamičnem okolju, kjer morajo
iskati hrano in vodo, ob tem pa se izogibati plenilcem.

Okolje je predstavljeno kot dvodimenzionalna mreža z različnimi tipi površin in viri, ki se skozi
čas spreminjajo zaradi vremenskih in sezonskih dejavnikov. Agentom je na voljo le lokalno znanje
pridobljeno z raziskovanjem in komunikacijo z drugimi agenti iste vrste.

Agenti uporabljajo strategije Q-učenja, ki temeljijo na izmenjavi informacij za izboljšanje
učinkovitosti populacije in posameznika. Pomembni so dejavniki, kot so energija, življenjske
točke in shranjevanje informacij o okolju (lokacija virov, plenilcev).

Končni cilj projekta je tako razviti večagentni sistem na osnovi Q-učenja, ki bo agentom
omogočil uspešno navigacijo v okolju. Za implementacijo sva izbrala knjižnico RLLib in jezik
Python. Za primerjalni algoritem pa sva izbrala algoritem PPO.


## Uvod

Večagentsko ojačitveno učenje (Multi-Agent Reinforcement Learning, MARL) predstavlja pomembno
področje umetne inteligence, kjer več agentov sočasno uči in prilagaja svoja dejanja v dinamičnem
okolju. V nasprotju z osnovnimi metodami ojačitvenega učenja, ki se osredotočajo na enega samega
agenta, MARL naslavlja izzive sodelovanja, koordinacije in usklajevanja med agenti za dosego
skupnega ali individualnega cilja.

Glavna prednost teh metod v primerjavi z osnovnimi metodami učenja s krepitvijo je kooperacija različnih 
agentov za doseg cilja. Agenti lahko na podlagi lokalnega znanja in izmenjave informacij pridejo do konsenz 
in sprejemajo boljše odločitve, ki bodo vodile v bolj uspešno raziskovanje okolja.

V večagentskem ojačitvenem učenju je ključen izziv prilagajanje dejanj posameznega agenta dinamičnemu okolju
izboljšanje celotne učinkovitosti sistema. Večina algoritmov predpostavlja, da agent pozna strukturo igre ali
Nashovo ravnotežje ter da ima informacije o dejanjih in nagradah drugih agentov. Ker nagrade temeljijo tako na
lastnih kot na dejanjih sodelujočih agentov, lahko MDP model ojačitvenega učenja obravnavamo kot večagentsko
Markovljevo igro [5].

Pri učenju agenti uporabljajo strategije raziskovanja, kot sta ε-greedy in Boltzmanova eksploracija, saj na
začetku nimajo zadostnega znanja o okolju. Zaradi omejenih izkušenj pogosto večkrat obiščejo ista stanja, kar
postane problematično v večjih prostorskih stanjih. Ključen izziv pri sodelovalnih večagentskih sistemih je
omogočanje izmenjave znanja med agenti. Predlagana optimizacijska metoda cikličnih poti omogoča izvleček
optimalnih poti iz izkušenj, ki jih lahko agenti ali skupine delijo za hitrejšo konvergenco vrednostne funkcije [5].

Prva izmed metod večagentnega učenja s krepitvijo je CTDE.
Metoda CTDE (Centralised Training, Decentralised Execution) je splošna metoda, kjer učenje agentov poteka 
centralno – delitev znanja. Agenti pa akcije izvedejo neodvisno drug od drugega na podlagi svojih preteklih 
izkušenj. Agenti lahko v fazi učenja uporabijo informacije, ki jim med decentraliziranim izvajanjem niso bile 
na voljo.

Nekateri tovrstni pristopi uporabljajo deljeno Q-funkcijo v času učenja. Izguba (loss) se tako za vsakega 
agenta v času učenja izračuna kot skupna Q-funkcija. Posledično imajo agenti tudi tekom decentraliziranega 
izvajanja nekaj znanja od ostalih agentov [4].

DQN (Deep Q-network) je nadgradnja Q-učenja, ki za funkcijo aproksimacije uporablja nevronsko mrežo. Vendar
pa ima DQN informacije o celotnem okolju, zato ta metoda ni relevantna za najin problem.

DRQN (Deep Recurrent Q-network) pa reši problem pomanjkljivih podatkov o okolju, saj omogoča delo z delnimi 
podatki. DRQN temelji na RNN modelu, katerega namen je, da hrani zgodovino vhodnih vrednosti in jo ponovno 
uporabi v prihodnjih napovedih [4].

QMIX je metoda za večagentsko ojačitveno učenje, ki razširja VDN (Value Decomposition Networks) tako, da
omogoča bolj splošne razgradnje vrednostnih funkcij. Namesto preproste vsote lokalnih Q-funkcij, QMIX modelira
skupno Q-funkcijo kot monotono nelinearno funkcijo posameznih Q-funkcij agentov. To pomeni, da lahko agenti še
vedno izbirajo akcije na podlagi svojih lokalnih Q-vrednosti, kar omogoča učinkovitejše usposabljanje in
decentralizirano izvajanje.

QMIX uporablja mixing network, ki zagotavlja monotono kombinacijo posameznih Q-funkcij s pomočjo hiperomrežij,
ki generirajo uteži. Med učenjem se omrežje trenira end-to-end, pri čemer se optimizira napaka med napovedano
skupno Q-funkcijo in ciljno vrednostjo, ki temelji na diskontiranih prihodnjih nagradah. Metoda se dobro 
obnese v okoljih, kjer agenti lahko delujejo pretežno neodvisno, vendar ima omejitve pri nalogah, kjer je 
nujno usklajevanje med agenti [4].

Metoda HC-MARL uporablja več slojev konsenza: konsenz na dolgi rok in konsenz na kratki rok. Kratka opazovanja
v okolju sprožijo takojšen, nizko-nivojski konsenz, medtem ko daljša opazovanja okolja sprožijo bolj 
strateški, visoko nivojski konsenz. Algoritem pa uporablja tudi mehanizem za prilagajanje pomembnosti vsakega 
nivoja, ki se spreminja skupaj z dinamičnim okoljem. Na ta način agenti bolj strateško sprejemajo odločitve, 
ki prinašajo takojšnjo nagrado in odločitve, ki nagrado prinašajo na dolgi rok. HC-MARL je posebej zanimiv za 
najin primer, saj omogoča agentom, da kombinirajo kratkoročne in dolgoročne strategije preživetja v 
dinamičnem okolju [3].


## Sorodna dela

Večina raziskav na področju večagentskega učenja s krepitvijo uporablja klasične algoritme, kot
je Proximal Policy Optimization (PPO), kot osnovo za primerjave in razvoj novih metod. PPO je
učinkovit in stabilen algoritem za samostojno učenje enega agenta v dinamičnih okoljih, vendar
ni posebej zasnovan za kooperacijo med več agenti.

Zaradi narave večagentnih problemov, kjer mora vsak agent prilagajati svoje odločitve na podlagi
vedenja drugih agentov, postanejo enostavni algoritmi, kot je PPO, manj učinkoviti. Zato so bile
razvite metode, kot so HC-MARL in CTDE, ki omogočajo boljšo koordinacijo in delitev informacij
med agenti, kar vodi do bolj uspešnega reševanja skupnih ciljev v kompleksnih okoljih. Eno izmed
del, ki sva ga vzela za zgled, je delo št. 3 pod Viri. 

V najinem delu uporabljava PPO kot osnovni primer primerjave, da izpostaviva prednosti večagentskih
pristopov, predvsem na področju sodelovanja in konsenza med agenti.


## Metodologija

V najinem projektu sva osredotočila na razvoj inteligentnih agentov (živali), ki se v simuliranem
okolju učijo učinkovito iskati vire hrane in vode. Okolje je predstavljeno kot mreža točk, kjer
so razporejeni ti viri, agenti pa se lahko med njimi premikajo.

Okolje v katerem delujejo agenti je dvodimenzionalno in sestoji iz ploščic postavljenih v mrežo. Vsaka
ploščica lahko predstavlja različen tip terena: travnik, pesek, gore, vodo, hrano itd. Gibanje agenta
je na določenih ploščicah omejeno in agent se more tovrstnim polščicam izogibati.

Stanje agenta je predstavljeno z več lastnostmi, kot so življenje, pozicija, lakota itd. Agent se tako
na podlagi svojega stanja in stanja okolja odloči za naslednjo akcijo: gibanje v prostoru v vse štiri
smeri, prehranjevanje, lahko pa tudi ne stori nič.

Agent za svoje akcije prejme nagrado ali pa kazen. Nagrado prejme vedno kadar najde hrano ali vir vode,
kaznovan pa je takrat, ko izgubi energijo zaradi neuspešnega iskanja. Pri tem je treba poudariti, da je
kazen dosti manjša od same nagrade, saj bi sicer bila izguba prevelika.

Za učenje uporabljava pristop Q-learning, ki agentom omogoča, da na podlagi nagrad in kazni postopoma
izboljšujejo svojo politiko odločanja. Ključno pri tem je, da agenti poskušajo uravnotežiti
raziskovanje neznanih poti in izkoriščanje že naučenih strategij.

Ker pa v najinem sistemu deluje več agentov, je pomembno, da lahko medsebojno izmenjujejo informacije,
kar poveča učinkovitost učenja. Zato uporabljava paradigmo Centralized Training with Decentralized
Execution (CTDE). To pomeni, da med treningom agenti centralno delijo svoja znanja in izkušnje, kar
pospeši učenje skupne politike, medtem ko v fazi izvajanja vsak agent deluje samostojno z lokalnimi
informacijami.

Pri implementaciji učenja in simulacije agentov uporabljava knjižnico RLLib, ki je del orodij za
večagentno učenje in ponuja podporo za različne algoritme, kot je Proximal Policy Optimization (PPO).
PPO bova uporabili kot primerjalni algoritem za oceno učinkovitosti najine Q-learning rešitve s CTDE
pristopom.

Agenti komunicirajo z izmenjavo ključnih informacij o Q-vrednostih ali optimiziranih poteh, kar
omogoča hitrejše prilagajanje okolju in večjo robustnost sistema.

Uspešnost agenta sva ocenila z več metrikami: hitrost konvergence, povprečna nagrada skozi iteracije,
delež uspešnih epizod skozi čas in dolžina poti do cilja.


## Poskusi in rezultati

Vzpostavila sva osnovno simulacijsko okolje, kjer agenti izvajajo premike in zbirajo vire, kot
sta hrana in voda. Za učenje in inferenco sva uporabili algoritme PPO iz knjižnice RLlib, ki omogoča
učinkovito implementacijo in testiranje modelov za večagentno učenje.

Z uporabo PPO sva izvedla začetne poskuse, ki so služili predvsem preverjanju funkcionalnosti okolja
in pravilnosti interakcij agentov z okoljem. Ti poskusi so potrdili, da okolje deluje skladno z
zastavljenimi pravili ter da agenti uspešno sprejemajo odločitve na podlagi prejetih nagrad.

Podrobnejša analiza rezultatov, vključno z meritvami hitrosti konvergence, uspešnosti agentov in
vpliva različnih nastavitev, bo izvedena po nadgradnji rešitve s komunikacijo med agenti.

Nisva dokončali implementacije celotne rešitve, predvsem zaradi kompleksnosti problema in omejenih
virov. Med drugim ni bilo izvedene komunikacije med agenti preko CTDE pristopa, prav tako nisva
uspela narediti podrobnejše evalvacije in primerjav z drugimi algoritmi.


## Zaključek

Projekt je predstavljal ambiciozen pristop k večagentnemu učenju v dinamičnem okolju, kjer so bili
načrtovani kompleksni mehanizmi sodelovanja agentov. Kljub nepopolni implementaciji sva vzpostavila
stabilno simulacijsko okolje in izvedla začetne poskuse z uporabo PPO algoritma in knjižnice RLLib.
Ta osnova omogoča nadaljnji razvoj in nadgradnjo, predvsem v smeri implementacije CTDE komunikacije
in izboljšanja učinkovitosti agentov. Prihodnje delo bo usmerjeno v dokončanje manjkajočih komponent
in poglobljeno evalvacijo, ki bo omogočila bolj celovito oceno prednosti večagentnih pristopov.


## Viri

1. [Holland, J. H. (1975). "Adaptation in Natural and Artificial Systems"](http://repo.darmajaya.ac.id/3794/1/Adaptation%20in%20Natural%20and%20Artificial%20Systems_%20An%20Introductory%20Analysis%20with%20Applications%20to%20Biology%2C%20Control%2C%20and%20Artificial%20Intelligence%20%28A%20Bradford%20Book%29%20%28%20PDFDrive%20%29.pdf),
2. [Wooldridge, M. (2002). "An Introduction to MultiAgent Systems"](https://uranos.ch/research/references/Wooldridge_2001/TLTK.pdf),
3. [Hierarchical Consensus-Based Multi-Agent Reinforcement Learning for Multi-Robot Cooperation Tasks](https://arxiv.org/html/2407.08164v2),
4. [An Introduction to Centralized Training for Decentralized Execution in Cooperative Multi-Agent Reinforcement Learning](https://arxiv.org/pdf/2409.03052),
5. [Collaborative multi-agent reinforcement learning based on experience propagation](https://ieeexplore.ieee.org/document/6587341),
6. [A Distributed Q-Learning Algorithm for Multi-Agent Team Coordination](https://ieeexplore.ieee.org/document/1526928),
7. [Ray](https://docs.ray.io/en/latest/rllib/index.html).
