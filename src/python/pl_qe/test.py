"""
Write the contents of pennylane.about() to a json file.
"""

import json
import pennylane as qml

from io import StringIO
from contextlib import redirect_stdout


def about():
    with StringIO() as buffer, redirect_stdout(buffer):
        qml.about()
        about = buffer.getvalue()
    message_dict = {}
    message_dict["message"] = about
    message_dict["schema"] = "message"

    with open("about.json",'w') as f:
        f.write(json.dumps(message_dict, indent=2))
