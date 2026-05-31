"""Template registry — add a new module here to register a new template."""

from diamond_setup._types import TemplateDict

from .genesis import TEMPLATE as GENESIS_TEMPLATE
from .implosive_origin import TEMPLATE as IMPLOSIVE_ORIGIN_TEMPLATE
from .minimal import TEMPLATE as MINIMAL_TEMPLATE

REGISTRY: dict[str, TemplateDict] = {
    "minimal": MINIMAL_TEMPLATE,
    "genesis": GENESIS_TEMPLATE,
    "implosive-origin": IMPLOSIVE_ORIGIN_TEMPLATE,
}

__all__ = ["REGISTRY"]
