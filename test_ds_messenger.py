# Sophia Zhang
# sophiasz@uci.edu
# 57934003

"""
Unittest module to test all send and receive functions 
inside ds_messenger. 
"""

import unittest
import ds_messenger
import json
import time


class DS_messenger_tester(unittest.TestCase):
    """
    Contains functions for testing every function
    used for DS messenger functions.
    """
    def test_set_recipient(self):
        """Test set recipient attribute."""
        recipient = "recipient_name"
        ds = ds_messenger.DirectMessage()
        ds.set_recipient(recipient)
        self.assertEqual(ds.recipient, recipient)

    def test_set_message(self):
        """Test set message attribute."""
        message = "test message"
        ds = ds_messenger.DirectMessage()
        ds.set_message(message)
        self.assertEqual(ds.message, message)

    def test_set_timestamp(self):
        """Test set timestamp attribute."""
        timestamp = time.time()
        ds = ds_messenger.DirectMessage()
        ds.set_timestamp(timestamp)
        self.assertEqual(ds.timestamp, timestamp)

    def test_send(self):
        """Test that send function returns True and False correctly."""
        ds = ds_messenger.DirectMessenger("168.235.86.101", "mrsmiggles133", "password")
        result = ds.send("test message", "receiver331")
        self.assertEqual(result, True)

        # test username invalid type
        ds2 = ds_messenger.DirectMessenger("168.235.86.101", 5.5555, "password")
        result = ds2.send("test message", "receiver331")
        self.assertEqual(result, False)

        ds3 = ds_messenger.DirectMessenger("160.000.00.000", "mrsmiggles133", "password")
        result = ds3.send("test message", "receiver331")
        self.assertEqual(result, False)

        ds4 = ds_messenger.DirectMessenger("168.235.86.101", "mrsmiggles133", "22")
        result = ds4.send("test message", "receiver331")
        self.assertEqual(result, False)

        ds5 = ds_messenger.DirectMessenger("168.235.86.101", "mrsmiggles133", "password")
        result = ds5.send("test message", None)
        self.assertEqual(result, False)

    def test_retrieve_new(self):
        """Test that retrieve new function returns all new messages."""
        ds = ds_messenger.DirectMessenger("168.235.86.101", "mrsmiggles133", "password")
        ds.send("testing retrieve new", "soph")
        ds2 = ds_messenger.DirectMessenger("168.235.86.101", "soph", "password")
        new = ds2.retrieve_new()
        self.assertEqual(new[-1].recipient, "mrsmiggles133")

    def test_retrieve_all(self):
        """
        Test that retrieve all function returns all messages.
        ds2 will send a message to ds.
        """
        ds = ds_messenger.DirectMessenger("168.235.86.101", "mrsmiggles133", "password")
        ds2 = ds_messenger.DirectMessenger("168.235.86.101", "soph", "password") 
        length_before_send = len(ds.retrieve_all())
        ds2.send("testing retrieve all", "mrsmiggles133")
        length_after_send = len(ds.retrieve_all())
        self.assertEqual(length_after_send, length_before_send + 1)

    def test_get_token(self):
        """Test that joining as a real user will return True."""
        ds = ds_messenger.DirectMessenger("168.235.86.101", "mrsmiggles133", "password")
        result = ds.get_token()
        self.assertEqual(result, True)

    def test_join_json(self):
        """Test that join_json correctly returns the join json object."""
        username = "username"
        password = "password"
        result = ds_messenger.DSProtocol.join_json(username, password)
        json_obj = json.loads(result)
        print(json_obj)
        self.assertEqual(json_obj["join"]["username"], username)
        self.assertEqual(json_obj["join"]["password"], password)

    def test_send_json(self):
        """Test that send_json correctly returns the send join object"""
        token = "placeholder"
        message = "test message"
        recipient = "receiver"       
        result = ds_messenger.DSProtocol.send_json(token, message, recipient)
        json_obj = json.loads(result)
        self.assertEqual(json_obj["token"], token)
        self.assertEqual(json_obj["directmessage"]["entry"], message)

    def test_request_json(self):
        """Test that request message json is created correctly."""
        token = "placeholder"
        msg_type = "new"
        result = ds_messenger.DSProtocol.request_json(token, msg_type)
        json_obj = json.loads(result)
        self.assertEqual(json_obj["token"], token)
        self.assertEqual(json_obj["directmessage"], msg_type)

    def test_extract_msgs(self):
        """Test that json used to extract messages is created correctly."""
        # test correct case
        type = "ok"
        message = "Hello User 1!"
        json_msg = {"response": {"type": type, "messages": [{"message": message, "from": "markb", "timestamp": "1603167689.3928561"}]}}
        json_obj = json.dumps(json_msg)
        type, msgs = ds_messenger.DSProtocol.extract_msgs(json_obj)
        self.assertEqual(type, "ok")
        self.assertEqual(msgs[0]["message"], message)

        json_msg = "invalid json"
        type, msgs = ds_messenger.DSProtocol.extract_msgs(json_msg)
        self.assertEqual(type, "")
        self.assertEqual(msgs, [])

    def test_extract_resp(self):
        type = "ok"
        message = "Direct messages sent"
        json_msg = {"response": {"type": type, "message": message}}
        json_obj = json.dumps(json_msg)
        type, msg = ds_messenger.DSProtocol.extract_resp(json_obj)
        self.assertEqual(msg, message)
        type, msg = ds_messenger.DSProtocol.extract_resp("invalid json")
        self.assertEqual(type, "")
        self.assertEqual(msg, "")

    def test_extract_token(self):
        json_msg = "{\"response\": {\"type\": \"ok\", \"message\": \"\", \"token\":\"12345678-1234-1234-1234-123456789abc\"}}"
        result = ds_messenger.DSProtocol.extract_token(json_msg)
        self.assertEqual(result[2], "12345678-1234-1234-1234-123456789abc")

if __name__ == "__main__":
    unittest.main()