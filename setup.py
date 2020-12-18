from setuptools import setup, find_packages

setup(
    name="en_to_ipa",
    version="0.1.0",
    description="Tools to convert English to ARPABET and IPA",
    url="https://github.com/rbracco/en_to_ipa",
    author="Robert Bracco",
    author_email="robertbracco1@gmail.com",
    license="BSD 2-clause",
    packages=find_packages(include=["en_to_ipa"]),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
