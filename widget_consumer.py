import argparse
import requests
import sys
import time
import uuid
from msg import Q, WidgetResponseMsg


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--openstack-request-queue', dest='request_queue',
                        default="itchy-octo-chainsaw-request", required=False,
                        help='OpenStack Request Queue')
    parser.add_argument('--openstack-response-queue', dest='response_queue',
                        default="itchy-octo-chainsaw-response", required=False,
                        help='OpenStack Response Queue')
    parser.add_argument('--sleep', dest='sleep', default=2, required=False,
                        help='Seconds to sleep between responses')
    return parser.parse_args()


def main():
    args = parse_args()

    client_id = str(uuid.uuid4())
    q = Q()
    q.connect(client_id)

    while True:

        (claim_id, messages) = q.get_msgs(args.request_queue)
        for _msg in messages:

            msg = WidgetResponseMsg(_msg, q)
            print("Received Msg; msg={0.id}, body={0.body}".format(msg))

            # Create response message.
            msg_resp = msg.get_std_response(msg)

            try:
                widget = msg.process()
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    # Our widget id is most likely not UUID v1.
                    print("Widget maker rejected widget; msg={0.id}, "
                          "status_code={1.status_code}".format(msg,
                                                               e.response))
                    # Delete Request Message.
                    q.delete_msg(args.request_queue, _msg, claim_id)
                else:
                    print("Widget maker failed to make widget; msg={0.id} "
                          "status_code={1.status_code}".format(msg,
                                                               e.response))
                    q.manage_failed_request(args.request_queue, _msg, claim_id)
                continue
            except requests.exceptions.ConnectionError:
                print("Widget maker is down; msg={0.id}".format(msg))
                q.manage_failed_request(args.request_queue, _msg, claim_id)
                continue
            else:
                print("Widget created; msg={0.id}, body={1.content}"
                      .format(msg, widget))
                msg_resp.update({"Status": "OK"})

            # Send Response Message.
            q.write_msg(args.response_queue, msg_resp)

            # Delete Request Message.
            q.delete_msg(args.request_queue, _msg, claim_id)

        time.sleep(float(args.sleep))


if __name__ == "__main__":
    sys.exit(main())
