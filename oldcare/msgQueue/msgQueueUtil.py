from multiprocessing import Queue

# Create a message queue
message_queue = Queue()


def receive_message_from_process():
    # Receive the message from the message queue
    message = message_queue.get()

    return message


def send_message_to_process(msg):
    # Put the message into the queue
    message_queue.put(msg)
