# dvh-fam-notebooks  
et repo som inneholder jupyter notebook-er for team familie

## Pre-commit (for notebooks)

Vi bruker pre-commit for å sikre at notebooks ikke pusher output (print) til github.

Dette gjør at ingen sensetive/personlige data kommer på avvei ved et uheld.

### Oppsett (må gjøres én gang)
`.pre-commit-config.yaml` ligger allerede i repoet.
Kjør dette én gang etter at du har klonet repoet:

```bash
uv pip install pre-commit
pre-commit install
```

### Første gang du bruker det
Hvis pre-commit endrer filer under commit, kjør:

```bash
git add .
git commit -m "re-commit etter pre-commit cleanup"
```