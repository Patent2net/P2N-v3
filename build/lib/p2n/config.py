# -*- coding: utf-8 -*-
# (c) 2017 The Patent2Net Developers

class OPSCredentials:
    """
    Wrapper around accessing the file for storing
    the OPS OAuth credentials, "cles-epo.txt".
    """

    def __init__(self, credentials_file=None):
        # put your credential from epo client in this file...
        # chargement clés de client
        self.credentials_file = credentials_file or 'cles-epo.txt'

    def read(self):
        """Read and decode credentials from file"""
        fic = open(self.credentials_file, 'r')
        key, secret = fic.read().split(',')
        key, secret = key.strip(), secret.strip()
        fic.close()

        return key, secret

    def write(self, oauth_key, oauth_secret):
        """Encode and write credentials to file"""
        fic = open(self.credentials_file, 'w')
        line = ','.join([oauth_key, oauth_secret])
        fic.write(line)
        fic.close()


def label_from_prefix(prefix):
    label = 'a single patent'
    if prefix == 'Families':
        label = 'the whole patent family'
    return label
