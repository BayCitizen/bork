from distutils.core import setup
name = 'bork'
setup(
    name = name,
    packages = [name],
    version = "0.0.2",
    description = "A light weight puppet like library",
    author = "Joshua Bonnett",
    author_email = "jbonnett@baycitizen.org",
    url = "http://github.com/baycitizen/bork",
    download_url = "",
    keywords = ["encoding", "i18n", "xml"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved ::  Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description = """\
A light weight puppet like library
-------------------------------------

Named after the catch phrase of a certain chef puppet.

After much frustration with puppet's docs not mapping to reality,
The over comfident developer that I am, I decided to write bork. 
For simplicty sake it is currently only targeting recent versions
of ubuntu. 

Licensed under the Apache Software License.
"""
)