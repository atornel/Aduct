import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Aduct",
    version="1.2.0",
    author="J Arun Mani; Atornel",
    author_email="j.arunmani@protonmail.com",
    description="Aduct lets you make flexible interfaces that can be easily\
    improved and modified by both developers and users.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/atornel/Aduct",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
    ],
    keywords="gui gtk ui",
    install_requires=["pygobject",],
    python_requires="~=3.3",
)
