"""
Unittest module to test all communication functions inside
ds_protocol. 
"""

import unittest
import ds_protocol
import json

class DS_protocol_tester(unittest.TestCase):
    """
    Contains functions for testing every function
    used for communication protocol.
    """

    def test_join_json(self):
        """Test that join_json correctly returns the join json object."""
        username = "username"
        password = "password"
        result = ds_protocol.join_json(username, password)
        json_obj = json.loads(result)
        print(json_obj)
        self.assertEqual(json_obj["join"]["username"], username)
        self.assertEqual(json_obj["join"]["password"], password)

    def test_send_json(self):
        """Test that send_json correctly returns the send join object"""
        token = "placeholder"
        message = "test message"
        recipient = "receiver"       
        result = ds_protocol.send_json(token, message, recipient)
        json_obj = json.loads(result)
        self.assertEqual(json_obj["token"], token)
        self.assertEqual(json_obj["directmessage"]["entry"], message)

    def test_request_json(self):
        """Test that request message json is created correctly."""
        token = "placeholder"
        msg_type = "new"
        result = ds_protocol.request_json(token, msg_type)
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
        type, msgs = ds_protocol.extract_msgs(json_obj)
        self.assertEqual(type, "ok")
        self.assertEqual(msgs[0]["message"], message)
         # incorrect test case:
        json_msg = "invalid json"
        type, msgs = ds_protocol.extract_msgs(json_msg)
        self.assertEqual(type, "")
        self.assertEqual(msgs, [])

    def test_extract_resp(self):
        type = "ok"
        message = "Direct messages sent"
        json_msg = {"response": {"type": type, "message": message}}
        json_obj = json.dumps(json_msg)
        type, msg = ds_protocol.extract_resp(json_obj)
        self.assertEqual(msg, message)
        type, msg = ds_protocol.extract_resp("invalid json")
        self.assertEqual(type, "")
        self.assertEqual(msg, "")

    def test_extract_token(self):
        json_msg = "{\"response\": {\"type\": \"ok\", \"message\": \"\", \"token\":\"12345678-1234-1234-1234-123456789abc\"}}"
        result = ds_protocol.extract_token(json_msg)
        self.assertEqual(result[2], "12345678-1234-1234-1234-123456789abc")
        
if __name__ == "__main__":
    unittest.main()
