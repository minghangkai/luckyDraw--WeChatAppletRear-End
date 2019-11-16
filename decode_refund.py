import base64
import hashlib
from Crypto.Cipher import AES


class AESCipher():
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    def __init__(self, key):
        self.key = hashlib.md5(key.encode('utf8')).hexdigest()

        # Padding for the input string --not
        # related to encryption itself.
        self.BLOCK_SIZE = 32  # Bytes
        self.pad = lambda s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    # 加密
    def encrypt(self, raw):
        raw = self.pad(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(raw))

    # 解密，针对微信用此方法即可
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return self.unpad(cipher.decrypt(enc)).decode('utf8')



"""req_info = '+SvyH+civpvogYSWAsO/Kct4RFWwNt/4UH3uo0vNtJr39zhk+lWw9eem5ANO6n0RBJR4VfDbdAfkfcfS9E/abTdoSjvmdbGO8VNkE8' \
           'P6CrElI3QOygVUvzvUNJqHQe5oI3VUxZ3J/MmTs9QcOuVu7TK8vba4dh50/IE5xtkLABMiYdfsM7Dg07m+FBcDac14t/Qpcs24jcvw' \
           'XtmlCAeOPjILUNNM4Gh9c6Tbv5mNZRx1UNtgmmDsJDwDMkc9XWOT/wdA5+wIbGTJob8xp8ogix5rKlV9uzhnc+4TQWoSYx/w/vKZc+' \
           'Ng+cIr0FQE0ezwNCpLH/kgY3soVn4GTpKWAoaPjTXoxIq2oNq1vLOI1R3FIGqvQKxYoAsk0gyzud3OkaTg31mY6Sp4q0H2rHRHkKNX' \
           '4lRNDQvKKgeUeMAPyoHTgIHr4jsv8sypMoqNRYDbYu8AMTsym/BemgUk9VQia30GpdlZ4Yg9LtLMQIfogEbQdH6cJ66SijHIN5vuJQ' \
           '7h4zEjgexMGiiVIA6fYcSCfsO15tlePmm98CXWysNyJzjq7lSJdT0P2eSaly4wm6qY6hAxXB3HujZefn3R5zf/533cg9hYhWZOXR5T' \
           'KRx5lrEB5Fg1TaC8s32iyuIZLS53sp8/QrOIYsfp5A737+Ej7l+eJMTWIw7Nz0GyW54hBXictUy5hXg8Ay97MPz3fYN2dgYlI78nN+' \
           'R0C9A13nARDQTuU6jRjmuXBqAC798Oa/FbuaACtuHmhEeY9l08m+Da6utrJXC4hEpi+q747QTdZG2Eufejsg35ev2vbpXzJW7bMtOi' \
           '+3m6EApe1JzYmg2fcg/y++RxCB//gTKgW7bI7cb3C3e2i1dq0AQ4/N5aJKam8Umplagdw/HdloUWi5QEPwGk0qV/TTZ6OeCRc5LXpY' \
           'SMB5m7w7mk8t2GcSWCzuw8K7ttQJe+M/Jv18U89JCJEsF5OGoq+kuTog2QdA7v3PnrkJFQefuAcP0QDES0NcI0uzR/hFp4SjRtfXZA' \
           'Kols+7wu88OWbq0hzEofm5CgoA=='

pwd = 'WUCHUANTONGCHENGWANGsR10280923sR'
msg = req_info
print(AESCipher(pwd).decrypt(msg))"""