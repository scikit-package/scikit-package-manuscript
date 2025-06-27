import shutil
import subprocess
import tempfile
from pathlib import Path

MANUSCRIPT_FILENAME = "manuscript.tex"


def get_scikit_manuscript_dir():
    """Return the full path to the local scikit-package-manuscript
    dir."""
    cookiecutter_dir = Path.home() / ".cookiecutters"
    candidates = []
    for candidate in cookiecutter_dir.iterdir():
        candidates.append(candidate)
        if (candidate.is_dir() and
                "scikit-package-manuscript" in candidate.name):
            return candidate.resolve()
    return Path(f"couldn't find scikit-package-manuscript, but did "
                f"find {*candidates,}")  # noqa E231


def copy_journal_template_files(journal_template_name, project_dir):
    """Copies files from a package's resource directory to a target
    directory.

    Parameters:
    ===========
    journal_template : str
      The name of the journal latex template to use, e.g. 'article'.
      It must be one of the available templates.
    project_dir : Path
      The path to the location of the output project where the files
      will be copied to.
    """
    cookiecutter_path = get_scikit_manuscript_dir()
    template_dir = cookiecutter_path / "templates" / journal_template_name
    if not template_dir.exists():
        raise FileNotFoundError(f"Cannot find the provided journal_template: "
                                f"{journal_template_name}. Please contact the "
                                f"software developers.")

    if not any(template_dir.iterdir()):
        raise FileNotFoundError(f"Template {journal_template_name} found but "
                                f"it contains no files. Please contact the "
                                f"software developers.")
    for item in template_dir.iterdir():
        dest = project_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)
    return


def get_user_headers(repo_url):
    """Clone a Git repository containing LaTeX header files into a
    string."""
    headers = ""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        subprocess.run(["git", "clone", repo_url, str(tmp_path)], check=True)
        for item in tmp_path.glob('**/*'):
            if item.is_file() and str(item).endswith(".tex"):
                headers += item.read_text()+'\n'
    return headers


def extract_manuscript_packages(manuscript_path):
    contents = manuscript_path.read_text(encoding="utf-8")
    packages, the_rest = _split_lines_with_keyword(contents, r"\usepackage")
    Path(manuscript_path).write_text(the_rest, encoding="utf-8")
    return packages


def _split_lines_with_keyword(content, keyword):
    lines_with_keyword = []
    other_lines = []
    for line in content.splitlines():
        if line.lstrip().startswith(keyword):
            lines_with_keyword.append(line)
        else:
            other_lines.append(line)
    return "\n".join(lines_with_keyword), "\n".join(other_lines)


def _insert_to_manuscript(manuscript_text, insert_text, location_keyword, method):
    lines = manuscript_text.splitlines()
    result_lines = []
    inserted = False
    if method=="below":
        for line in lines:
            result_lines.append(line)
            if not inserted and line.lstrip().startswith(location_keyword):
                result_lines.append(insert_text)
                inserted = True
    elif method=="above":
        for line in lines:
            if not inserted and r"\end{document}" in line:
                result_lines.append(insert_text)
                inserted = True
            result_lines.append(line)

    return "\n".join(result_lines)


def recompose_manuscript(manuscript_path, user_packages, user_commands):
    new_header = "\n".join([user_packages, user_commands])
    manuscript_contents = manuscript_path.read_text(encoding="utf-8")
    manuscript_contents_with_header = _insert_to_manuscript(
        manuscript_contents, new_header, r"\documentclass", "below"
    )
    manuscript_path.write_text(
        manuscript_contents_with_header, encoding="utf-8"
    )

def copy_all_files(source_dir, target_dir):
    """Copies files from a package's resource directory to a target
    directory.

    Parameters:
    ===========
    source_dir : Path
      The source dir from which all the files will be copied, recursively
    project_dir : Path
      The path to the location of the output project where the files
      will be copied to.
    """
    # reuse the code in copy_journal_template_files and then delete that function
    pass

def clone_gh_repo(url):
    """Clone the repo to a temporary location.

    Parameters
    ----------
    url : a url

    Returns
    -------
    The path to the contents of the repo on the local files-system
    """
    pass

def load_headers(headers_path, manuscript_path):
    """Loads usepackages.txt and newcommands.txt into manuscript.tex
    header.

    Updates manuscript.tex headers in place with the contents of the user-files.


    Parameters
    ----------
    headers_path : Path
      The path to the location of the usepackages.txt and newcommands.txt file
    manuscript_path : Path
      The path to the manuscript.tex file

    Returns
    -------
    None
    """
    pass

def load_bib_info(bibs_path, manuscript_path):
    """Finds all bib files and loads the names into the \thebibliography
    field.

    Updates manuscript.tex bibliography in place with the name-list of all bib files

    Parameters
    ----------
    bibs_path : Path
      The path to the location of the bib file.
    manuscript_path : Path
      The path to the manuscript.tex file

    Returns
    -------
    None
    """
    if not manuscript_path.exists():
        raise FileNotFoundError(
        "Unable to find the path: "
        f"{str(manuscript_path)}. Please leave an issue "
        "on GitHub."
        )

    bib_files = []
    for item in bibs_path.glob('**/*'):
        if item.name.endswith(".bib"):
            bib_files.append(item)
    if len(bib_files)==0:
        return

    bib_names = sorted([file.stem for file in bib_files])
    bib_in_repo = r"\bibliography{" + ", ".join(bib_names) + r"}"
    manuscript_text = manuscript_path.read_text()
    bib_in_manuscript, manuscript_without_bib = _split_lines_with_keyword(manuscript_text, r"\bibliography")
    insert_text = bib_in_repo + "\n" + bib_in_manuscript
    manuscript_text_with_all_bib = _insert_to_manuscript(manuscript_without_bib, insert_text, r"\end{document}", "above")
    manuscript_path.write_text(manuscript_text_with_all_bib)



def remove_temporary_files(tmpdir_path):
    pass


def main():
    project_dir = Path().cwd()
    manuscript_path = project_dir / MANUSCRIPT_FILENAME
    if ("{{ cookiecutter.latex_headers_repo_url }}" ==
            "use-scikit-package-default"):
        user_headers_repo_url = \
            "https://github.com/scikit-package/default-latex-headers.git"
    else:
        user_headers_repo_url = "{{ cookiecutter.latex_headers_repo_url }}"
    copy_journal_template_files(
        "{{ cookiecutter.journal_template }}", project_dir
    )
    user_headers = get_user_headers(user_headers_repo_url)
    manuscript_packages = extract_manuscript_packages(manuscript_path)
    user_packages, the_rest = split_usepackage_lines(user_headers)
    all_packages = "\n".join([manuscript_packages, user_packages])
    recompose_manuscript(manuscript_path, all_packages, the_rest)


if __name__ == "__main__":
    main()
