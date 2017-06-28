#!/usr/bin/env python

"""
Download the current audio matrix
configuration and save it to a file.
"""

import argparse

from denond import denon


def parse_args():
    """Handle commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--host",
                        help="Denon host",
                        required=True)

    parser.add_argument("-o", "--output",
                        help="Save file here",
                        required=True)

    return parser.parse_args()



def main():
    """Download an audiomatrix config"""
    args = parse_args()

    print("[i] Fetching config from: {}".format(args.host))

    client = denon.Client(args.host)
    conf = client.read_matrix_config()
    conf.save(args.output)

    print("[+] Config saved to: {}".format(args.output))


if __name__ == '__main__':
    main()

