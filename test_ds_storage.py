"""
Unittest module to test that ds_storage can
manage and access stored message data correctly.
"""

import unittest
import ds_messenger
import ds_storage
import json
from Profile import Profile
from pathlib import Path


class DS_storage_tester(unittest.TestCase):
    """
    Contains unittests to test that ds_storage
    functions work as intended when accessing local
    file data.
    """
    def test_save_receieved(self):
        """Test that DirectMessage objects are stored successfully."""
        ds = ds_messenger.DirectMessenger("168.235.86.101", "mrsmiggles331", "password")
        obj_lst = ds.retrieve_all()
        length_obj_lst = len(obj_lst)
        store = ds_storage.Storage()
        store.save_received(obj_lst, "mrsmiggles133", "password")
        with open("mrsmiggles133.dsu", "r") as recv_file:
            contents = recv_file.read()
            json_obj = json.loads(contents)
            msg_cnt = len(json_obj["received"])
        self.assertEqual(msg_cnt, length_obj_lst)

    def test_save_sent(self):
        """Test that saving messages sent by the user is stored succesfully."""
        ds = ds_messenger.DirectMessenger("168.235.86.101", "mrsmiggles133", "password")
        ds.send("test message", "test331")
        store = ds_storage.Storage()
        store.save_sent("mrsmiggles133", "password", ds.sent)
        with open("mrsmiggles133.dsu", "r") as sent_file:
            contents = sent_file.read()
            json_obj = json.loads(contents)
            newest_sent = json.loads(json_obj["sent"][-1])["message"]
        self.assertEqual(newest_sent, "test message")

    def test_get_contact_messages(self):
        """Test that the contact's messages can be retrieved."""
        contact = ds_messenger.DirectMessenger("168.235.86.101", "test331", "password")
        contact.send("test contact message", "mrsmiggles133")
        user = ds_messenger.DirectMessenger("168.235.86.101", "mrsmiggles133", "password")
        dm_lst = user.retrieve_all()
        store = ds_storage.Storage()
        store.save_received(dm_lst, "mrsmiggles133", "password")
        recv_dict = store.get_contact_messages("test331", "mrsmiggles133", "password")
        newest_recv = list(recv_dict.values())[-1]
        newest_msg = newest_recv[1]
        self.assertEqual(newest_msg, "test contact message")

    def test_get_user_messages(self):
        """
        Test that the user's messages to the specified contact
        can be retrieved.
        """
        user = ds_messenger.DirectMessenger("168.235.86.101", "mrsmiggles133", "password")
        user.send("test user message", "test331")
        store = ds_storage.Storage()
        store.save_sent("mrsmiggles133", "password", user.sent)
        sent_dict = store.get_user_messages("test331", "mrsmiggles133", "password")
        newest_sent = list(sent_dict.values())[-1]
        newest_msg = newest_sent[1]
        self.assertEqual(newest_msg, "test user message")

    def test_check_new_contact(self):
        """
        Test that if a new contact not on the user's contact 
        list sends a message, return the contact's names in a list.
        """
        dsu_name = "userdoph" + ".dsu"
        p = Path(".") / dsu_name
        p_str = str(p)
        if p.exists():
            p.unlink()
        user = Profile(None, "userdoph", "password")
        store = ds_storage.Storage()
        test_dm = ds_messenger.DirectMessage()
        test_dm.set_recipient("13723718sahjshdaj")
        test_dm.set_message("test message")
        test = []
        test.append(test_dm)
        store.check_new_contact(test, "userdoph", "password")
        profile = Profile(None, "userdoph", "password")
        profile.load_profile(p_str)
        self.assertEqual((profile.friend)[0], "13723718sahjshdaj")


if __name__ == "__main__":
    unittest.main()
