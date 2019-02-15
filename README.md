### sea-ice project ###

## 1. Classification des années de toutes les simulations CanESM2-LE
K-means clustering
données de bases sie (en %) après une transformation logarithmique
utilisation d'une 3eme classe (une sorte de zone tampon) des années pour instaurer une 'frontière' claire entre les régimes avec et sans glace de mer
information à conserver: année, membre, classe (1, 2 ou tampon)
résultats du clustering: pas de glace -> 0 - 110'000'000, tampon -> 26'000'000 - 318'000'000, glace -> 185'000'000 - 534'000'000
ACHEVÉ

## 2. Construction de la correspondance avec les simulations ClimEx
reprendre l'information conservée et ajouter une colonne avec le nom de la simulation ClimEx
ACHEVÉ

## 3. Detrend des simulations
appliquer le polygone québécois sur les jeux de données
detrender avec un polynôme d'ordre 4 pour chaque point de grille
ACHEVÉ

## 4. Calcul des indicateurs sur les simulations ClimEx
- 3 saisons: SON, DJFM, AMJ
- avec tasmin et tasmax: mean, std
- avec tasmax seulement: 95e, 99e percentiles et maximum annuel (qmax95, qmax99, maxx)
- avec tasmin seulement: 5e, 1er percentile et minimum annuel (qmin05, qmin01, minn)
- avec pr (séries journalières OBTENUES via un code Julia)
- avec prsn (régler le souci de l'axe des temps)

## 5. Études régionaux (par régions administratives)
- travail sur les fichiers finaux, masque avec Julia


## Construction des figures
- distributions globales
- quantile-quantile des distributions
- différence entre max(C1) et max(C2) en cartes
