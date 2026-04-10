# dvh-fam-notebooks
et repo som inneholder jupyter notebook-er for team familie

## Pre-commit (for notebooks)

Vi bruker pre-commit for å sikre at notebooks ikke pusher output (print) til github.

Dette gjør at ingen sensetive/personlige data kommer på avvei ved et uheld.

### Oppsett

en .pre-commit-config.yaml fil ble opprettet og er en del av repoet nå.

Kjør dette én gang etter at du har clonet repoet:

```bash
(uv) pip install pre-commit
pre-commit install
