"""
Created at 11/07/20
@author: virenderkumarbhargav
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
import re
import uuid


def is_phone_valid(phone):
    regex_object = re.search(
        "\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$",
        phone)
    return True if regex_object else False


class DocumentJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)
