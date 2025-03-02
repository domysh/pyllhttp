from setuptools import setup, Extension

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'pyllhttp',
    version = '6.7.0',
    description = ("llhttp in python"),
    url = "http://github.com/domysh/pyllhttp",
    author = "Derrick Lyndon Pallas, Domingo Dirutigliano",
    author_email = "derrick@pallas.us",
    license = "MIT",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    keywords = "http parser",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: JavaScript",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "License :: OSI Approved :: MIT License",
    ],
    packages = [ "pyllhttp" ],
    headers = [ "lib/llhttp.h", "lib/api.h" ],
    ext_modules = [ Extension('__pyllhttp',
        sources = """
            pyllhttp.c
            lib/llhttp.c
            lib/http.c
            lib/api.c
        """.split(),
        language = "c",
        extra_compile_args=["-O3"],
        #extra_compile_args=["-static-libasan", "-fsanitize=address"],
        #extra_link_args=[ "-static-libasan", "-fsanitize=address"],
    ) ],
)
#