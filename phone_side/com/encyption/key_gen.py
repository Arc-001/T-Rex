#importing key generator and unique id labler
from pgpy import PGPKey, PGPUID, PGPMessage
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm

class key:
    def __init__(self, uuid: str, hostname: str, password:str):
        self.key = self.gen_key(uuid, hostname, password)
        self.uuid = uuid
        self.hostname = hostname
        self.password = password


    def gen_key(self,uuid: str, hostname: str, password:str):
        #make a new key object
        self.key = PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 2048)
        
        #makeing the lable for the key
        uid = PGPUID.new(uuid, email = hostname, comment= password)

        #attaching the lable to the key
        

        '''
        alternative compressions for future reference

        CompressionAlgorithm.ZIP,
        CompressionAlgorithm.ZLIB,
        CompressionAlgorithm.BZ2,
        CompressionAlgorithm.Uncompressed
        '''
        
        self.key.add_uid(
            uid,
            usage = [KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage],
            hashes = [HashAlgorithm.SHA256],
            ciphers = [SymmetricKeyAlgorithm.AES256],
            compress = [CompressionAlgorithm.Uncompressed]

        )
        return self.key

    def save_key(self, path: str):

        #save private key
        with open(path, "w") as key_file_private:
            key_file_private.write(str(self.key))

        #save the private key
        with open(f"{path}.pub", "w") as key_file_public:
            key_file_public.write(str(self.key.pubkey))

    def get_key(self):
        return self.key


# def get_key_path(path:str):

#     return PGPKey.from_file(path)

'''
TODO:
encrypt the private key by using 
key.protect("your-strong-passphrase", SymmetricKeyAlgorithm.AES256, HashAlgorithm.SHA256)

and unlock using 
with my_key.unlock("password"):
'''

def encrypt_message_file(pub_key : str, message_str:str):
    pub_key, info = PGPKey.from_file(pub_key)
    info = dict(info)
    # printing the key info
    print("-----------------info in the key-----------------")
    for key in info:
        print (f"{key}: {info[key]}")

    #create the message object to work with encryption in pypg
    message = PGPMessage.new(f"{message_str}")

    #encrypting the message

    encrypted = pub_key.encrypt(message)


    #printing the encrypted message for debugging
    print ("-----------------encrypted message-----------------")
    print (f"encrypted message is {encrypted}")

    return str(encrypted)
    

def decrypt_message(priv_key:str, enc_message:str):
    private_key, info = PGPKey.from_file(priv_key)
    info = dict(info)
    # printing the key info
    print("-----------------info in the key-----------------")
    for key in info:
        print (f"{key}: {info[key]}")

    #making a message object to work with decryption in pypg
    enc_msg = PGPMessage.from_blob(enc_message)

    #decrypting the message
    decrypted = private_key.decrypt(enc_msg)

    #printing the decrypted message for debugging
    print ("-----------------decrypted message-----------------")
    print (f"decrypted message is {decrypted.message}")
    

    return str(decrypted)



