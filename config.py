
from collections import namedtuple
import client
import os 


print("Only fill the Channel id , Token will be in Secret file")

print("You may watch guide or join on Discord .")

Login = namedtuple('Login', 'token, catching_channels')
ACCOUNTS = [
    Login(token = os.environ.get("token1"), catching_channels = [837046124865912864]),
  ]

SPAM_CHANNELS = [837045943672242187]