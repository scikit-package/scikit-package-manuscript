This is a Cookiecutter template for creating Overleaf LaTex paper repositories using Billinge group standards.

# Features:
- Auto-generates the repository name, paper title, and one author name.
- Uses the IUCR LaTeX template (`iucr.bst`, `iucrit.bst`, `iucrjournals.cls`, `fig1.png`).
- Includes dynamically generated files `cmds-general.tex`, `cmds-programs.tex`, and `packages.tex` from https://github.com/Billingegroup/latex-headers.
- Includes empty .bib files: `bg-pdf-standards.bib`, `billinge-group-bib.bib`, ``hand-coded.bib``, and ``repo_name.bib``.

# HOW TO USE

1. cd to the directory that contains this folder.
   Install Cookiecutter, run the template, and follow the prompts:

   ```bash
   cookiecutter cookiecutter-overleaf
   ```

2. Push to GitHub:
   ```bash
   git remote add origin git@github.com:<yourusername>/<repo_name>.git
   git push -u origin main
   ```

# Release Workflow
## Overview
In this guide, you will learn to release to GitHub.

## The Release Process
To create the ``sciki-package-manuscript`` repository, we will largely follow the ``scikit-package`` release workflow. This workflow will:
1. Bump a version, create a git tag (e.g. v1.0.0 or whatever version you decide), and let GitHub register that tag as a formal release.
2. In our case, “releasing” means publishing the LaTeX sources on GitHub. 
3. Once the tag is pushed, a GitHub Release is created under that tag, and any chosen manuscript artifacts are attached for download.
4. General instructions for this can be found at [this link](https://scikit-package.github.io/scikit-package/release-guides/pypi-github.html).
5. Note that one difference from the workflow in ``scikit-package`` is that this is a manuscript directory with latex files in it. It will never be sent to PyPI and pip installed.
6. Done!



