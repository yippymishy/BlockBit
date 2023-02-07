"""module with main class to process Local Databases with dictionaries"""
from __future__ import unicode_literals
# Standard library imports
import logging

# Third party imports

# Local imports
from local_simple_database.virtual_class_all_local_databases import \
    VirtualAnyLocalDatabase
from local_simple_database.class_dict_database_handler import \
    DictDatabaseHandler

LOGGER = logging.getLogger("local_simple_database")


class LocalDictDatabase(VirtualAnyLocalDatabase):
    """
    This class was built to handle dictionary DataBase-s

    ...

    Parent Attributes
    -----------------
    self.str_path_main_database_dir : str
        Path to main folder with DataBase-s
    self.str_datetime_template_for_rolling : str
        Datetime template for folder name if to use rolling
    self.list_supported_types : list
        DataBase Types with which this local database can work
    self.dict_file_lock_by_fila_path : dict
        {file_path_1: FileLock object, ...}
    self.float_max_seconds_per_file_operation : float
        Seconds per file operation, need it for multiprocessing safety

    Attributes
    ----------
    self.default_value : object
        Value to use if key in database is not found
    self.dict_db_handler_by_str_db_name : dict
        {database_name: handler ( special object to handle access to one DB)}
    """

    def __init__(
            self,
            str_path_database_dir=".",
            float_max_seconds_per_file_operation=0.01,
            default_value=None,
            str_datetime_template_for_rolling="",
    ):
        """Init DB-s object

        Parameters
        ----------
        str_path_database_dir : str, optional
            Path to main folder with DataBase-s (default is ".")
        float_max_seconds_per_file_operation : float
            Seconds per file operation, need it for multiprocessing safety
        default_value : object, optional
            Value to use if key in database is not found (default is None)
        str_datetime_template_for_rolling : str
            Datetime template for folder name if to use rolling
        """
        # Init class of all local DataBases
        super(LocalDictDatabase, self).__init__(
            str_path_database_dir=str_path_database_dir,
            float_max_seconds_per_file_operation=\
                float_max_seconds_per_file_operation,
            str_datetime_template_for_rolling=\
                str_datetime_template_for_rolling,
        )
        self.list_supported_types = ["dict"]
        self.default_value = default_value
        self.dict_db_handler_by_str_db_name = {}

    def init_new_class_obj(self, **kwargs):
        """Create a new instance of the same class object

        Parameters
        ----------
        """
        return LocalDictDatabase(**kwargs)

    def __getitem__(self, str_db_name):
        """self[database_name]   method for getting DB current value

        Parameters
        ----------
        str_db_name : str
            Name of DataBase which to use
        """
        if str_db_name not in self.dict_db_handler_by_str_db_name:
            self.dict_db_handler_by_str_db_name[str_db_name] = \
                DictDatabaseHandler(
                    self,
                    str_db_name
                )
        return self.dict_db_handler_by_str_db_name[str_db_name]

    def __setitem__(self, str_db_name, dict_values_to_set):
        """self[database_name] = {key_1: value_1, ...} for setting DB value

        Parameters
        ----------
        str_db_name : str
            Name of DataBase which to use
        dict_values_to_set : dict
            Value to set for DB
        """
        assert isinstance(dict_values_to_set, dict), (
            "ERROR: Unable to set for dict DB" +
            " Value with type: " + str(type(dict_values_to_set))
        )
        # Set value for database
        if str_db_name not in self.dict_db_handler_by_str_db_name:
            self.dict_db_handler_by_str_db_name[str_db_name] = \
                DictDatabaseHandler(
                    self,
                    str_db_name
                )
        self.dict_db_handler_by_str_db_name[str_db_name].set_value(
            dict_values_to_set
        )
        LOGGER.debug(
            "For DataBase %s set values: %d",
            str_db_name,
            len(dict_values_to_set)
        )

    def change_default_value(self, new_default_value):
        """Changing default value to use for all DICT DataBase-s

        Parameters
        ----------
        new_default_value : obj
            Value to use if key in database is not found
        """
        self.default_value = new_default_value
        for str_db_name in self.dict_db_handler_by_str_db_name:
            db_handler = self.dict_db_handler_by_str_db_name[str_db_name]
            db_handler.change_default_value(new_default_value)
