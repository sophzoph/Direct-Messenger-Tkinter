"""
ds_protocol handles the serializing and deserializing of
JSON objects used to communicate between the client and server.
"""

import json
import time

"""ds protocol part 1 How you solve this requirement is up
to you, but a good approach will likely include adding a
function to your ds_protocol that converts JSON messages to
a list or a dictionary."""


def extract_token(json_msg: str):
    """
    Call the json.loads function on a json string and convert
    it to a TokenTuple object.
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


def join_json(username, password):
    """Format join message into JSON."""
    jdict = {"join": {"username": username, "password": password, "token": ""}}
    join_msg = json.dumps(jdict)
    return join_msg


# new protocol functions for a5
def send_json(token, message, recipient):
    """Format message sent to receiver into JSON."""
    time_now = str(time.time())
    s_dict = {"token": token, "directmessage": {"entry": message, "recipient": recipient, "timestamp": time_now}}
    s_msg = json.dumps(s_dict)
    return s_msg


def request_json(token, msg_type):
    """Format requesting message type into JSON."""
    r_dict = {"token": token, "directmessage": msg_type}
    r_msg = json.dumps(r_dict)
    return r_msg


def extract_msgs(json_msg):
    """
    Call the json.loads function on a json string and convert
    it to a MsgTuple object.
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
    Call the json.loads function on a json string and convert
    it to a RespTuple object.
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
