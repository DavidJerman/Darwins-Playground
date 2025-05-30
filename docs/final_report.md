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

Med naprednejšimi pristopi v MARL so metode kot so HC-MARL (Hierarchical Consensus-based MARL)
in CTDE (Centralized Training Decentralized Execution), ki omogočajo izboljšano kooperacijo agentov.
S tem, ko agenti izmenjujejo informacije in sprejemajo odločitve na podlagi lokalnega znanja, lahko
dosežejo konsenz in sprejemajo bolj optimalne akcije, kar vodi do bolj učinkovitega raziskovanja in
upravljanja okolja.

Eden izmed temeljnih izzivov pri MARL je prilagajanje strategij posameznih agentov glede na dinamičnost
okolja, kjer so nagrade in odločitve močno odvisne od interakcij med agenti. Zato je MARL pogosto
modeliran kot večagentska Markovljeva igra, kjer so informacije o stanju okolja in dejanjih drugih
agentov omejene ali deljene v omejenem obsegu.

Za raziskovanje okolja agenti uporabljajo raziskovalne strategije, kot so ε-greedy ali Boltzmannova
eksploracija, ki pa lahko zaradi omejenih izkušenj in velikih stanj povzročajo ponavljajoče se obiske
istih stanj, kar zavira učenje. Ključna prednost sodobnih pristopov je možnost izmenjave znanja med
agenti, na primer z metodo cikličnih poti, ki omogoča deljenje optimalnih poti in s tem pospešuje
konvergenco vrednostne funkcije.

Posebno mesto zasedajo metode, kot so DQN (Deep Q-Network) in njegova nadgradnja DRQN (Deep Recurrent
Q-Network), ki omogočajo učenje z uporabo nevronskih mrež. DRQN z vključitvijo RNN-jev rešuje problem
delnih opazovanj okolja in omogoča uporabo zgodovine vhodnih podatkov za boljše napovedi. Kljub temu
je DQN primarno zasnovan za enega agenta in celovito opazovanje okolja, kar ni optimalno za
večagentske scenarije.

Metoda QMIX predstavlja naprednejši pristop k večagentskemu učenju, saj razširja Value Decomposition
Networks (VDN) z modeliranjem skupne Q-funkcije kot monotone nelinearne kombinacije lokalnih
Q-funkcij agentov. To omogoča decentralizirano izvajanje akcij in učinkovitejše usposabljanje,
vendar z omejitvami v nalogah, kjer je nujno tesno usklajevanje med agenti.

HC-MARL pa uvaja hierarhičen konsenz preko več nivojev, kjer kratkoročni nizko nivojski konsenz
omogoča hitro prilagajanje, medtem ko dolgoročni strateški konsenz vodi k bolj premišljenim
odločitvam. Ta mehanizem dinamičnega prilagajanja pomembnosti nivojev omogoča učinkovito
kombinacijo kratkoročnih in dolgoročnih strategij, kar je ključno v kompleksnih in dinamičnih
okoljih.

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

V najinem projektu se osredotočiva na razvoj inteligentnih agentov (živali), ki se v simuliranem
okolju učijo učinkovito iskati vire hrane in vode. Okolje je predstavljeno kot mreža točk, kjer
so razporejeni ti viri, agenti pa se lahko med njimi premikajo.

Za učenje uporabljava pristop Q-learning, ki agentom omogoča, da na podlagi nagrad in kazni postopoma
izboljšujejo svojo politiko odločanja. Ključno pri tem je, da agenti poskušajo uravnotežiti
raziskovanje neznanih poti in izkoriščanje že naučenih strategij.

Ker pa v najinem sistemu deluje več agentov, je pomembno, da lahko medsebojno izmenjujejo informacije,
kar poveča učinkovitost učenja. Zato uporabljamo paradigmo Centralized Training with Decentralized
Execution (CTDE). To pomeni, da med treningom agenti centralno delijo svoja znanja in izkušnje, kar
pospeši učenje skupne politike, medtem ko v fazi izvajanja vsak agent deluje samostojno z lokalnimi
informacijami.

Pri implementaciji učenja in simulacije agentov uporabljava knjižnico RLLib, ki je del orodij za
večagentno učenje in ponuja podporo za različne algoritme, kot je Proximal Policy Optimization (PPO).
PPO bova uporabili kot primerjalni algoritem za oceno učinkovitosti najine Q-learning rešitve s CTDE
pristopom.

Agenti komunicirajo z izmenjavo ključnih informacij o Q-vrednostih ali optimiziranih poteh, kar
omogoča hitrejše prilagajanje okolju in večjo robustnost sistema.

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
