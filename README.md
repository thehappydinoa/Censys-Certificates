# Certificates Index [![Python3.7](https://img.shields.io/badge/Python-3.7-orange.svg?style=flat-square)](https://www.python.org/downloads/release/python-370/)

Simple script for getting validity dates and the SHA256 fingerprint of certificates.

## Install

```bash
pip install -r requirements.txt
```

## Run

Add the Censys API ID and secret that are shown under [My Account](https://censys.io/account) to `.env.sample` then rename to `.env`

```bash
python certificates_index.py
```

## Usage

```usage
usage: certificates_index.py [-h] [-v] [-o FILE]

Certificate info to CSV

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -o FILE, --output FILE
                        output for csv
```
