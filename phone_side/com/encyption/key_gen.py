#importing key generator and unique id labler
from pypg import PGPKey, PGPUID
from pypg.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm

class key:
    def __init__(self, uuid: str, hostname: str, password:str):
        self.key = self.gen_key(uuid, hostname, password)
        self.uuid = uuid
        self.hostname = hostname
        self.password = password


    def gen_key(uuid: str, hostname: str, password:str):
        #make a new key object
        key = PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 2048)
        
        #makeing the lable for the key
        uid = PGPUID.new(uuid, hostname = hostname, password = password)

        #attaching the lable to the key
        key.add_uid(
            uid,
            usage = [KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage],
            hashes = [HashAlgorithm.SHA256],
            ciphers = [SymmetricKeyAlgorithm.AES256],
            compress = [CompressionAlgorithm.Uncompressed]
            '''
            alternative compressions for future reference

            CompressionAlgorithm.ZIP,
            CompressionAlgorithm.ZLIB,
            CompressionAlgorithm.BZ2,
            CompressionAlgorithm.Uncompressed
            '''
        )

    def save_key(self, path: str):

        #save private key
        with open(path, "w") as key_file_private:
            key_file_private.write(str(key))

        #save the private key
        with open(f"{path}.pub", "w") as key_file_public:
            key_file_public.write(str(key.pubkey))

    def get_key(self):
        return self.key




