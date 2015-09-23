import base64
import json
import pyrax
pq = pyrax.queues

TTL = 60
GRACE = 60
NUM_MSGS = 10


class QAuthError(Exception):
    pass


class Q():
    def connect(self, client_id):
        pyrax.keyring_auth()
        pyrax.queues.client_id = client_id

    def get_msgs(self, queue, ttl=TTL, grace=GRACE, count=NUM_MSGS):
        queue_claim = pyrax.queues.claim_messages(queue, ttl, grace, count)

        # make messages result iterable
        if queue_claim is None:
            return None, []

        return queue_claim.id, queue_claim.messages

    def write_msg(self, queue, msg, ttl=TTL):
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

    def manage_failed_request(self, queue, msg, visibility_timeout=30,
                              receive_count_limit=3):
        pass
