import nox


@nox.session()
def format(session: nox.Session) -> None:
    session.install("-r", "dev-requirements.txt")
    session.run("pytest", "tests")
