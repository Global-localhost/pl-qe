import setuptools
import os

setuptools.setup(
    name="qe-pennylane",
    version="0.1.0",
    author="Xanadu Inc.",
    description="PennyLane device for Quantum Engine",
    url="https://github.com/XanaduAI/pl-qe",
    packages=['qe_pennylane'],
    package_dir={'' : 'python'},
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        "pennylane",
        "pennylane-qiskit",
        "pennylane-qchem",
        "z-quantum-core",
    ]
)
