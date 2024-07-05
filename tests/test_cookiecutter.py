def test_defaults(cookies):
    result = cookies.bake()

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'A repository'
    assert result.project.isdir()
    assert len(result.project.listdir()) == 3
    assert result.project.join('README.md').isfile()
    assert result.project.join('LICENSE').isfile()
    assert result.project.join('.github', 'CODEOWNERS').isfile()
    assert len(result.project.join('.github', 'workflows').listdir()) == 0


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
    assert result.project.basename == 'Test repository'
    assert result.project.isdir()
    assert len(result.project.listdir()) == 7
    assert "test-team" in result.project.join('.github', 'CODEOWNERS').read()
    assert "Test description" in result.project.join('README.md').read()
    assert "GNU LESSER GENERAL PUBLIC LICENSE" in result.project.join('LICENSE').read()
    assert len(result.project.join('.github', 'workflows').listdir()) == 2
