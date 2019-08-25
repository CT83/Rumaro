import click

from apis.instagram_user import InstagramUser
from apis.run_analysis import run_analysis


@click.command()
@click.option('--instagram_id', help="Who's instagram would you like to analyze?")
def cli(instagram_id):
    insta_user = InstagramUser(instagram_id=instagram_id)
    run_analysis(insta_user)


if __name__ == '__main__':
    cli()
