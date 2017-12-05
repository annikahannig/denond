#!/usr/bin/env python


import argparse

from denond import denon


def parse_args():
    """Handle commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--host",
                        help="Denon host",
                        required=True)

    parser.add_argument("-f", "--filename",
                        help="Restore this config",
                        required=True)

    return parser.parse_args()


def main():
    args = parse_args()

    print("[i] Restoring audio matrix configuration")

    client = denon.Client(args.host)
    conf = matrix_config.MatrixConfig.from_file(args.filename)

    client.write_matrix_config(conf)
    print("[+] Done.")
