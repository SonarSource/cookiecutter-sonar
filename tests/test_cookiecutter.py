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
    assert len(list(project_path.joinpath('.github', 'workflows').iterdir())) == 2

def test_customization(cookies):
    result = cookies.bake(extra_context={
        "repository_name": "Test repository",
        "repository_description": "Test description",
        "repository_visibility": "public",
        "owner_team": "test-team",
        "use_github_actions_ci": "yes",
        "use_release": "yes",
        "use_pre_commit": "yes"
    })

    assert result.exit_code == 0
    assert result.exception is None
    project_path: pathlib.Path = result.project_path
    assert project_path.name == 'Test repository'
    assert project_path.is_dir()
    # With all options enabled: README.md, LICENSE, .github/, .pre-commit-config.yaml, .markdownlint.yaml = 5 files
    assert len(list(project_path.iterdir())) == 5
    assert "test-team" in project_path.joinpath('.github', 'CODEOWNERS').read_text()
    assert "Test description" in project_path.joinpath('README.md').read_text()
    assert "GNU LESSER GENERAL PUBLIC LICENSE" in project_path.joinpath('LICENSE').read_text()
    # When all options enabled: build.yml, pr-cleanup.yml, pre-commit.yml, release.yml = 4 files
    assert len(list(project_path.joinpath('.github', 'workflows').iterdir())) == 4

def test_no_github_actions_ci(cookies):
    result = cookies.bake(extra_context={
        "repository_name": "No Actions Repository",
        "repository_description": "Test repository without GitHub Actions CI",
        "repository_visibility": "private",
        "owner_team": "test-team",
        "use_github_actions_ci": "no",
        "use_release": "no",
        "use_pre_commit": "no"
    })

    assert result.exit_code == 0
    assert result.exception is None
    project_path: pathlib.Path = result.project_path
    assert project_path.name == 'No Actions Repository'
    assert project_path.is_dir()

    # When use_github_actions_ci is "no", CI workflow files should be removed by post_gen_project.py
    workflows_dir = project_path.joinpath('.github', 'workflows')
    if workflows_dir.exists():
        assert len(list(workflows_dir.iterdir())) == 0
    # If workflows directory doesn't exist, that's also acceptable (no workflows to create)
