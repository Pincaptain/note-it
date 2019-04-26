import configparser


class _Section:
    """
    Section class represents a single section in the config.ini file
    containing all the key=value pairs for it.
    """

    def __init__(self, section):
        """
        Initializes the values dictionary for the specified section.

        :param section: Single ini section containing key=value pairs. (Dictionary)
        """

        self.values = section

    def __getitem__(self, key):
        """
        Returns a value from a section based on the specified key.

        :param key: Key for a specific value in section. (String)
        :return: Value from section (Dynamic)
        """

        return self.values[key]


class Config:
    """
    Configuration class for obtaining configuration
    settings from config.ini file.

    :cvar _instance: Singleton instance. (Config)
    """

    _instance = None

    @classmethod
    def get_instance(cls):
        """
        The correct class method to obtain the
        singleton instance of Config.

        :param cls: Class of the method (Config)
        :return: Returns an instance of the Config singleton. (Config)
        """

        if not cls._instance:
            cls._instance = Config()

        return cls._instance

    def __init__(self):
        """
       Constructor for Config singleton class.

       Checks if :cvar _instance: is already instantiated
       and if it is it throws an exception.

       If not it instantiates the class and sets the :cvar _instance: to itself.
       """

        if Config._instance:
            raise Exception('Config singleton is already instantiated. User Config.get_instance() obtain it.')

        parser = configparser.ConfigParser()
        parser.read('C:\\Users\\Akatosh\\PythonProjects\\note-it\\config\\config.ini')

        self.sections = {}

        for section in parser:
            self.sections[section] = _Section(parser[section])

        Config._instance = self

    def resolve(self, section, key):
        """
        Resolves/Returns a value from a specified section and a key.

        :param section: The section in the ini file where the key is stored.
        :param key: The key that holds the value required.
        :return: Returns the value based on a section and a key.
        """

        return self.sections[section][key]
