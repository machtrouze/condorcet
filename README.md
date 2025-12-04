# Flux RSS Horaires Bus (Île-de-France Mobilités)

Ce projet génère automatiquement un flux RSS à partir de l'API Île-de-France Mobilités.

## Étapes d'installation
1. **Ajouter le secret API** :
   - Allez dans `Settings > Secrets and variables > Actions`.
   - Cliquez sur `New repository secret`.
   - Nom : `IDFM_API_KEY`.
   - Valeur : votre clé API Île-de-France Mobilités.

2. **Activer GitHub Pages** :
   - Allez dans `Settings > Pages`.
   - Source : `Deploy from a branch`.
   - Branche : `main` et `/root`.

3. **Déploiement automatique** :
   - Le workflow s'exécute toutes les 5 minutes.
   - Le fichier `horaires_bus.xml` sera mis à jour et publié.

## Dépendances
```
requests
```
