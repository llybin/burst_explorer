def get_message(attachment: bytes) -> str:
    """
    byte[0] - tx version
    2**8 * byte[2] + byte[1] - message len
    byte[3] and byte[4] - ?
    """
    header = attachment[:5]
    body = attachment[5:]
    message_len = 2**8 * header[2] + header[1]
    return body[:message_len].decode()
