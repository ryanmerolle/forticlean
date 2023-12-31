"""Invoke file to define all tasks for this project."""
from invoke import task


@task()
def fmt(ctx):
    """Format project (check only)."""
    fmt_black(ctx)
    fmt_isort(ctx)
    fmt_autoflake(ctx)


@task
def fmt_black(ctx, check=False):
    """Run black (default: check)."""
    if check:
        print("## black (check) ##")
        ctx.run("black . --check")
    else:
        print("## black (auto-fix) ##")
        ctx.run("black .")
    print()


@task
def fmt_autoflake(ctx, check=False):
    """Run autoflake (default: check)."""
    if check:
        print("## autoflake (check) ##")
        ctx.run(
            "autoflake -r . --exclude venv --expand-star-imports --remove-unused-variables --remove-all-unused-imports"
        )
    else:
        print("## autoflake (auto-fix) ##")
        ctx.run(
            "autoflake -vri . --exclude venv --expand-star-imports --remove-unused-variables --remove-all-unused-imports"
        )
    print()


@task
def fmt_isort(ctx, check=False):
    """Run isort (default: check)."""
    if check:
        print("## isort (check) ##")
        ctx.run("isort . -c")
    else:
        print("## isort (auto-fix) ##")
        ctx.run("isort .")
    print()


@task
def lint(ctx):
    """Lint."""
    lint_bandit(ctx)
    lint_flake8(ctx)
    lint_pydoc(ctx)
    lint_yaml(ctx)
    lint_mypy(ctx)


@task
def lint_bandit(ctx):
    """Run bandit."""
    print("## bandit ##")
    ctx.run('bandit -r . -c "pyproject.toml"')
    print()


@task
def lint_flake8(ctx):
    """Run flake8."""
    print("## flake8 ##")
    ctx.run("flake8 .")
    print()


@task
def lint_pydoc(ctx):
    """Run pydocstyle."""
    print("## pydocstyle ##")
    ctx.run("pydocstyle .")
    print()


@task
def lint_yaml(ctx):
    """Run yamllint."""
    print("## yamllint ##")
    ctx.run("yamllint .")
    print()


@task
def lint_mypy(ctx):
    """Run mypy."""
    print("## mypy ##")
    ctx.run("mypy .")
    print()


@task
def all(ctx):
    """Format & lint project."""
    fmt(ctx)
    lint(ctx)
