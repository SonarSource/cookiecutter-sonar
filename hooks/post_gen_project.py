#!/usr/bin/env python
import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

def set_security():
    visibility = '{{ cookiecutter.repository_visibility }}'
    if visibility == "public":
        os.remove(os.path.join(PROJECT_DIRECTORY, 'SECURITY.md'))

def set_license():
    visibility = '{{ cookiecutter.repository_visibility }}'
    if visibility in ("private", "internal"):
        shutil.move(os.path.join(PROJECT_DIRECTORY, 'licenses/sonarsource.txt'), os.path.join(PROJECT_DIRECTORY, 'LICENSE'))
    elif visibility == "public":
        shutil.move(os.path.join(PROJECT_DIRECTORY, 'licenses/lgpl-3.0.txt'), os.path.join(PROJECT_DIRECTORY, 'LICENSE'))
    else:
        raise ValueError(f"Invalid repository visibility: {visibility}")
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, 'licenses'))

def use_cirrus_ci():
    _use_cirrus_ci = '{{ cookiecutter.use_cirrus_ci }}'
    if _use_cirrus_ci != 'yes':
        os.remove(os.path.join(PROJECT_DIRECTORY, '.cirrus.yml'))
        os.remove(os.path.join(PROJECT_DIRECTORY, '.cirrus.star'))

def use_release():
    _use_release = '{{ cookiecutter.use_release }}'
    if _use_release != 'yes':
        os.remove(os.path.join(PROJECT_DIRECTORY, '.github', 'workflows', 'release.yml'))

def use_pre_commit():
    _use_pre_commit = '{{ cookiecutter.use_pre_commit }}'
    if _use_pre_commit != 'yes':
        os.remove(os.path.join(PROJECT_DIRECTORY, '.github', 'workflows', 'pre-commit.yml'))
        os.remove(os.path.join(PROJECT_DIRECTORY, '.pre-commit-config.yaml'))
        os.remove(os.path.join(PROJECT_DIRECTORY, '.markdownlint.yaml'))

def main():
    set_security()
    set_license()
    use_cirrus_ci()
    use_release()
    use_pre_commit()

if __name__ == "__main__":
    main()
