=============
Release notes
=============

.. current developments

0.1.0
=====

**Added:**

* Build user_filesystem for testing in `contest.py`.
* Add workflows form `scikit-package`.
* Add function `copy_all_files` to `post_gen_project.py`.
* Add pre-commit setup, Github release workflow.
* Add function ``load_headers`` to ``post_gen_project.py``.
* Add function ``load_bib_info`` to ``post_gen_project.py``.
* Add function ``initialize_project`` to wrap all other functions in ``main``.

**Fixed:**

* Remove non-latex files in the template to avoid copying duplicate files from user-supplied repo.
