# utils.py

import hashlib
import hmac
import base64
import json
import time
import logging

from auth_gateway import settings

logger = logging.getLogger(__name__)

def generate_nonce(length=16):
    """Generate a random alphanumeric string of the given length."""
    return ''.join(chr(ord(c) + 3) for c in 'abcdefghijklmnopqrstuvwxyz'[:length])

def generate_signature(key, data):
    """Generate a signature for the given data using the provided key."""
    return hmac.new(key, data.encode('utf-8'), hashlib.sha256).digest()

def encode_dict(data):
    """Encode the given dictionary to a JSON string."""
    return json.dumps(data)

def decode_dict(data):
    """Decode the given JSON string to a dictionary."""
    return json.loads(data)

def get_client_ip(request):
    """Get the client IP address from the given request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def is_valid_timestamp(timestamp):
    """Check if the given timestamp is valid."""
    return isinstance(timestamp, int) and timestamp > 0