
# Standard library imports
# Third party imports

# Local imports
from local_simple_database.class_local_simple_database import \
    LocalSimpleDatabase
from local_simple_database.class_local_dict_database import \
    LocalDictDatabase


__all__ = [
    "LocalSimpleDatabase",
    "LocalDictDatabase"

]


#####
# Prepare basic logger in case user is not setting it itself.
#####
import logging
LOGGER = logging.getLogger("local_simple_database")
LOGGER.addHandler(logging.NullHandler())
