# Darwin's Playground

## Definicija problema

### Splošna definicija problema

V naravi organizmi tekmujejo za omejene vire, pri čemer evolucijski proces oblikuje njihove strategije
preživetja in reprodukcije. Razumevanje teh procesov je ključno za področja, kot so biologija,
inteligenca in teorija iger. Cilj tega projekta je razviti simulacijo večagentnega sistema, kjer agenti
evolucijsko prilagajajo svoje strategije glede na okoljske pogoje. Vsak agent ima omejene vire in mora
sprejemati odločitve, ki vplivajo na njegovo preživetje in reprodukcijo.

Gre za umetno ustvarjen problem, ki pa temelji na resničnih principih naravne selekcije. Model temelji na
osnovnih evolucijskih mehanizmih, kot so selekcija, mutacija in križanje.

Evolucija je definirana kot iterativni proces s populacijo $P_t$, ki se skozi generacije razvija s pomočjo
selekcijske (*selection*) funkcije $S(P_t)$, mutacijske (*mutation*) funkcije $M(P_t)$ in križanja
(*crossover*) $C(P_t)$:

$P_{t+1} = S(M(R(P_{t})))$

, kjer:

- $S(P_t)$ izbere najbolj prilagojene agente,
- $M(P_t)$ izvaja mutacije na genomih agentov,
- $R(P_t)$ združuje genetske informacije dveh ali več agentov.

Cilj je analizirati, katere strategije preživetja se razvijejo glede na dane okoljske pogoje in kako
različni parametri vplivajo na evolucijski proces.

### Podrobna definicija problema

V sistemu bodo dve osnovni vrsti bitij:

- žrtve (rastlinojedci),
- plenilci (mesojedci).

To bi se kasneje lahko nadgradilo z vsejedimi organizmi, ki se lahko prehranjujejo bodisi z rastlinami bodisi
z žrtvami, odvisno od tega, kaj je na voljo v okolju.

Plenilci potrebujejo tako vodo (morajo najti vodni vir) kot hrano (žrtve), medtem ko žrtve potrebujejo hrano
(vir hrane, kot so rastline) in vodo (vir z vodo). Žrtve se pogosto združujejo v večje skupine, kar omogoča
hitrejšo in bolj raznoliko evolucijo prek mutacije. Plenilci pa imajo bolj omejen dostop do virov, kar pomeni,
da bodo morda potrebovali bolj specifične strategije za preživetje.

Vsa živa bitja imajo določene lastnosti (genom), ki se skozi evolucijo spreminjajo. Sprememba teh lastnosti
lahko pripelje do boljše ali slabše uspešnosti agenta v okolju. Uspešnost agentov se oceni z uporabo funkcije
"life energy", ki se spreminja glede na uspešne in neuspešne akcije agentov, kot je iskanje virov ali srečanje
s plenilci.

Strategije agentov bodo odvisne od njihove vloge v okolju. Plenilci bodo morda razvili strategije, ki
vključujejo večje iskanje žrtev in vodenje bojev za teritorij, medtem ko bodo žrtve razvijale strategije
bega, skrivalnic ali iskanja zaščite v skupinah. Vse te strategije se bodo razvijale skozi evolucijo, ko se
bodo agenti morali prilagoditi na spremembe v okolju in konkurenčne pritiske.

Okolje je dinamično in se lahko spreminja skozi čas. Lokacija, količina in uporabnost virov (voda, hrana)
se lahko spreminjajo zaradi različnih zunanjih dejavnikov, kot so vremenske spremembe (npr. dež, suša, mrak)
ali sezonske spremembe, ki vplivajo na količino hrane in vode v okolju. Te spremembe bodo vplivale na strategije
preživetja agentov, ki se bodo morali hitro prilagoditi novim pogojem.

Interakcije med agenti bodo pomemben del evolucijskega procesa. Plenilci bodo lovili žrtve, kar bo vplivalo na
velikost populacije žrtev, medtem ko bo preživetje plenilcev odvisno od tega, kako učinkovito bodo našli in
ulovili žrtve. Prav tako bodo medsebojne interakcije med agenti pripomogle k dinamiki populacij in različnim
evolucijskim strategijam.

Cilj je, da se razvijejo optimizirane strategije za preživetje v tem dinamičnem okolju, ob upoštevanju
spreminjajočih se virov in pogojev.

### Ključne besede

1. Evolucijski algoritmi,
2. Večagentni sistemi,
3. Naravna selekcija,
4. Simulacija prilagajanja,
5. Optimizacija strategij.

## Evaluacija problema

Sledeča dela so bila v pomoč pri načrtovanju evaluacije rešitve:

