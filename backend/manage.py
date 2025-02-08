import subprocess

import click


@click.group()
def cli():
    pass


@cli.command()
def runtests():
    click.echo("Run tests")
    subprocess.call("pytest tests/ --log-cli-level=INFO".split())


@cli.command()
def coverage():
    click.echo("Tests Coverage")
    subprocess.call("coverage run -m pytest --log-cli-level=INFO".split())
    subprocess.call("coverage report".split())


@cli.command()
def drop():
    click.echo("Drop Tables")

    find_command = ["find", "../docker/", "-name", "docker-compose.dev.yml"]
    result = subprocess.check_output(find_command).decode().strip()
    realpath_command = ["realpath", result]
    full_path = subprocess.check_output(realpath_command).decode().strip()
    project_name = full_path.split("/")[-2].lower()

    for volume in [
        i.decode() for i in subprocess.check_output("docker volume ls".split()).split()
    ]:
        if project_name in volume:
            subprocess.call("docker compose down".split())
            subprocess.call(f"docker volume rm {volume}".split())


@cli.command()
@click.option("--env_file", default="", help="env_file path.")
@click.option("--nginx", is_flag=True, help="Start Nginx")
@click.option("-d", is_flag=True, help="Daemon")
def runserver(env_file: str, nginx: bool, d):
    click.echo("Server starting")
    cmd = "docker-compose -f ../deploy/docker-compose.dev.yml up --build"
    if env_file:
        cmd += f"env ENV={env_file} "
    if nginx:
        cmd += " --scale nginx=1"
    if d:
        cmd += " -d"
    subprocess.call(cmd.split())
    click.echo("Server was started")


"""
ENV=.localenv docker-compose -f ../deploy/docker-compose.dev.yml up --build --scale nginx=1
"""

if __name__ == "__main__":
    cli()
