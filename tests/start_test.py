import hashlib
import subprocess
import time
from multiprocessing import Process

from Models.User import UserModel
from server import start_server

test_user = UserModel(
    user_id="test_user_id",
    password_hash=hashlib.sha256("test_password_hash".encode()).hexdigest()
)

if __name__ == '__main__':
    server1 = Process(target=start_server, args=(8000,))
    server2 = Process(target=start_server, args=(8001,))
    server1.start()
    server2.start()

    time.sleep(5)

    subprocess.run("coverage run -m pytest".split())

    server1.terminate()
    server2.terminate()