1. [Holland, J. H. (1975). "Adaptation in Natural and Artificial Systems"](http://repo.darmajaya.ac.id/3794/1/Adaptation%20in%20Natural%20and%20Artificial%20Systems_%20An%20Introductory%20Analysis%20with%20Applications%20to%20Biology%2C%20Control%2C%20and%20Artificial%20Intelligence%20%28A%20Bradford%20Book%29%20%28%20PDFDrive%20%29.pdf),
2. [Mitchell, M. (1996). "An Introduction to Genetic Algorithms"](https://www.boente.eti.br/fuzzy/ebook-fuzzy-mitchell.pdf),
3. [Wooldridge, M. (2002). "An Introduction to MultiAgent Systems"](https://uranos.ch/research/references/Wooldridge_2001/TLTK.pdf),
4. Galanter, E., & Ginsberg, A. (2011). "Self-Organizing Systems: Theory and Applications",
5. [Evolutionary multi-agent systems](https://home.agh.edu.pl/~iisg/emas/index.php?page=theory&subpage=emas).

Problem se bo ocenil s pomočjo funkcije `fitness`. Gre za funkcijo, ki sestoji iz več parametrov in katero poskušamo
maksimirati. Ta funkcija predstavlja uspešnost agenta v danem okolju. Na ta način lahko ocenimo, ali je bil proces
evolucije uspešen, ali pa je novi agent s procesom evolucije nazadoval. Parametri te funkcije bi bili:

- starost organizma,
- lakota,
- žeja,
- velikost populacije, v kateri organizem živi ...

Vendar pa tradicionalni evolucijski algoritmi običajno zahtevajo znanje celotnega okolja, ki pa posameznim agentom ni
dostopno. Zato namesto `fitness` funkcije uporabimo podobno funkcijo imenovano `life energy`. Vrednost le-te se
spreminja
na podlagi dobrih (odkritje novega vira hrane ali vode) in slabih akcij (žrtev sreča plenilca), ki jih agent izvede v
okolju. Smrt organizma ravno tako predstavlja neuspešno akcijo organizma.

Drugi način evaluacije pa je konvergenca. Ta nam pove, kako hitro agenti najdejo rešitev problema. V najinem primeru
bi to bilo preživetje čim večjega dela populacije oz. odkritje novih virov v naravi, ali pa morebiti v primeru okolja
kot je puščava, odkritje vira vode.

Poleg tega bova upoštevala še druge vidike evalvacije, kot so:

1. **Raznovrstnost populacije**: Ali so agenti v populaciji preveč podobni, kar lahko vodi v stagnacijo evolucijskega
   procesa? Morda bi bilo bolje, da je populacija bolj raznolika, saj to povečuje možnosti za nastanek novih in bolj
   uspešnih strategij,
2. **Stabilnost strategij**: Kako stabilna je strategija, ki jo agenti razvijejo? Ali je ta rešitev dolgoročno vzdržna?,
3. **Večdimenzionalne funkcije uspešnosti**: Poleg osnovnih parametrov (starost, lakota, žeja) bova upoštevala tudi
   interakcije med agenti, prilagodljivost na spremembe okolja in trajnost strategij skozi čas,
4. **Hitrost konvergence**: Kako hitro se najboljši agenti razvijajo skozi generacije? Kako se populacija spreminja in
   ali doseže stabilnost?

Še en zanimiv aspekt tega problema pa je opazovanje obnašanja agentov v statičnem okolju v primerjavi z dinamičnim
okoljem, kjer se spreminja količina virov, vremenske razmere ipd.

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

Naloge:

1. Načrtovanje in implementacija osnovnih razredov agentov in okolje,
2. Razvoj osnovne evolucijske funkcionalnosti: selekcija, mutacija in križanje,
3. Uvedba preprostega evalvacijskega sistema (življenjska energija in osnovni parametri),
4. Implementacija osnovne logike za začetne agentove odločitve (npr. gibanje, iskanje hrane ali vode),
5. Testiranje osnovne strukture z eno generacijo agentov.

#### Iteracija 2: Povečanje kompleksnosti agentov in okolja

1. Razvoj večdimenzionalnih strategij agentov (npr. prilagodljivost na okoljske spremembe, iskanje novih virov),
2. Razširitev okolja z dinamičnimi spremembami (sprememba virov, vremenski pogoji),
3. Razvoj naprednejšega sistema za ocenjevanje uspešnosti agentov (npr. vključitev več parametrov),
4. Izboljšanje mutacije in križanja za boljšo prilagoditev agentov na spremembe v okolju,
5. Implementacija večgeneracijskega sistema za evolucijo agentov,
6. Prvo testiranje sistema z več generacijami in analizo uspešnosti agentov v različnih pogojih.

#### Iteracija 3: Napredna evalvacija in optimizacija strategij

1. Razvoj metod za analizo raznovrstnosti populacije (preprečevanje stagnacije),
2. Razširitev evalvacije s funkcijami, ki spremljajo dolgoročno stabilnost strategij agentov,
3. Izboljšanje metod za hitro konvergenco in stabilizacijo strategij,
4. Implementacija testnih primerov za analizo vpliva različnih parametrov (npr. starost, lakota, žeja) na evolucijo,
5. Analiza rezultatov, priprava poročil o uspešnosti,
6. Optimizacija obstoječega kode za boljšo učinkovitost pri večjih generacijah.

#### Iteracija 4: Povratne informacije, izboljšave in dokumentacija

1. Analiza prejšnjih testov in izvajanje potrebnih izboljšav v agentih, okolju in evolucijskem procesu,
2. Uvedba naprednih funkcij za večjo simulacijsko natančnost (npr. bolj realistično modeliranje okolja),
3. Testiranje z različnimi konfiguracijami (različni pogoji za preživetje, dinamično okolje),
4. Priprava zaključnega poročila o evalvaciji sistema in analiziranih rezultatih,
5. Izdelava uporabniške in tehnične dokumentacije (vključno z UML diagrami, opisom razvoja, konfiguracijami),
6. Zaključni test in optimizacija kode za nemoten zaključek projekta.

#### Povzetek

- Iteracija 1: Postavitev temeljev sistema (agenti, okolje, osnovna evolucija).
- Iteracija 2: Povečanje kompleksnosti, dinamično okolje, naprednejša strategija agentov.
- Iteracija 3: Napredna evalvacija, optimizacija in testiranje različnih parametrov.
- Iteracija 4: Izboljšave na podlagi povratnih informacij, dokončanje projekta in priprava dokumentacije.

### Opis rešitve z UML diagramom

... Tule pride UML diagram ...
