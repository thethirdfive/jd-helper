# -*- coding: utf-8 -*-
# 参考
# https://segmentfault.com/a/1190000019378870

import base64
from Crypto.Cipher import AES
 
AES_SECRET_KEY = '5a8f3244786ea9b8' #此处16|24|32个字符
IV = "0000000000000000" #AES.MODE_CBC 需要
 
# padding算法
BS = len(AES_SECRET_KEY)
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1:])]
 
class AES_ENCRYPT(object):
    def __init__(self):
        self.key = AES_SECRET_KEY
        self.mode = AES.MODE_ECB # 这个模式不需要IV，需要的自己更换
 
    #加密函数
    def encrypt(self, text):
        #使用不同的模式
        #cryptor = AES.new(self.key.encode("utf8"), self.mode, IV.encode("utf8"))
        cryptor = AES.new(self.key.encode("utf8"), self.mode)
        self.ciphertext = cryptor.encrypt(bytes(pad(text), encoding="utf8"))
        #AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题，使用base64编码
        return base64.b64encode(self.ciphertext)
 
    #解密函数
    def decrypt(self, text):
        decode = base64.b64decode(text)
        #使用不同的模式
        #cryptor = AES.new(self.key.encode("utf8"), self.mode, IV.encode("utf8"))
        cryptor = AES.new(self.key.encode("utf8"), self.mode)
        plain_text = cryptor.decrypt(decode)
        return unpad(plain_text)
 
if __name__ == '__main__':
    aes_encrypt = AES_ENCRYPT()
    phone = "18615508659" # mobile=gyiWefherEdmpPHnNkWTNw==
    e = aes_encrypt.encrypt(phone)
    d = aes_encrypt.decrypt(e)
    print(phone)
    print(e)
    print(d)