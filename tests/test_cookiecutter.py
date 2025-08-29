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

def test_public_repository_hooks(cookies):
    """Test post-generation hooks for public repository - should remove SECURITY.md and use LGPL license"""
    result = cookies.bake(extra_context={
        "repository_name": "Public Test Repo",
        "repository_description": "Test public repository",
        "repository_visibility": "public",
        "owner_team": "test-team",
        "use_github_actions_ci": "yes",
        "use_release": "no",
        "use_pre_commit": "no"
    })
    
    assert result.exit_code == 0
    project_path: pathlib.Path = result.project_path
    
    # SECURITY.md should be removed for public repos
    assert not project_path.joinpath('SECURITY.md').exists()
    # Should use LGPL license for public repos
    license_content = project_path.joinpath('LICENSE').read_text()
    assert "GNU LESSER GENERAL PUBLIC LICENSE" in license_content

def test_internal_repository_hooks(cookies):
    """Test post-generation hooks for internal repository - should keep SECURITY.md and use SonarSource license"""
    result = cookies.bake(extra_context={
        "repository_name": "Internal Test Repo", 
        "repository_description": "Test internal repository",
        "repository_visibility": "internal",
        "owner_team": "test-team",
        "use_github_actions_ci": "yes",
        "use_release": "no",
        "use_pre_commit": "no"
    })
    
    assert result.exit_code == 0
    project_path: pathlib.Path = result.project_path
    
    # SECURITY.md should exist for internal repos  
    assert project_path.joinpath('SECURITY.md').exists()
    # Should use SonarSource license for internal repos
    license_content = project_path.joinpath('LICENSE').read_text()
    assert "SonarSource" in license_content

def test_release_workflow_hooks(cookies):
    """Test that release workflow is only created when enabled"""
    # Test with release disabled
    result_no_release = cookies.bake(extra_context={
        "repository_name": "No Release Repo",
        "repository_visibility": "private", 
        "owner_team": "test-team",
        "use_github_actions_ci": "yes",
        "use_release": "no",
        "use_pre_commit": "no"
    })
    
    assert result_no_release.exit_code == 0
    workflows_dir = result_no_release.project_path.joinpath('.github', 'workflows')
    workflow_files = list(workflows_dir.iterdir())
    workflow_names = [f.name for f in workflow_files]
    
    # Should have build.yml and pr-cleanup.yml but not release.yml
    assert 'build.yml' in workflow_names
    assert 'pr-cleanup.yml' in workflow_names  
    assert 'release.yml' not in workflow_names
    assert len(workflow_files) == 2

def test_pre_commit_workflow_hooks(cookies):
    """Test that pre-commit files are only created when enabled"""
    # Test with pre-commit disabled  
    result_no_precommit = cookies.bake(extra_context={
        "repository_name": "No Precommit Repo",
        "repository_visibility": "private",
        "owner_team": "test-team", 
        "use_github_actions_ci": "yes",
        "use_release": "no",
        "use_pre_commit": "no"
    })
    
    assert result_no_precommit.exit_code == 0
    project_path = result_no_precommit.project_path
    
    # Pre-commit files should not exist
    assert not project_path.joinpath('.github', 'workflows', 'pre-commit.yml').exists()
    assert not project_path.joinpath('.pre-commit-config.yaml').exists()
    assert not project_path.joinpath('.markdownlint.yaml').exists()
