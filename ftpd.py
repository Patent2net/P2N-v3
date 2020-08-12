import os.path
import argparse

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

FTP_ROOT = '.'


def run_ftpd(user, password, host, port, passive, anon):
    user_dir = os.path.join(FTP_ROOT, user)
    if not os.path.isdir(user_dir):
        os.mkdir(user_dir)
    authorizer = DummyAuthorizer()
    authorizer.add_user(user, password, user_dir, perm="elradfmw")
    if anon:
        authorizer.add_anonymous("/usr/src/P2N-V3")

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.permit_foreign_addresses = True
    
    passive_ports = passive.split('-')
    handler.passive_ports = range(int(passive_ports[0]), int(passive_ports[1]))

    server = FTPServer((host, port), handler)
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--user', default='user',
        help="Username for FTP acess (user will be created)")
    parser.add_argument('--password', default='password',
                        help="Password for FTP user.")
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5021)
    parser.add_argument('--passive', default='5001-5011',
                        help="Range of passive ports")
    parser.add_argument('--anon', action='store_true',
                        help="Allow anonymous access")
    args = parser.parse_args()
    run_ftpd(**vars(args))

if __name__ == '__main__':
    main()
