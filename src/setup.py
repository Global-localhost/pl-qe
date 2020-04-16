from setuptools import setup, find_packages


with open("python/qe-pennylane/_version.py") as f:
    version = f.readlines()[-1].split()[-1].strip("\"'")


requirements = [
    "pennylane",
    "z-quantum-core",
]


info = {
    "name": "qe-pennylane",
    "version": version,
    "author": "Xanadu Inc.",
    "packages": find_packages(where="python"),
    "package_dir": {"": "python"},
    "install_require": requirements,
    "description": "PennyLane device for Quantum Engine",
    'provides': ["qe-pennylane"],
}


classifiers = [
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
]


setup(classifiers=classifiers, **(info))
