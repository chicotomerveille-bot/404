# 404

**Dictée vocale locale, en français, sur Windows.**

Appuyez sur un raccourci, parlez, relâchez : le texte s'écrit directement dans
l'application où vous êtes. Aucun son ne quitte votre machine — pas de compte,
pas de cloud, pas de télémétrie.

404 est un fork de [Handy](https://github.com/cjpais/Handy), recentré sur un seul
usage : dicter du français, vite et juste, sur un PC sans carte graphique.

## Ce qui change par rapport à Handy

- **Trois modèles, un seul choix à faire.** Les poids Whisper (GGML) de
  « 404 Rapide » et « 404 Équilibré » sont hébergés sur ce dépôt et téléchargés
  depuis nos releases. « 404 Ultra » utilise Parakeet TDT 0.6B v3 (GGUF Q8_0),
  récupéré depuis le dépôt Hugging Face officiel à une révision figée — aucun
  gros fichier n'est stocké dans le dépôt ni dans l'installeur.
- **Français par défaut.** La langue de reconnaissance est fixée au français au
  lieu de la détection automatique, peu fiable sur les phrases courtes.
  Parakeet v3 fait exception : il détecte lui-même la langue et ignore cette
  consigne (le français fait partie de ses 25 langues).
- **Interface noir et blanc.** Plus aucune couleur d'accent : le contraste porte
  l'interface, seules les erreurs et les avertissements gardent une teinte.
- **Windows x64 uniquement.** Le reste de la matrice de build upstream est retiré.

## Les modèles

| Modèle                               | Taille | Pour quoi                                           |
| ------------------------------------ | ------ | --------------------------------------------------- |
| **404 Rapide** (Whisper base)        | 141 Mo | Notes courtes, réponse quasi instantanée            |
| **404 Équilibré** (Whisper small)    | 465 Mo | Le compromis par défaut : rapide et précis          |
| **404 Ultra** (Parakeet TDT 0.6B v3) | 705 Mo | Précision maximale, 25 langues, très faible latence |

Les trois tournent sur processeur, sans GPU. Le modèle se choisit dans les
réglages et se télécharge au premier lancement.

Face à l'ancien `large-v3-turbo` (1,55 Go), Parakeet v3 occupe moins de la
moitié de l'espace et transcrit environ **9× plus vite** sur CPU (facteur temps
réel 13,7 contre 1,4 dans les benchmarks du catalogue), avec un taux d'erreur
d'environ 5,3 % en français sur FLEURS.

## Installation

1. Téléchargez l'installeur Windows depuis les
   [releases](https://github.com/chicotomerveille-bot/404/releases).
2. Lancez-le : installation par utilisateur, aucun droit administrateur requis.
3. Au premier démarrage, choisissez un modèle — « 404 Équilibré » est un bon
   point de départ.

Le raccourci par défaut est `Ctrl + Espace` : maintenez-le pour parler, relâchez
pour insérer le texte.

## Vie privée

- L'audio est traité sur votre machine par
  [transcribe-cpp](https://github.com/handy-computer/transcribe-cpp) :
  whisper.cpp pour « Rapide » et « Équilibré », le chargeur Parakeet pour
  « Ultra ».
- Le silence est filtré en local par Silero VAD.
- Les seules connexions sortantes servent à télécharger un modèle et à vérifier
  les mises à jour ; les deux peuvent être désactivées dans les réglages.

## Provenance du modèle Ultra

« 404 Ultra » n'est pas embarqué dans l'installeur. Au premier lancement,
l'application télécharge le GGUF depuis
[handy-computer/parakeet-tdt-0.6b-v3-gguf](https://huggingface.co/handy-computer/parakeet-tdt-0.6b-v3-gguf)
à la révision figée `85ac09ea12fc4b1112fa76810059364bc6adc9de`, puis le vérifie
avec le SHA-256 compilé dans `catalog.json` :

- taille : 739 508 576 octets (705 Mio), téléchargés uniquement sur le poste de
  l'utilisateur final, jamais dans ce dépôt Git
- SHA-256 : `5859f77944efcd8eafa23a6350731960b2b55b2203df51f319665c807d802cc7`

Pour héberger ce fichier sur la release `models-v1` (optionnel), il suffit
d'ajouter un champ `url` au fichier `Q8_0` de l'entrée `four04-parakeet-v3` du
catalogue. Cette opération manipule 705 Mio : à faire depuis un runner CI plutôt
qu'en local.

## Construire

Le projet se compile avec Tauri 2 (Rust + React). La compilation Windows est
assurée par GitHub Actions : chaque push sur `main` produit un installeur
téléchargeable dans l'onglet _Actions_.

```bash
bun install
bun run tauri dev     # développement
bun run tauri build   # installeur
```

Les prérequis détaillés (Rust, Visual Studio Build Tools, CMake) sont dans
[BUILD.md](BUILD.md).

## Crédits

404 repose entièrement sur le travail de [cj Pais](https://github.com/cjpais) et
des contributeurs de Handy, publié sous licence MIT (voir [LICENSE](LICENSE)).
Les poids Whisper proviennent de [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp)
(OpenAI Whisper, licence MIT).
Les poids « 404 Ultra » proviennent de
[NVIDIA Parakeet TDT 0.6B v3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3),
convertis en GGUF par
[handy-computer](https://huggingface.co/handy-computer/parakeet-tdt-0.6b-v3-gguf)
(licence CC BY 4.0).
