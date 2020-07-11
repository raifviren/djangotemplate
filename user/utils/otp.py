"""
Created at 11/07/20
@author: virenderkumarbhargav
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json
import urllib
from urllib.request import urlopen


def send_otp(mobile, authkey=None, message=None, sender='FAMHLT', otp_length=4, otp=None, otp_expiry=3, email=None):

    """
    Utility function to send otp using msg91 api
    source : https://docs.msg91.com/collection/msg91-api-integration/5/send-otp-message/TZ6HN0YI

    Parameter	    Type	    Description
    template		            Your custom template id
    otp_length	    number	    Number of digits in OTP (Keep in between 4 to 9)
    authkey*	    string	    Login authentication key (This key is unique for every user)
    message*	    string	    Message content to send. (For example : Your verification code is ##OTP##.)
    sender*	        string	    Receiver will see this as sender's ID. (For example : OTPSMS)
    mobile*	        string	    Keep number in international format (With country code)
    otp	            number	    OTP to send and verify. If not sent, OTP will be generated.
    otp_expiry	    number	    Expiry of OTP you can pass into minutes (default : 1440, max : 1440, min : 1)
    email	        string	    Email ID to which you wish to send the OTP

    *required

    :return:
    {
        "message":"3763646c3058373530393938",
        "type":"success"
    }
    """
    if not authkey:
        authkey = os.environ.get('MSG91_AUTH_KEY')
    if not message:
        message = "You otp for Famhealth app is ##OTP##"
    values = {
        'authkey': authkey,
        'mobile': mobile,
        'message': message,
        'sender': sender,
        'otp_expiry': otp_expiry
    }
    if otp:
        values.update({'otp': str(otp)})
    if email:
        values.update({'email': str(email)})

    url = "http://api.msg91.com/api/sendotp.php"  # API URL
    postdata = urllib.parse.urlencode(values)  # URL encoding the data here.
    req = urllib.request.Request(url, postdata.encode('UTF-8'))
    response = urlopen(req)
    data = response.read()  # Get Response
    res = json.loads(data.decode("utf-8"))
    if res['type'] == 'success':
        return True, res['message']
    return False, res['message']


def resend_otp(mobile, authkey=None, retrytype='voice'):
    """
        Utility function to resend otp using msg91 api
        source : https://docs.msg91.com/collection/msg91-api-integration/5/send-otp-resend/T1JWUDGB

        Parameter	    Type	    Description
        authkey*	    string	    Login authentication key (this key is unique for every user)
        mobile*	        number	    Keep number in international format (with country code)
        retrytype	    string	    Method to retry otp : voice or text. Default is voice.

        *required

        :return:
        {
            "message":"otp_sent_successfully",
            "type":"success"
        }
    """

    headers = {'content-type': "application/x-www-form-urlencoded"}
    if not authkey:
        authkey = os.environ.get('MSG91_AUTH_KEY')
    values = {
        'authkey': authkey,
        'mobile': mobile,
        'retrytype': retrytype,
    }
    url = "http://api.msg91.com/api/retryotp.php"  # API URL
    postdata = urllib.parse.urlencode(values)  # URL encoding the data here.
    req = urllib.request.Request(url, postdata.encode('UTF-8'), headers=headers)
    response = urlopen(req)
    data = response.read()  # Get Response
    res = json.loads(data.decode("utf-8"))
    if res['type'] == 'success':
        return True, res['message']
    return False, res['message']


def verify_otp(mobile, otp, authkey=None):
    """
            Utility function to verify otp using msg91 api
            source : https://docs.msg91.com/collection/msg91-api-integration/5/verify-otp/T1SVAQJ7

            Parameter	    Type	    Description
            authkey*	    string	    Login authentication key (this key is unique for every user)
            mobile*	        string	    Keep number in international format (with country code)
            otp*	        string	    OTP to verify

            *required

            :return:
            {
                "message":"number_verified_successfully",
                "type":"success"
            }
    """
    headers = {'content-type': "application/x-www-form-urlencoded"}
    if not authkey:
        authkey = os.environ.get('MSG91_AUTH_KEY')
    values = {
        'authkey': authkey,
        'mobile': mobile,
        'otp': otp,
    }
    url = "http://api.msg91.com/api/verifyRequestOTP.php"  # API URL
    postdata = urllib.parse.urlencode(values)  # URL encoding the data here.
    req = urllib.request.Request(url, postdata.encode('UTF-8'), headers=headers)
    response = urlopen(req)
    data = response.read()  # Get Response
    res = json.loads(data.decode("utf-8"))
    if res['type'] == 'success':
        return True, res['message']
    return False, res['message']