import discord

from config.config import Config


class DiscordExtension(discord.Client):
    """
    Discord extension/bot to listen
    for discord messages and act accordingly.

    Discord users from the bot server can make requests
    and get responses based on a selection of
    commands understandable to the bot.

    :cvar _instance: Instance of the singleton. (DiscordExtension)
    """

    _instance = None

    @classmethod
    def get_instance(cls):
        """
        The correct class method to obtain the
        singleton instance of DiscordExtension.

        :param cls: Class of the method (DiscordExtension)
        :return: Returns an instance of the DiscordExtension singleton. (DiscordExtension)
        """

        if not cls._instance:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        """
        Constructor for DiscordExtension singleton class.

        Checks if :cvar _instance: is already instantiated
        and if it is it throws an exception.

        If not it instantiates the class and sets the :cvar _instance: to itself.
        """

        if DiscordExtension._instance:
            raise Exception('DiscordExtension instance already exists. '
                            'Use DiscordExtension.get_instance() to obtain it')

        super().__init__()

        # Obtain an instance of the config singleton.
        # Resolve the token using the config instance.
        # Run the discord bot.
        config = Config.get_instance()
        token = config.resolve('extensions.discord', 'token')
        self.run(token)

        DiscordExtension._instance = self


if __name__ == '__main__':
    discord = DiscordExtension.get_instance()
