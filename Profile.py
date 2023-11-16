import json
import time
from pathlib import Path


"""
DsuFileError is a custom exception handler that you should catch in your own
code. It is raised when attempting to load or save Profile objects to file
the system.

"""


class DsuFileError(Exception):
    pass


"""
DsuProfileError is a custom exception handler that you should catch in your
own code. It is raised when attempting to deserialize a dsu file to a Profile
object.

"""


class DsuProfileError(Exception):
    pass


class Profile:
    """
    The Profile class exposes the properties required to join an ICS 32
    DSU server. You will need to use this class to manage the information
    provided by each new user created within your program for a2. Pay close
    attention to the properties and functions in this class as you will
    need to make use of each of them in your program.

    When creating your program you will need to collect user input for the
    properties exposed by this class. A Profile class should ensure that a
    username and password are set, but contains no conventions to do so.
    You should make sure that your code verifies that required properties
    are set.

    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.bio = ''
        self.friend = []
        self.received = []
        self.sent = []


    def add_friend(self, name) -> None:
        self.friend.append(name)

    """

    save_profile accepts an existing dsu file to save the current instance
    of Profile to the file system.

    Example usage:

    profile = Profile()
    profile.save_profile('/path/to/file.dsu')

    Raises DsuFileError

    """
    def save_profile(self, path: str) -> None:
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                msg = "Error while attempting to process the DSU file."
                print(msg)
        else:
            print("Error: Invalid DSU file path or type")

    """

    load_profile will populate the current instance of Profile with data stored
    in a DSU file.

    Example usage:

    profile = Profile()
    profile.load_profile('/path/to/file.dsu')

    Raises DsuProfileError, DsuFileError

    """
    def load_profile(self, path: str) -> None:
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                self.friend = obj['friend']
                self.received = obj['received']
                self.sent = obj['sent']
                f.close()
            except Exception as ex:
                print("ERROR:", ex)
        else:
            print("ERROR: file does not exist or not a DSU file.")
