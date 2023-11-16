"""
The storage module is responsible for saving DirectMessage objects
into a DSU file for local usage. In addition, there are functions
for returning the contact's messages to the user and vice versa.
"""

from Profile import DsuFileError
from Profile import Profile
import json
from pathlib import Path
import ds_messenger


class Storage:
    """
    Contains functions that save message objects on a local
    file and retrieve either messages from the contact or sent
    by the user.
    """
    def __init__(self):
        """Initialize Storage."""
        self.dir = "."

    def save_received(self, dm_lst, username, password, server=None):
        """Write the DirectMessage objects into profile dsu file."""
        json_lst = []
        try:
            dsu_name = username + ".dsu"
            p = Path(self.dir) / dsu_name
            p_str = str(p)
            if not p.exists():
                new_file = open(p_str, "x")
                new_file.close()
            profile = Profile(server, username, password)
            profile.load_profile(p_str)
            for dm in dm_lst:
                json_str = json.dumps(dm.__dict__)
                json_lst.append(json_str)
            profile.received = json_lst
            profile.save_profile(p_str)
        except Exception as ex:
            msg = "Error while attempting to process the DSU file."
            print(msg, ex)

    def save_sent(self, username, password, sent_dm, server=None):
        """Write the user sent DirectMessage objects into their profile dsu."""
        json_lst = []
        try:
            dsu_name = username + ".dsu"
            p = Path(self.dir) / dsu_name
            p_str = str(p)
            if not p.exists():
                new_file = open(p_str, "x")
                new_file.close()
            profile = Profile(server, username, password)
            profile.load_profile(p_str)
            json_str = json.dumps(sent_dm.__dict__)
            profile.sent.append(json_str)
            profile.save_profile(p_str)
        except Exception as ex:
            msg = "Error while attempting to process the DSU file."
            print(msg, ex)

    def get_contact_messages(self, friend, username, password, server=None):
        """
        Get dm objects from contact_name in the json storage file.
        Return all corresponding messages in a dictionary with
        timestamp as key.
        """
        recv_dict = {}
        try:
            dsu_name = username + ".dsu"
            p = Path(self.dir) / dsu_name
            p_str = str(p)
            if not p.exists():
                new_file = open(p_str, "x")
                new_file.close()
            profile = Profile(server, username, password)
            profile.load_profile(p_str)
            with open(dsu_name, "r") as recv_file:
                recv_list = profile.received
                for dm in recv_list:
                    dm = json.loads(dm)
                    if dm["recipient"] == friend:
                        recv_dict[float(dm["timestamp"])] = [friend, dm["message"]]
        except Exception as ex:
            msg = "Error while attempting to process the DSU file."
            print(msg, ex)
        return recv_dict

    def get_user_messages(self, contact_name, username, password, server=None):
        """
        Load sent_messages.dsu to return all messages
        corresponding to the specified user and contact.
        Returns messages in their own dictionaries with
        timestamp as the key.
        """
        sent_dict = {}
        try:
            dsu_name = username + ".dsu"
            p = Path(self.dir) / dsu_name
            p_str = str(p)
            if not p.exists():
                new_file = open(p_str, "x")
                new_file.close()
            profile = Profile(server, username, password)
            profile.load_profile(p_str)
            with open(dsu_name, "r") as sent_file:
                sent_list = profile.sent
                for dm in sent_list:
                    dm = json.loads(dm)
                    if dm["recipient"] == contact_name:
                        sent_dict[float(dm["timestamp"])] = [username, dm["message"]]
        except Exception as ex:
            msg = "Error while attempting to process the DSU file."
            print(msg, ex)
        return sent_dict

    def check_new_contact(self, dm_lst, username, password, server=None):
        """
        Return empty list if no new contacts have sent messages,
        else return the names of the senders not on the user's contact
        list.
        """
        new_friends = []
        try:
            dsu_name = username + ".dsu"
            p = Path(self.dir) / dsu_name
            p_str = str(p)
            if not p.exists():
                new_file = open(p_str, "x")
                new_file.close()
            profile = Profile(server, username, password)
            profile.load_profile(p_str)
            for dm in dm_lst:
                json_str = json.dumps(dm.__dict__)
                profile.received.append(json_str)
                ds = json.loads(json_str)
                sender = ds["recipient"]
                if sender not in profile.friend:
                    profile.friend.append(sender)
                    new_friends.append(sender)
            profile.save_profile(p_str)
        except Exception as ex:
            msg = "Error while attempting to process the DSU file."
            print(msg, ex)
        return new_friends
