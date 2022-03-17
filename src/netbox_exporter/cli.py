from .exporter import Exporter
from .fetcher import Fetcher

import click
import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)


@click.command()
@click.option(
    '--token', '-t',
    help="API auth-token",
    required=True,
)
@click.option(
    '--url', '-u', '-s',
    help="Netbox URL",
    required=True,
)
@click.option(
    '--dir', '-d', 'dir_',
    help="Destination directory",
    default="netbox",
)
def main(token, url, dir_):
    """Fetch and export you Netbox inventory to a local directory."""

    fetcher = Fetcher(url, token)
    exporter = Exporter(dir_)

    for ctx_prefix, prefix_url in fetcher.fetch_index().items():
        for ctx_suffix, url in fetcher.fetch_index(prefix_url).items():
            ctx = f"{ctx_prefix}/{ctx_suffix}"
            data = fetcher.fetch_data(url)
            exporter.dump(ctx, data)
