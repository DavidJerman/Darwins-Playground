# Darwin's Playground

## Definicija problema

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

kjer:

- $S(P_t)$ izbere najbolj prilagojene agente,
- $M(P_t)$ izvaja mutacije na genomih agentov,
- $R(P_t)$ združuje genetske informacije dveh ali več agentov.

Cilj je analizirati, katere strategije preživetja se razvijejo glede na dane okoljske pogoje in kako
različni parametri vplivajo na evolucijski proces.

### Ključne besede

1. Evolucijski algoritmi,
2. Večagentni sistemi,
3. Naravna selekcija,
4. Simulacija prilagajanja,
5. Optimizacija strategij.
