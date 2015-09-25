import base64
import json
import pyrax

MSG_TTL = 345600  # 4 days
CLAIM_TTL = 60
GRACE = 60
NUM_MSGS = 10

receive_counts = dict()


class QAuthError(Exception):
    pass


class Q():
    def connect(self, client_id):
        pyrax.keyring_auth()
        pyrax.queues.client_id = client_id

    def get_msgs(self, queue, ttl=CLAIM_TTL, grace=GRACE, count=NUM_MSGS):
        queue_claim = pyrax.queues.claim_messages(queue, ttl, grace, count)

        # make messages result iterable
        if queue_claim is None:
            return None, []
        else:
            # record read counts, replacement for SQS ApproximateReceiveCount
            for message in queue_claim.messages:
                if message.id in receive_counts:
                    receive_counts[message.id] += 1
                else:
                    receive_counts[message.id] = 1

        return queue_claim.id, queue_claim.messages

    def write_msg(self, queue, msg, ttl=MSG_TTL):
        body = base64.b64encode(json.dumps(msg))
        msg_sent = pyrax.queues.post_message(queue, body, ttl)
        print("Sent Msg; queue={0}, msg={1.id}".format(queue, msg_sent))
        return msg_sent

    def delete_msg(self, queue, msg, claim_id=None):
        msg_del = msg.delete(claim_id)
        print("Deleted Msg; queue={0}, msg={1.id}".format(queue, msg))
        return msg_del

    def update_msg(self, queue, orig_msg, new_msg):
        status = self.write_msg(self, queue, new_msg)
        self.delete_msg(queue, orig_msg)
        print("Updating Msg; queue={0}, orig_msg={1.id}, new_msg={2.id}"
              .format(queue, orig_msg, new_msg))
        return status

    def manage_failed_request(self, queue, msg, claim_id,
                              claim_renewal_ttl=60,
                              receive_count_limit=3):
        """Handle a failed request that has come through OpenStack Queues.
        If a msg has been read less than receive_count, renew the claim.
        Once receive_count has been reached, delete the message.
        """

        if msg.id in receive_counts:
            receive_count = receive_counts[msg.id]
        else:
            receive_count = 0

        if receive_count >= receive_count_limit or receive_count == 0:
            print("Failed message reached, deleting; receive_count={0},"
                  " receive_count_limit={1}, msg={2.id}".format(
                      receive_count, receive_count_limit, msg))
            return self.delete_msg(queue, msg, claim_id)
        else:
            print("Message Failed, renewing claim; "
                  "claim_renewal_ttl={0}, msg={1.id}, receive_count={2}, "
                  "receive_count_limit={3}".format(claim_renewal_ttl, msg,
                                                   receive_count,
                                                   receive_count_limit))
            return pyrax.queues.update_claim(queue, claim_id, claim_renewal_ttl)
