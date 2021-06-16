import nox
import tempfile


def install_with_constraints(session, *args, **kwargs):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            'poetry',
            'export',
            '--dev',
            '--format=requirements.txt',
            f'--output={requirements.name}',
            '--without-hashes',
            external=True
        )
        session.install(f'--constraint={requirements.name}', *args, **kwargs)


@nox.session(python=['3.8'])
def lint(session):
    args = session.posargs or ['src', 'noxfile.py']
    install_with_constraints(session, 'flake8')
    session.run('flake8', *args)
