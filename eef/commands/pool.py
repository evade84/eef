from typer import Argument, Option, Typer, confirm, style

from eef import headtail, output
from eef.node_client import NodeClient

app = Typer()


@app.command("new", help="Create a new pool.")
def pool_new(
    tag: str = Argument(None, help="Pool tag."),
    master_key: str = Option(None, "--master-key", "-mk", help="Pool master key."),
    reader_key: str = Option(None, "--reader-key", "-rk", help="Pool reader key."),
    creator: str = Option(
        None, "--creator", "-c", help="Signature of the pool creator."
    ),
    description: str = Option(None, "--description", "-d", help="Pool description."),
    indexable: bool = Option(
        False, "--indexable", "-i", help="Will the pool be indexable?"
    ),
    yes: bool = Option(False, "--yes", "-y", help="Confirm pool creation."),
):
    if indexable and reader_key:
        output.error("pool with reader key cannot be indexable.", terminate=True)
    if reader_key and not master_key:
        output.error("pool with reader key must have master key.", terminate=True)
    if not yes:
        output.info(
            style("You are going to create a new pool:\n\n", bold=True)
            + f"tag: {output.pretty_tag(tag)}\n"
            f"description: {output.pretty_description(description)}\n"
            f"creator: {output.pretty_signature(creator)}\n"
            f"indexable: {output.pretty_bool(indexable, invert=True)}\n"
            f"master key is required to write: {output.pretty_bool(bool(master_key))}\n"
            f"reader or master key is required to read: {output.pretty_bool(bool(reader_key))}\n"
        )
        confirm("Continue?", default=True, abort=True)
    pool = NodeClient().pool_new(
        tag=tag,
        master_key=master_key,
        reader_key=reader_key,
        creator=creator,
        description=description,
        indexable=indexable,
    )
    output.info(f"Created a new pool: {pool.address}")


@app.command("list", help="List indexable pools.")
def pool_list(
    head: int = Option(None, "--head", "-h", help="Get first n pools."),
    tail: int = Option(None, "--tail", "-t", help="Get last n pools."),
):
    first, last = headtail.handle(head, tail)
    pools = NodeClient().pool_list(first=first, last=last)
    if pools.total == 0:
        output.info("There are no indexable pools at this node.", terminate=True)

    output.info(f"Showing {output.pretty_first_last(first, last)} {pools.total} indexable pools:")
    for pool in pools.pools:
        output.info(
            f"{output.pretty_address(pool.address)}:\n"
            f"\t{output.pretty_description(pool.description)}\n\n"
            f"\ttag: {output.pretty_tag(pool.tag)}\n"
            f"\tcreated by: {output.pretty_signature(pool.creator)}\n"
            f"\tmaster key is required to write: {output.pretty_bool(pool.write_key_required, invert=True)}\n"
        )


@app.command("info", help="Get information about pool.")
def pool_info(
    identifier: str = Argument(..., help="Pool identifier."),
    master_key: str = Option(None, "--master-key", "-mk", help="Pool master key."),
    reader_key: str = Option(None, "--reader-key", "-rk", help="Pool reader key."),
):
    pool = NodeClient().pool_info(identifier, master_key, reader_key)
    output.info(
        f"{output.pretty_address(pool.address)}:\n"
        f"{output.pretty_description(pool.description)}\n\n"
        f"tag: {output.pretty_tag(pool.tag)}\n"
        f"created by: {output.pretty_signature(pool.creator)}\n"
        f"indexable: {output.pretty_bool(pool.indexable, invert=True)}\n\n"
        f"master key is required to write: {output.pretty_bool(bool(pool.write_key_required))}\n"
        f"master or reader key is required to read: {output.pretty_bool(bool(pool.read_key_required))}\n"
    )


@app.command("read", help="Read messages from pool.")
def pool_read(
    identifier: str = Argument(..., help="Pool identifier."),
    master_key: str = Option(None, "--master-key", "-mk", help="Pool master key."),
    reader_key: str = Option(None, "--reader-key", "-rk", help="Pool reader key."),
    head: int = Option(None, "--head", "-h", help="Get first n messages."),
    tail: int = Option(None, "--tail", "-t", help="Get last n messages."),
):
    first, last = headtail.handle(head, tail)
    messages = NodeClient().pool_read(
        identifier=identifier,
        first=first,
        last=last,
        master_key=master_key,
        reader_key=reader_key,
    )
    if messages.total == 0:
        output.info("Pool does not have any messages.", terminate=True)
    output.info(
        f"Reading pool {identifier} {output.pretty_first_last(first, last)} {messages.total} messages:"
    )
    for message in messages.messages:
        output.info(f"{output.pretty_signature(message.signature)}: {message.text}")


@app.command("write", help="Write a message to pool.")
def pool_write(
    identifier: str = Argument(..., help="Pool identifier."),
    text: str = Argument(..., help="Message text."),
    signature: str = Option(None, "--from", "-f", help="Message author signature."),
    master_key: str = Option(None, "--master-key", "-mk", help="Pool master key."),
):
    message = NodeClient().pool_write(
        identifier=identifier, text=text, signature=signature, master_key=master_key
    )
    output.info(
        "Wrote a new message to the pool:\n"
        f"{output.pretty_signature(message.signature)}: {message.text}"
    )
