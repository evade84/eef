from typing import Optional

from eef.output import error


def handle(
    head: Optional[int] = None, tail: Optional[int] = None
) -> tuple[int | None, int | None]:
    if head and tail:
        error("head and tail options can't be both used at once.", terminate=True)
    if not head and not tail:
        tail = 50
    return head, tail
