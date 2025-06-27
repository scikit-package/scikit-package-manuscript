from pathlib import Path
from unittest import mock

import pytest


@pytest.fixture(scope="session")
def template_files():
    skm_template_files = {
        "article.cls": r"Contents of article.cls",
        "package-existing-in-manuscript.tex": r"""
\documentclass{article}
\usepackage{package-in-manuscript}
\newcommand{\command_in_manuscript}
\begin{document}
Contents of manuscript
\bibliography{bib-in-manuscript}
\bibliographystyle{chicago}
\end{document}
    """,
    }
    yield skm_template_files


@pytest.fixture(scope="session")
def user_repo_files_and_contents():
    user_repo_files_and_contents = {
        "usepackages.txt": r"\usepackage{package-from-user-usepackage}",
        "newcommands.txt": r"\newcommand{\command_from_user_newcommands}{}",
        "user-bib-file-1.bib": "Contents of user-bib-file-1.bib",
        "user-bib-file-2.bib": "Contents of user-bib-file-2.bib",
        "user-supplied-non-bib-file.tex": (
            "Contents of user-supplied-non-bib-file.tex"
        ),
    }
    yield user_repo_files_and_contents


@pytest.fixture
def mock_home(tmp_path):
    with mock.patch.object(Path, "home", return_value=tmp_path):
        yield tmp_path


@pytest.fixture
def user_filesystem(
    tmp_path,
    template_files,
    user_repo_files_and_contents,
):
    # create a filesystem with spm in a .cookiecutters directory and
    # template directories called article, other, and another
    # the article template contains a set of files defined in TEMPLATE_FILES
    spm_path = Path(tmp_path / ".cookiecutters" / "scikit-package-manuscript")
    spm_path.mkdir(parents=True, exist_ok=True)

    template_names = ["other", "another"]
    for template_name in template_names:
        template_path = spm_path / "templates" / template_name
        template_path.mkdir(parents=True, exist_ok=True)

    article_path = Path(spm_path / "templates" / "article")
    article_path.mkdir(parents=True, exist_ok=True)
    for key, value in template_files.items():
        template_file_path = article_path / key
        template_file_path.write_text(value)

    source_dir = tmp_path / "source-dir"
    source_dir.mkdir()
    target_dir = tmp_path / "target-dir"
    target_dir.mkdir()
    for key, value in user_repo_files_and_contents.items():
        file_path = source_dir / key
        file_path.write_text(value)

    empty_dir = tmp_path / "empty-dir"
    empty_dir.mkdir()

    dir_with_duplicated_file = tmp_path / "duplicated-dir"
    dir_with_duplicated_file.mkdir()
    key = "usepackage.txt"
    Path(dir_with_duplicated_file / key).touch()

    yield tmp_path
