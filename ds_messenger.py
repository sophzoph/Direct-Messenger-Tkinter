"""
ds_messenger handles all sending and retrieving of the user's
messages.
"""

import socket
import time
import json


class DirectMessage:
    """
    For creating DirectMessage object when new and all
    messages are retrieved.
    """
    def __init__(self):
        """Initialize attributes of DirectMessage."""
        self.recipient = None
        self.message = None
        self.timestamp = None

    def set_recipient(self, recipient):
        """Set recipient attribute."""
        self.recipient = recipient

    def set_message(self, message):
        """Set message attribute."""
        self.message = message

    def set_timestamp(self, timestamp):
        """Set timestamp attribute."""
        self.timestamp = timestamp


class DirectMessenger:
    """
    Contains functions for sending and retrieving messages
    from the server.
    """
    def __init__(self, dsuserver=None, username=None, password=None):
        """Initialize attributes of DirectMessenger."""
        self.token = None
        self.username = username
        self.password = password
        self.dsuserver = dsuserver
        self.port = 3021
        self.sent = ""

    def send(self, message: str, recipient: str) -> bool:
        """Return true if message successfully sent, false if send failed."""
        # if recipient is None, then will return false, else True
        valid_send = True
        try:
            # if joining server is successful(also sets token attribute)
            if self.get_token():
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                    client.connect((self.dsuserver, self.port))
                    s_msg = DSProtocol.send_json(self.token, message, recipient)
                    send = client.makefile("w")
                    recv = client.makefile("r")
                    send.write(s_msg + '\r\n')
                    send.flush()
                    resp = recv.readline()
                    type, server_msg = DSProtocol.extract_resp(resp)
                    if type == "error":
                        valid_send = False
                    else:
                        # write a json object into a temporary file
                        s_msg = json.loads(s_msg)
                        d_msg = DirectMessage()
                        d_msg.set_recipient(recipient)
                        d_msg.set_message(message)
                        d_msg.set_timestamp(s_msg["directmessage"]["timestamp"])
                        self.sent = d_msg
            else:  # if getting token is unsuccessful
                valid_send = False

        except socket.error as err:
            print("ERROR:", err)
            valid_send = False
        except socket.herror as err:
            print("ERROR:", err)
            valid_send = False
        except socket.gaierror as err:
            print("ERROR:", err)
            valid_send = False
        except socket.timeout as err:
            print("ERROR:", err)
            valid_send = False
        except Exception as excep:
            print("ERROR:", excep)
            valid_send = False
        return valid_send

    def retrieve_new(self) -> list:
        """Return a list of DirectMessage objects containing all new messages."""
        dm_lst = []
        try:
            if self.get_token():
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                    client.connect((self.dsuserver, self.port))
                    get_msg = DSProtocol.request_json(self.token, "new")
                    send = client.makefile("w")
                    recv = client.makefile("r")
                    send.write(get_msg + '\r\n')
                    send.flush()
                    resp = recv.readline()
                    type, msg_lst = DSProtocol.extract_msgs(resp)

                    if type == "error":
                        print("ERROR in retrieving messages")
                    else:
                        for msg in msg_lst:
                            d_msg = DirectMessage()
                            d_msg.set_recipient(msg["from"])
                            d_msg.set_message(msg["message"])
                            d_msg.set_timestamp(msg["timestamp"])
                            dm_lst.append(d_msg)
            else:
                pass

        except socket.error as err:
            print("ERROR:", err)
        except socket.herror as err:
            print("ERROR:", err)
        except socket.gaierror as err:
            print("ERROR:", err)
        except socket.timeout as err:
            print("ERROR:", err)
        except Exception as excep:
            print("ERROR:", excep)
        return dm_lst

    def retrieve_all(self) -> list:
        """Return a list of DirectMessage objects containing all messages."""
        dm_lst = []
        try:
            if self.get_token():
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                    client.connect((self.dsuserver, self.port))
                    get_msg = DSProtocol.request_json(self.token, "all")
                    send = client.makefile("w")
                    recv = client.makefile("r")
                    send.write(get_msg + '\r\n')
                    send.flush()
                    resp = recv.readline()
                    type, msg_lst = DSProtocol.extract_msgs(resp)

                    if type == "error":
                        print("ERROR in retrieving messages")
                    else:
                        for msg in msg_lst:
                            d_msg = DirectMessage()
                            d_msg.set_recipient(msg["from"])
                            d_msg.set_message(msg["message"])
                            d_msg.set_timestamp(msg["timestamp"])
                            dm_lst.append(d_msg)
            else:
                pass

        except socket.error as err:
            print("ERROR:", err)
        except socket.herror as err:
            print("ERROR:", err)
        except socket.gaierror as err:
            print("ERROR:", err)
        except socket.timeout as err:
            print("ERROR:", err)
        except Exception as excep:
            print("ERROR:", excep)
        return dm_lst

    def get_token(self):
        """
        Return whether user is valid.
        Sets token attribute if login is successful.
        """
        valid_user = True
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, self.port))
                join_msg = DSProtocol.join_json(self.username, self.password)
                send = client.makefile("w")
                recv = client.makefile("r")
                send.write(join_msg + '\r\n')
                send.flush()
                resp = recv.readline()
                type, msg, token = DSProtocol.extract_token(resp)
                if type == "error":
                    valid_user = False
                else:
                    self.token = token

        except socket.error as err:
            print("ERROR:", err)
            valid_user = False
        except socket.herror as err:
            print("ERROR:", err)
            valid_user = False
        except socket.gaierror as err:
            print("ERROR:", err)
            valid_user = False
        except socket.timeout as err:
            print("ERROR:", err)
            valid_user = False
        except Exception as excep:
            print("ERROR:", excep)
            valid_user = False
        return valid_user


