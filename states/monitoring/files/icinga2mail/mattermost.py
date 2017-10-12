#!/usr/bin/python

# Copyright (c) 2015 NDrive SA
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import argparse
import json
import urllib2

VERSION = "0.2.1"

TEMPLATE_HOST = "__{notificationtype}__ {hostalias} is {hoststate} - {hostoutput}"  # noqa
TEMPLATE_SERVICE = "__{notificationtype}__ {hostalias}/{servicedesc} is {servicestate} - {serviceoutput}" # noqa

def parse():
    parser = argparse.ArgumentParser(description='Sends alerts to Mattermost')
    parser.add_argument('--url', help='Incoming Webhook URL', required=True)
    parser.add_argument('--channel', help='Channel to notify')
    parser.add_argument('--username', help='Username to notify as',
                        default='Monitoring')
    parser.add_argument('--iconurl', help='URL of icon to use for username',
                        default='https://s3.amazonaws.com/cloud.ohloh.net/attachments/50631/icinga_logo_med.png') # noqa
    parser.add_argument('--notificationtype', help='Notification Type',
                        required=True)
    parser.add_argument('--hostalias', help='Host Alias', required=True)
    parser.add_argument('--hoststate', help='Host State')
    parser.add_argument('--hostoutput', help='Host Output')
    parser.add_argument('--servicedesc', help='Service Description')
    parser.add_argument('--servicestate', help='Service State')
    parser.add_argument('--serviceoutput', help='Service Output')
    parser.add_argument('--oneline', action='store_true', help='Print only one line')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {version}'.format(version=VERSION))
    args = parser.parse_args()
    return args


def encode_special_characters(text):
    text = text.replace("%", "%25")
    return text


def make_data(args):
    template = TEMPLATE_SERVICE if args.servicestate else TEMPLATE_HOST

    # Emojis
    if args.notificationtype == "RECOVERY":
        EMOJI = ":white_check_mark:"
    elif args.notificationtype == "PROBLEM":
        EMOJI = ":sos:"
    elif args.notificationtype == "DOWNTIMESTART":
        EMOJI = ":thumbsdown:"
    elif args.notificationtype == "DOWNTIMEEND":
        EMOJI = ":thumbsup:"
    elif args.notificationtype == "DOWNTIMEREMOVED":
        EMOJI = ""
    elif args.notificationtype == "CUSTOM":
        EMOJI = ":sound:"
    elif args.notificationtype == "FLAPPINGSTART":
        EMOJI = ":cloud:"
    elif args.notificationtype == "FLAPPINGEND":
        EMOJI = ":sunny:"
    elif args.notificationtype == "ACKNOWLEDGEMENT":
        EMOJI = ":exclamation:"
    else:
        EMOJI = ""

    text = EMOJI + template.format(**vars(args))

    if args.oneline:
        text = text.splitlines()[0]

    payload = {
        "username": args.username,
        "icon_url": args.iconurl,
        "text": encode_special_characters(text)
    }

    if args.channel:
        payload["channel"] = args.channel

    data = "payload=" + json.dumps(payload)
    return data


def request(url, data):
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    return response.read()

if __name__ == "__main__":
    args = parse()
    data = make_data(args)
    response = request(args.url, data)
    print response

