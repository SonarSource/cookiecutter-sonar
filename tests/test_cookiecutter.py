import pathlib


def test_defaults(cookies):
    result = cookies.bake()

    assert result.exit_code == 0
    assert result.exception is None
    project_path: pathlib.Path = result.project_path
    assert project_path.name == 'A repository'
    assert project_path.is_dir()
    assert len(list(project_path.iterdir())) == 4
    assert project_path.joinpath('README.md').is_file()
    assert project_path.joinpath('LICENSE').is_file()
    assert project_path.joinpath('.github', 'CODEOWNERS').is_file()
    assert len(list(project_path.joinpath('.github', 'workflows').iterdir())) == 0


def test_customization(cookies):
    result = cookies.bake(extra_context={
        "repository_name": "Test repository",
        "repository_description": "Test description",
        "repository_visibility": "public",
        "owner_team": "test-team",
        "use_cirrus_ci": "yes",
        "use_release": "yes",
        "use_pre_commit": "yes"
    })

    assert result.exit_code == 0
    assert result.exception is None
    project_path: pathlib.Path = result.project_path
    assert project_path.name == 'Test repository'
    assert project_path.is_dir()
    assert len(list(project_path.iterdir())) == 7
    assert "test-team" in project_path.joinpath('.github', 'CODEOWNERS').read_text()
    assert "Test description" in project_path.joinpath('README.md').read_text()
    assert "GNU LESSER GENERAL PUBLIC LICENSE" in project_path.joinpath('LICENSE').read_text()
    assert len(list(project_path.joinpath('.github', 'workflows').iterdir())) == 2
