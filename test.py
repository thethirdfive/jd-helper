from AES_SECRET import AES_ENCRYPT


if __name__ == '__main__':
    aes_encrypt = AES_ENCRYPT()
    mobile = 'Y7yUMqjFLhHW5sALAwsidA=='
    phone = "13585096000"

    print(aes_encrypt.decrypt(mobile))