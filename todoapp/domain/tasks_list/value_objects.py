from typing import NewType

from pydantic import UUID4

ListId = NewType("ListId", UUID4)
