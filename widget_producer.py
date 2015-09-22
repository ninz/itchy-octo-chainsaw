import pyrax.queues as pq


def main():
    msg = pq.post_message('itchy-octo-chainsaw-request', body, ttl)
