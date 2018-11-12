### sea-ice project ###

## Étapes de travail
--- 1. Classification des années de toutes les simulations CanESM2-LE
K-means clustering
utilisation d'une 3eme classe (une sorte de zone tampon) des années pour instaurer une 'frontière' claire entre les régimes avec et sans glace de mer
information à conserver: année, membre, classe (1, 2 ou tampon)
DONE

--- 2. Construction de la correspondance avec les simulations ClimEx
reprendre l'information conservée et ajouter une colonne avec le nom de la simulation ClimEx
DONE

--- 3. Detrend des simulations
appliquer le polygone québécois sur les jeux de données
detrender avec un polynôme d'ordre 4 pour chaque point de grille
DONE

--- 4. Calcul des indicateurs d'extrêmes sur les simulations ClimEx
- avec tasmax en JJAS: 95e, 99e percentiles et maximum annuel DONE
- avec tasmin en DJFM: 5e, 1er percentile et minimum annuel DONE
- précipitations à venir

--- 5. Classification des indicateurs par clusters
DONE

--- 6. Statistiques sur les indicateurs classés
- distributions globales
- quantile-quantile des distributions
- différence entre max(C1) et max(C2) en cartes
