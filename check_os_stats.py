import sys

import check_vxlan_link
from common import log


def main():
    print('Welcome to checking OpenStack stats...')
    print()

    log.init_logging()

    # Check vxlan link info between cmp nodes
    check_vxlan_link.VxlanLinkCheck().execute()


if __name__ == '__main__':
    sys.exit(main())