class DSProtocol:
    """
    Contains all functions needed to deserialize and serialize
    JSON objects.
    """
    def join_json(username, password):
        """Format join message into JSON."""
        jdict = {"join": {"username": username, "password": password, "token": ""}}
        join_msg = json.dumps(jdict)
        return join_msg

    def send_json(token, message, recipient):
        """Format message sent to receiver into JSON."""
        tm = str(time.time())
        s_dict = {"token": token, "directmessage": {"entry": message, "recipient": recipient, "timestamp": tm}}
        s_msg = json.dumps(s_dict)
        return s_msg

    def request_json(token, msg_type):
        """Format requesting message type into JSON."""
        r_dict = {"token": token, "directmessage": msg_type}
        r_msg = json.dumps(r_dict)
        return r_msg

    def user_msg_json(recipient, message):
        """add docstring here"""
        tm = str(time.time())
        s_dict = {"message": message, "recipient": recipient, "timestamp": tm}
        s_json = json.dumps(s_dict)
        return s_json

    def extract_msgs(json_msg):
        """
        Call the json.loads function on a json string
        Return messages for all and new
        """
        type = ""
        msgs = []
        try:
            json_obj = json.loads(json_msg)
            type = json_obj['response']['type']
            msgs = json_obj['response']['messages']
        except json.JSONDecodeError:
            print("Json cannot be decoded.")
        return type, msgs

    def extract_resp(json_msg):
        """
        Call the json.loads function on a json string
        Return whether sending of direct message was successful
        """
        type = ""
        msg = ""
        try:
            json_obj = json.loads(json_msg)
            type = json_obj['response']['type']
            msg = json_obj['response']['message']
        except json.JSONDecodeError:
            print("Json cannot be decoded.")
        return type, msg

    def extract_token(json_msg: str):
        """
        Call the json.loads function on a json string
        Returns server response type, msg, and user token.
        """
        type = ""
        msg = ""
        token = ""
        try:
            json_obj = json.loads(json_msg)
            type = json_obj['response']['type']
            msg = json_obj['response']['message']
            if 'token' not in json_obj['response'].keys():
                token = ""
            else:
                token = json_obj['response']['token']
        except json.JSONDecodeError:
            print("Json cannot be decoded.")
        return type, msg, token
