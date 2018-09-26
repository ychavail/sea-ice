### sea-ice project ###

## Étapes de travail
--- 1. Classification des années de toutes les simulations CanESM2-LE
K-means clustering
utilisation d'un tampon de 10% des années pour instaurer une 'frontière' claire entre les régimes avec et sans glace de mer
information à conserver: année, membre, classe (1, 2 ou tampon)

--- 2. Construction de la correspondance avec les simulations ClimEx
reprendre l'information conservée et ajouter une colonne avec le nom de la simulation ClimEx

--- 3. Detrend des simulations
appliquer le polygone québécois sur les jeux de données
detrender avec un polynôme d'ordre 4 pour chaque point de grille

--- extrêmes à investiguer
maximum journalier de précipitations
maximum sur 5 jours de précipitations
5e percentile de la température en DJFM
95e percentile de la température en JJAS
