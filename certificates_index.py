#!/usr/bin/env python3
"""
Simple script for getting validity dates and the SHA256 fingerprint of certificates.
"""

import csv
import logging
from os import getenv
from argparse import ArgumentParser

# Thrid-Party Libraries
try:
    from dotenv import load_dotenv
except ImportError:
    print("Please install dotenv with `pip install python-dotenv`")
    quit(1)
try:
    import censys.certificates
except ImportError:
    print("Please install censys with `pip install censys`")
    quit(1)

# Loads and reads `.env`
load_dotenv()
API_ID = getenv("CENSYS_APP_ID")
API_SECRET = getenv("CENSYS_SECRET")


def main(query="parsed.names: censys.io and tags: trusted", csv_filename="certificates_index.csv"):
    """
    main function
    """
    # Checks that required tokens are present
    if not (API_ID and API_SECRET):
        raise KeyError(
            "Please specify both `CENSYS_APP_ID` and `CENSYS_SECRET` in your `.env` file")

    # Authenticates with Censys
    client = censys.certificates.CensysCertificates(
        api_id=API_ID, api_secret=API_SECRET)

    # Queries Censys
    cert_fields = ["parsed.subject_dn",
                   "parsed.validity",
                   "parsed.fingerprint_sha256"]
    logging.debug("Searching for `%s`", query)
    certs = client.search(query, fields=cert_fields)
    account = client.account()
    logging.info("Used %d of %d calls for %s",
                 account["quota"]["used"], account["quota"]["allowance"], account["email"])

    # Writes to CSV
    with open(csv_filename, "w") as csvfile:
        csv_fields = ["subject_dn", "fingerprint_sha256",
                      "validity_start", "validity_end"]
        writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
        writer.writeheader()

        for cert in certs:
            writer.writerow({
                "subject_dn": cert["parsed.subject_dn"],
                "fingerprint_sha256": cert["parsed.fingerprint_sha256"],
                "validity_start": cert["parsed.validity.start"],
                "validity_end": cert["parsed.validity.end"]
            })
    logging.info("Wrote to %s", csv_filename)


if __name__ == "__main__":
    # Argparse
    parser = ArgumentParser(description="Certificate info to CSV")
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity", action="store_true")
    parser.add_argument("-o", "--output", type=str,
                        metavar="FILE", help="output for csv")
    args = parser.parse_args()

    # Logging
    logging_level = logging.INFO
    if args.verbose:
        logging_level = logging.DEBUG
    logging.basicConfig(level=logging_level)

    # Main
    try:
        kwargs = dict()
        if args.output:
            kwargs = {"csv_filename": args.output}
        main(**kwargs)
    except KeyboardInterrupt:
        print("Quitting...")
        quit(0)
    except Exception as error:
        print("Something Went Wrong:")
        print(str(error))
