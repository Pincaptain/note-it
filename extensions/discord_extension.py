import json

import discord

from config.config import Config
from repositories.note_repository import NoteRepository
from models.note import Note


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

        self.note_repository = NoteRepository('omnividence')

        # Obtain an instance of the config singleton.
        # Resolve the token using the config instance.
        # Run the discord bot.
        config = Config.get_instance()
        token = config.resolve('extensions.discord', 'token')
        self.run(token)

        DiscordExtension._instance = self

    async def on_ready(self):
        """
        Event function that is called once the discord
        bot is ready to listen.

        The function is called only once on the start
        and it is a very good sign that everything is functional.
        """

        print('Discord client initialized.')
        print('Listening for messages....')
        print('')

    async def on_message(self, message):
        """
        The function is called for every new message written in the discord
        server your bot is on.

        :param message: Instance of the discord message sent.
        """

        # Read the content of the message
        content = str(message.content)

        # If the content starts with !ni it is a message for the bot
        if content.startswith('!ni'):
            # Split the content in params
            params = content.split(':')

            # Check if the parameters contain a keyword
            if len(params) <= 1:
                await self.error(message, 'Invalid number of parameters! Type !ni:help for more info.')

                return

            # Act based on the keyword parameter
            keyword = params[1]

            if keyword == 'add':
                await self.add(message, params)
            elif keyword == 'patch':
                await self.patch(message, params)
            elif keyword == 'delete':
                await self.delete(message, params)
            elif keyword == 'help':
                await self.help(message)
            else:
                await self.error(message, 'Command not found. Use "!ni help" for more info!')

    async def add(self, message: discord.Message, params: list):
        """
        Adds a note to the database using the provided parameters.

        :param message: Instance of the discord message that triggered the error. (discord.Message)
        :param params: Message parameters/note attributes. (List[String])
        :return: Returns the created note.
        """

        if len(params) != 5:
            await self.error(message, 'Add command takes exactly 3 parameters!')

            return

        title = params[2]
        body = params[3]
        tags = params[4].split(',')
        note = Note(
            title=title,
            body=body,
            tags=tags,
            author=message.author.name
        )
        note = self.note_repository.create(note)
        response = note.to_json()

        await message.author.send(response)

    async def delete(self, message: discord.Message, params: list):
        """
        Deletes a note from the database using the provided note id.

        :param message: Instance of the discord message that triggered the error. (discord.Message)
        :param params: Message parameters/note attributes. (List[String])
        :return: Returns the number of deleted notes.
        """

        if len(params) != 3:
            await self.error(message, 'Delete command takes exactly 1 parameters!')

            return

        id = params[2]
        note = self.note_repository.get(id=id)

        if note.author == message.author.name:
            deleted = self.note_repository.delete(id=id)

            response = json.dumps({
                'deleted': deleted
            })

            await message.author.send(response)
        else:
            response = json.dumps({
                'error': 'This is not your note to delete!'
            })

            await message.author.send(response)

    async def patch(self, message: discord.Message, params: list):
        """
        Updates a note from the database using the provided parameters.

        :param message: Instance of the discord message that triggered the error. (discord.Message)
        :param params: Message parameters/note attributes. (List[String])
        :return: Returns the number of deleted notes.
        """

        if len(params) != 6:
            await self.error(message, 'Patch command takes exactly 4 parameters!')

            return

        id = params[2]
        title = params[3]
        body = params[4]
        tags = params[5].split(',')

        note = self.note_repository.get(id=id)

        if note.author == message.author.name:
            updated = self.note_repository.update(id, set__title=title, set__body=body, set__tags=tags)

            response = json.dumps({
                'updated': updated
            })

            await message.author.send(response)
        else:
            response = json.dumps({
                'error': 'This is not your note to patch!'
            })

            await message.author.send(response)

    async def help(self, message: discord.Message):
        """
        Returns an array of commands available at the moment.

        :param message: Instance of the discord message that triggered the error. (discord.Message)
        """

        response = json.dumps({
            'commands': [
                '!ni:help - Lists all the available commands.',
                '!ni:add:${title}:${body}:${tags(a,b)} - Adds a new note to the database.',
                '!ni:delete:${id} - Removes a note from the database.',
                '!ni:patch:${id}:${title}:${body}:${tags(a,b)} - Updates a note from the database.'
            ]
        })

        await message.author.send(response)

    async def error(self, message: discord.Message, error: str):
        """
        Returns an error response with :param error: message to the client.

        :param message: Instance of the discord message that triggered the error. (discord.Message)
        :param error: Error text. (String)
        """

        response = json.dumps({
            'error': 'Invalid request parameters. Make sure that you formatted your message correctly!'
        })

        await message.author.send(response)


if __name__ == '__main__':
    discord = DiscordExtension.get_instance()
