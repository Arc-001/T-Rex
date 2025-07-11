from pgpy import PGPKey, PGPUID, PGPMessage
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm

from key_gen import *
#generate a key

key = key("test", "test", "test")

#testing the save function

key.save_key("test")

private_key_str = ""
with open("test", "r") as private_key:
    private_key_str = private_key.read()

public_key_str = ""
with open("test.pub","r") as public_key:
    public_key_str = public_key.read()


#encrypting a message
encr_str = encrypt_message_file("test.pub", "This is ssuppose to be defcon 1 level secrete!!")

print("-------------------decryption---------------")

decr_str = decrypt_message("test", encr_str)
yield


