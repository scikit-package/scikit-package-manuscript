This is a Cookiecutter template for creating Overleaf LaTex paper repositories using Billinge group standards.

# Features:
- Auto-generates the repository name, paper title, and one author name.
- Uses the IUCR LaTeX template (`iucr.bst`, `iucrit.bst`, `iucrjournals.cls`, `fig1.png`).
- Includes dynamically generated files `cmds-general.tex`, `cmds-programs.tex`, and `packages.tex` from https://github.com/Billingegroup/latex-headers.
- Includes empty .bib files: `bg-pdf-standards.bib`, `billinge-group-bib.bib`, ``hand-coded.bib``, and ``repo-name.bib``.

# HOW TO USE

1. cd to the directory that contains this folder.
   Install Cookiecutter, run the template, and follow the prompts:

   ```bash
   cookiecutter cookiecutter-overleaf
   ```

2. Push to GitHub:
   ```bash
   git remote add origin git@github.com:yourusername/repo-name.git
   git push -u origin main
   ```

# Release Workflow
## Overview
In this guide, you will learn to release your source code to GitHub so that by the end of the guide, you can install your package via ``pip install <package-name>``.

## Initiate the Release Process
1. In the repository, create an issue on GitHub with the ``Release`` option as shown below:
   ![GitHub issue screenshot](https://github.com/user-attachments/assets/5eb8276f-1afd-487c-a878-92f2524f962a)
2. Check off all items in the first checklist for GitHub release.
3. Proceed to the next section

## Start Pre-Release
1. Review the release GitHub issue created in the previous step.
2. Make sure the ```PAT_TOKEN``` is configured at the organization or repository level by following the instructions in [Appendix 1](https://github.com/zmx27/scikit-package-manuscript/tree/release-documentation?tab=readme-ov-file#appendix-1).
3. Setup GitHub Pages at the repository level by following the instructions in [Appendix 2](https://github.com/zmx27/scikit-package-manuscript/tree/release-documentation?tab=readme-ov-file#appendix-2).
4. Confirm the ``maintainer_github_username`` section in ``.github/workflows/build-wheel-release-upload.yml`` is that of the project maintainer.
5. In your terminal, run ``git checkout main && git pull upstream main`` to sync with the main branch.
6. (Optional but recommended) Install and run the ``vulture`` tool to identify and manually remove unused or dead code before tagging a release:
   ```
   $ conda install vulture
   #### Example outputs after running vulture ####
   $ vulture src/ tests/
   tests/test_module1.py:22: unused import 'os' (100% confidence)
   ```
   Review the output and remove or suppress unused code when it is not needed to keep the release clean and maintainable.
7. Run the following:
   ```
   # For pre-release, use *.*.*-rc.* e.g., 1.0.0-rc.0
   # rc stands for release candidate
   $ git tag <version>-rc.<rc-number>
   $ git push upstream <version>-rc.<rc-number>
   ```
8. Once the tag is pushed, visit the ``Actions`` tab in the repository to monitor the CI progress.
9. You will see that the GitHub Actions workflow is triggered and the package is built and uploaded to GitHub.
10. For ``pre-release``, it will not update the documentation on GitHub Pages. It will also not update the changelog. See the next section for the full release process.

## Full Release
1. In your terminal, run ``git checkout main && git pull upstream main`` to sync with the main branch.
2. Run the following:
   ```
   # For release, use *.*.* e.g., 1.0.0
   $ git tag <version>
   $ git push upstream <version>
   ```
3. Notice that ``CHANGELOG.rst`` is also updated with the new release version and the documentation is built under the ``gh-pages`` branch.

## Appendix 1
### Setup ``PAT_TOKEN`` to allow GitHub Actions to compile ``CHANGELOG.rst``
Recall that dring a release (not pre-release) process, the GitHub Actions workflow compiles the news items in the ``CHANGELOG.rst`` file in the ``main`` branch. Hence, the GitHub workflow needs to link with this privilege through a personal access token (PAT) of the project maintainer.
1. Visit [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Click Generate new token and choose the classic option.
3. Under Note, write, “GitHub CI release”
4. Set the Expiration date of the token.
5. Under Select scopes, check repo and user.
6. Scroll down, click Generate token.
7. Done!

![image](https://github.com/user-attachments/assets/247411f9-ad33-4944-98ba-8dfb55d75f0a)  

Copy and paste the ``PAT_TOKEN`` to your GitHub organization:
1. Go to ``Settings`` in your organization.
2. Click the ``Actions`` tab under ``Secrets and variables``.
3. Click ``New organization secret`` and add a new secret and name it as ``PAT_TOKEN``.
4. Done!

## Appendix 2
### Host documentation online with GitHub Pages
Let's host the documentation online, e.g., ``https://diffpy.github.io/diffpy.utils``, using GitHub Pages.
1. Visit ``Settings ‣ Code and automation ‣ Pages``.
2. Click ``Deploy`` from a branch under ``Source``.
3. Choose the ``gh-pages`` branch and ``/(root)``
4. Click ``Save``.

![image](https://github.com/user-attachments/assets/743cc6eb-1e77-476d-a87a-16ea8ae757b7)

5. Wait a few minutes and visit your GitHub Pages URL!




