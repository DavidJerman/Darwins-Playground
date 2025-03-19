# Darwin's Playground

## Definicija problema

V sistemu bodo dve osnovni vrsti bitij:

- žrtve (rastlinojedci),
- plenilci (mesojedci).

Plenilci potrebujejo tako vodo (morajo najti vodni vir) kot hrano (žrtve), medtem ko žrtve potrebujejo hrano
(vir hrane, kot so rastline) in vodo (vir z vodo). Fokus te raziskovalne naloge bodo žrtve in njihove strategije
za preživetje v danem okolju. Plenilci imajo bolj omejen dostop do virov, kar pomeni, da bodo vedno na preži za
rastlinojedci.

Agenti globalnega znanja o okolju nimajo. Znanje si gradijo na podlagi raziskovanja okolja in informacij, ki
jih dobijo od ostalih agentov.

Strategije agentov bodo zasnovane na podlagi Q-učenja, kjer pa bo poudarek predvsem na izmenjavi informacij
med agenti iste vrste. Izmenjava informacij bo pripomogla k boljšemu uspehu populacije kot celote kot tudi
agenta samega.

### Okolje

Okolje bo predstavljeno s pomočjo dvodimenzionalne plošče, kjer bodo posamezni kvadratki predstavljali
različne dele površja (voda, pesek, viri hrane itd.). Agenti bodo za premikanje po različnih ploščah
porabili različno količino energije.

Okolje je dinamično in se lahko spreminja skozi čas. Lokacija, količina in uporabnost virov (voda, hrana)
se lahko spreminjajo zaradi različnih zunanjih dejavnikov, kot so vremenske spremembe (npr. dež, suša, mrak)
ali sezonske spremembe, ki vplivajo na količino hrane in vode v okolju. Te spremembe bodo vplivale na strategije
preživetja agentov, ki se bodo morali hitro prilagoditi novim pogojem.

### Obnašanje agentov

Agenti bodo lahko v okolju izvedli več različnih akcij:

- gibanje: navzgor, navzdol, levo, desno,
- prehranjevanje: v primeru, da se nahajajo ob viru hrane,
- komunikacija: izmenjava informacij z ostalimi agenti.

Cilj je, da se razvijejo optimizirane strategije za preživetje v tem dinamičnem okolju, ob upoštevanju
spreminjajočih se virov in pogojev.

### Lastnosti agentov

Agenti imajo različne lastnosti, ki vplivajo na njihovo obnašanje in strategijo preživetja:

- energija (potrebna za vse akcije, ko je dosežena energija nič, agent začne izgubljati življenje),
- življenjske točke (ko se agent poškoduje, le-te izgubi, ko je dosežena vrednost nič, agent umre).

Poleg tega vsak agent hrani koristne informacije o okolju, ki jih uporabi kot del strategije za premikanje
po okolju. To so informacije, kot so:

- lokacija virov,
- zadnja videna lokacija plenilcev ...

### Primeri iz realnega sveta

Problemi iz realnega sveta, ki so primerljivi s to nalogo so:

- strateške video igre kot npr. *Sid Meier’s Civilization® VI*, kjer se uporablja kompleksno ravnanje z viri,
  prilagajanje na dinamično okolje in interakcija med različnimi agenti (npr. enotami, naravnimi viri, naselji),
- biološki ekosistemi, kjer se spremljajo interakcije med plenilci in žrtvami, prilagajanje na sezonske spremembe
  in evolucijske strategije za preživetje,
- nadzorovanje naravnih virov v simulacijah, kot so sistemi za upravljanje z vodo, energijo ali gozdovi, kjer
  različni agenti (npr. podjetja, skupnosti, države) sprejemajo odločitve, ki vplivajo na okolje in druge akterje,
- robotika in avtonomni sistemi, kjer roboti sodelujejo in tekmujejo za vire v dinamičnem okolju, kot so pri reševanju 
  nalog v nesrečah ali za iskanje virov na težko dostopnih območjih ...

### Ključne besede

1. Večagentni sistemi,
2. Simulacija prilagajanja,
3. Optimizacija strategij,
4. Q-Learning.

## Evaluacija problema

Sledeča dela so bila v pomoč pri načrtovanju evaluacije rešitve:

1. [Holland, J. H. (1975). "Adaptation in Natural and Artificial Systems"](http://repo.darmajaya.ac.id/3794/1/Adaptation%20in%20Natural%20and%20Artificial%20Systems_%20An%20Introductory%20Analysis%20with%20Applications%20to%20Biology%2C%20Control%2C%20and%20Artificial%20Intelligence%20%28A%20Bradford%20Book%29%20%28%20PDFDrive%20%29.pdf),
2. [Wooldridge, M. (2002). "An Introduction to MultiAgent Systems"](https://uranos.ch/research/references/Wooldridge_2001/TLTK.pdf),
3. Galanter, E., & Ginsberg, A. (2011). "Self-Organizing Systems: Theory and Applications".

... TODO ...

## Načrt rešitve

### Informacije o skupini

Izbrana projektna skupina je skupina št. 4.

Na tem projektu pa delava sledeča študenta:

- David Jerman,
- Andraž Škof.

### Tehnične informacije o projektu

Projekt je dostopen na spletni strani GitHub in sicer na sledečem naslovu:
[Darwin's Playground](https://github.com/DavidJerman/Darwins-Playground).

Poglaviten programski jezik izbran za izvedbo tega projekta je `Python`, ki pa se bo kombiniral
z raznimi programskimi knjižnicami, ki bodo omogočile lažji razvoj končne rešitve.

### Iterativen razvoj projekta

#### Iteracija 1: Osnovna struktura

1. Osnovna implementacija agentov in njihovih lastnosti,
2. Osnovna implementacija statičnega okolja,
3. Osnovno obnašanje agentov – gibanje, iskanje virov.

#### Iteracija 2: Povečanje kompleksnosti agentov in okolja

1. Implementacija Q-učenja za agente,
2. Osnovne strategije preživetja.

#### Iteracija 3: Nadgradnja Q-učenja

1. Deljenje znanja med agenti,
2. Kooperativne strategije (nadgradnja Q-učenja).

#### Iteracija 4: Povratne informacije, izboljšave in dokumentacija

1. Optimizacija performance,
2. Končno testiranje,
3. Evaluacija različnih pristopov.

### Opis rešitve z UML diagramom

... Tule pride UML diagram ...
