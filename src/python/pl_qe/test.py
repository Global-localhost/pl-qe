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

    with open("about.json", "w") as f:
        f.write(json.dumps(message_dict, indent=2))


def simple_circuit():
    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def circuit(x):
        qml.RX(x, wires=0)
        qml.RY(x, wires=1)
        qml.CNOT(wires=[0, 1])
        return qml.expval(qml.PauliZ(0))

    p = 0.123
    output = circuit(p)

    message_dict = {}
    message_dict["message"] = "{}".format(output)
    message_dict["schema"] = "message"

    with open("circuit_output.json", "w") as f:
        f.write(json.dumps(message_dict, indent=2))
