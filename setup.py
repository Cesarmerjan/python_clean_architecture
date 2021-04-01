from setuptools import setup, find_packages


def read(filename):
    return [
        req.strip()
        for req
        in open(filename).readlines()
    ]


setup(
    author="CesarMerjan",
    name="make_a_comment",
    python_requires=">3.6",
    version="0.1",
    description="Clean Architecture with Python",
    url="",
    license="",
    package_dir={"": "src"}
    packages=find_packages("src", exclude=[".venv", "tests"]),
    include_package_data=True,
    install_requires=read("requirements/prod.txt"),
    extras_require={
        "dev": read("requirements/dev.txt")
    }
)
