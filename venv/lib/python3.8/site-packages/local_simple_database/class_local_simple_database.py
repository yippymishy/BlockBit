"""Module with class to handle all simple local databases"""
from __future__ import unicode_literals
# Standard library imports
import logging
import datetime

# Third party imports
import dateutil.parser as parser

# Local imports
from local_simple_database.virtual_class_all_local_databases import \
    VirtualAnyLocalDatabase

LOGGER = logging.getLogger("local_simple_database")
LIST_ALL_SUPPORTED_TYPES = ["int", "float", "str", "datetime", "date"]

class LocalSimpleDatabase(VirtualAnyLocalDatabase):
    """
    This class was built to handle all one value DataBase-s

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
    self.dict_str_db_type_by_str_db_name : dict
        {database_1_name: str_value_type, ...}
    self.dict_list_db_allowed_types_by_str_db_name : dict
        {database_1_name: list_allowed_types_for_set_value, ...}
    self.dict_func_db_getter_by_str_db_name : dict
        {database_1_name: func_to_convert_str_to_value, ...}
    self.dict_func_db_setter_by_str_db_name : dict
        {database_1_name: func_to_convert_value_to_str, ...}
    """

    def __init__(
            self,
            str_path_database_dir=".",
            float_max_seconds_per_file_operation=0.01,
            str_datetime_template_for_rolling="",
    ):
        """Init DB-s object

        Parameters
        ----------
        str_path_database_dir : str, optional
            Path to main folder with DataBase-s (default is ".")
        float_max_seconds_per_file_operation : float
            Seconds per file operation, need it for multiprocessing safety
        str_datetime_template_for_rolling : str
            Datetime template for folder name if to use rolling
        """
        # Init class of all local DataBases
        super(LocalSimpleDatabase, self).__init__(
            str_path_database_dir=str_path_database_dir,
            float_max_seconds_per_file_operation=\
                float_max_seconds_per_file_operation,
            str_datetime_template_for_rolling=\
                str_datetime_template_for_rolling,
        )
        self.list_supported_types = LIST_ALL_SUPPORTED_TYPES
        self.dict_func_db_getter_by_str_db_name = {}
        self.dict_func_db_setter_by_str_db_name = {}
        self.dict_str_db_type_by_str_db_name = {}
        self.dict_list_db_allowed_types_by_str_db_name = {}

    def init_new_class_obj(self, **kwargs):
        """Create a new instance of the same class object

        Parameters
        ----------
        """
        return LocalSimpleDatabase(**kwargs)

    def __getitem__(self, str_db_name):
        """self[database_name]   method for getting DB current value

        Parameters
        ----------
        str_db_name : str
            Name of DataBase which to use
        """
        if str_db_name not in self.dict_func_db_getter_by_str_db_name:
            self.init_new_simple_database(str_db_name)
        str_db_content = self.read_file_content(str_db_name)
        func_getter = self.dict_func_db_getter_by_str_db_name[str_db_name]
        return func_getter(str_db_content)

    def __setitem__(self, str_db_name, value_to_set):
        """self[database_name] = x   method for setting DB value

        Parameters
        ----------
        str_db_name : str
            Name of DataBase which to use
        value_to_set : object
            Value to set for DB
        """
        #####
        if str_db_name not in self.dict_func_db_setter_by_str_db_name:
            self.init_new_simple_database(str_db_name)
        # Check that value to set has suitable type
        list_allowed_type = \
            self.dict_list_db_allowed_types_by_str_db_name[str_db_name]
        assert isinstance(value_to_set, tuple(list_allowed_type)), (
            "ERROR: Unable to set for DB with type: " +
            str(self.dict_str_db_type_by_str_db_name[str_db_name]) +
            " Value with type: " + str(type(value_to_set))
            )
        # Get setter converter and save value
        func_setter = self.dict_func_db_setter_by_str_db_name[str_db_name]
        str_value_to_save = func_setter(value_to_set)
        self.save_file_content(
            str_value_to_save,
            str_db_name
        )
        LOGGER.debug(
            "For DataBase %s set value: %s", str_db_name, str_value_to_save
        )

    def init_new_simple_database(self, str_db_name):
        """Method for first preparings for new database

        Parameters
        ----------
        str_db_name : str
            Name of DataBase which to use
        """
        # assert isinstance(str_db_name, str), (
        #     "ERROR: DataBase name should have type str, now it is: " +
        #     str(type(str_db_name))
        # )
        assert str_db_name, "ERROR: Database name should not be empty"
        #####
        # If DB already initialized then finish execution
        assert str_db_name not in self.dict_str_db_type_by_str_db_name,\
            "ERROR: DB {} is not defined, but shouldn't be so.".format(
                str_db_name
            )
        #####
        # Check that name of DataBase is correct
        LOGGER.debug("Try to init new DB: %s", str_db_name)
        str_db_type = self.define_type_of_db_by_name(str_db_name)
        LOGGER.debug("DB type: %s", str_db_type)
        if str_db_type not in self.list_supported_types:
            raise KeyError(
                "Unable to init database with name: " + str_db_name +
                " As database type: " + str_db_type +
                " NOT in the list of allowed types:  " +
                str(self.list_supported_types)
            )
        #####
        # Init new DataBase
        self.dict_str_db_type_by_str_db_name[str_db_name] = str_db_type
        LOGGER.debug(
            "Initialize new database with name %s With type of values: %s",
            str_db_name,
            str(str_db_type).upper()
        )
        #####
        # int
        if str_db_type == "int":
            self.dict_list_db_allowed_types_by_str_db_name[str_db_name] = \
                [int]
            def getter(str_f_content):
                if not str_f_content:
                    return int()
                return int(str_f_content)
            self.dict_func_db_getter_by_str_db_name[str_db_name] = getter
            self.dict_func_db_setter_by_str_db_name[str_db_name] = \
                lambda value_to_set: "%d" % value_to_set
        #####
        # float
        elif str_db_type == "float":
            self.dict_list_db_allowed_types_by_str_db_name[str_db_name] = \
                [int, float]
            def getter(str_f_content):
                if not str_f_content:
                    return float()
                return float(str_f_content)
            self.dict_func_db_getter_by_str_db_name[str_db_name] = getter
            self.dict_func_db_setter_by_str_db_name[str_db_name] = \
                lambda value_to_set: "%d" % value_to_set
        #####
        # str
        elif str_db_type == "str":
            self.dict_list_db_allowed_types_by_str_db_name[str_db_name] = \
                [str]
            self.dict_func_db_getter_by_str_db_name[str_db_name] = str
            self.dict_func_db_setter_by_str_db_name[str_db_name] = str
            # self.dict_func_db_getter_by_str_db_name[str_db_name] = \
            #     lambda str_f_content: str(str_f_content)
            # self.dict_func_db_setter_by_str_db_name[str_db_name] = \
            #     lambda value_to_set: str(value_to_set)
        #####
        # datetime
        elif str_db_type == "datetime":
            self.dict_list_db_allowed_types_by_str_db_name[str_db_name] = \
                [datetime.date]
            def getter(str_f_content):
                if not str_f_content:
                    dt_obj = datetime.datetime(1970, 1, 1)
                    dt_obj = dt_obj.replace(tzinfo=datetime.timezone.utc)
                    return dt_obj
                try:
                    return datetime.datetime.fromisoformat(str_f_content)
                except (ValueError, AttributeError):
                    return parser.parse(str_f_content)
            self.dict_func_db_getter_by_str_db_name[str_db_name] = getter
            self.dict_func_db_setter_by_str_db_name[str_db_name] = \
                lambda value_to_set: str(value_to_set.isoformat())
        #####
        # date
        elif str_db_type == "date":
            self.dict_list_db_allowed_types_by_str_db_name[str_db_name] = \
                [datetime.date]
            def getter(str_f_content):
                if not str_f_content:
                    dt_obj = datetime.datetime(1970, 1, 1)
                    dt_obj = dt_obj.replace(tzinfo=datetime.timezone.utc)
                    return dt_obj.date()
                try:
                    return \
                        datetime.datetime.fromisoformat(str_f_content).date()
                except (ValueError, AttributeError):
                    return parser.parse(str_f_content)
            self.dict_func_db_getter_by_str_db_name[str_db_name] = getter
            self.dict_func_db_setter_by_str_db_name[str_db_name] = \
                lambda value_to_set: str(value_to_set.isoformat())
