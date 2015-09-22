TTL = 60
GRACE = 60
NUM_MSGS = 10


class QAuthError(Exception):
    pass


class Q():
    def connect(self):
        pass


    def get_msgs(self, queue, ttl=TTL, grace=GRACE, count=NUM_MSGS):
        queue_claim = pq.claim_messages(queue, ttl, grace, count)
        msgs = queue_claim.messages

        # make result iterable
        if msgs is None:
            return []

        return msgs

        

    def write_msg(self, queue, msg):
        pass


    def delete_msg(self, queue, msg):
        pass


    def update_msg(self, queue, orig_msg, new_msg):
        pass


    def manage_failed_request(self, queue, msg, visibility_timeout=30,
                              receive_count_limit=3):
        pass