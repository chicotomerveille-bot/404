# 404

**Dictée vocale locale, en français, sur Windows.**

Appuyez sur un raccourci, parlez, relâchez : le texte s'écrit directement dans
l'application où vous êtes. Aucun son ne quitte votre machine — pas de compte,
pas de cloud, pas de télémétrie.

404 est un fork de [Handy](https://github.com/cjpais/Handy), recentré sur un seul
usage : dicter du français, vite et juste, sur un PC sans carte graphique.

## Ce qui change par rapport à Handy

- **Trois modèles, un seul choix à faire.** Les poids Whisper (GGML) sont hébergés
  sur ce dépôt et téléchargés depuis nos releases — plus de dépendance à un
  hébergement tiers.
- **Français par défaut.** La langue de reconnaissance est fixée au français au
  lieu de la détection automatique, peu fiable sur les phrases courtes.
- **Interface noir et blanc.** Plus aucune couleur d'accent : le contraste porte
  l'interface, seules les erreurs et les avertissements gardent une teinte.
- **Windows x64 uniquement.** Le reste de la matrice de build upstream est retiré.

## Les modèles

| Modèle | Taille | Pour quoi |
| --- | --- | --- |
| **404 Rapide** (base) | 141 Mo | Notes courtes, réponse quasi instantanée |
| **404 Équilibré** (small) | 465 Mo | Le compromis par défaut : rapide et précis |
| **404 Ultra** (large-v3-turbo) | 1,55 Go | Précision maximale, termes techniques et noms propres |

Les trois tournent sur processeur, sans GPU. Le modèle se choisit dans les
réglages et se télécharge au premier lancement.

## Installation

1. Téléchargez l'installeur Windows depuis les
   [releases](https://github.com/chicotomerveille-bot/Handy/releases).
2. Lancez-le : installation par utilisateur, aucun droit administrateur requis.
3. Au premier démarrage, choisissez un modèle — « 404 Équilibré » est un bon
   point de départ.

Le raccourci par défaut est `Ctrl + Espace` : maintenez-le pour parler, relâchez
pour insérer le texte.

## Vie privée

- L'audio est traité sur votre machine par whisper.cpp, via
  [transcribe-cpp](https://github.com/handy-computer/transcribe-cpp).
- Le silence est filtré en local par Silero VAD.
- Les seules connexions sortantes servent à télécharger un modèle et à vérifier
  les mises à jour ; les deux peuvent être désactivées dans les réglages.

## Construire

Le projet se compile avec Tauri 2 (Rust + React). La compilation Windows est
assurée par GitHub Actions : chaque push sur `main` produit un installeur
téléchargeable dans l'onglet *Actions*.

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
