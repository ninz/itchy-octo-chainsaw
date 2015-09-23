import argparse
from msg import Q
import sys
import uuid


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--widget-id', dest='widget_id',
                        default=str(uuid.uuid1()), required=False,
                        help='Widget ID')
    parser.add_argument('--openstack-request-queue', dest='request_queue',
                        default='itchy-octo-chainsaw-request', required=False,
                        help='OpenStack Request Queue')
    return parser.parse_args()


def main():
    args = parse_args()
    client_id = str(uuid.uuid4())

    q = Q()
    q.connect(client_id)

    msg_resq = {'WidgetId': args.widget_id}
    q.write_msg(args.request_queue, msg_resq)


if __name__ == '__main__':
    sys.exit(main())
