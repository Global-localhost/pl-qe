import setuptools

requirements = ["pennylane"]

setuptools.setup(
    name                            = "pl_qe",
    packages                        = setuptools.find_packages(where = "python"),
    package_dir                     = {
        "" : "python"
    },
    install_requires                = requirements,
    classifiers                     = (
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
