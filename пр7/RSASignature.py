from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


class RSASignature:
    def generate_keys(self, key_size=2048):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
        public_key = private_key.public_key()
        self.save_private_key(private_key)
        self.save_public_key(public_key)

    def save_private_key(self, private_key, filename="private_key.pem"):
        if private_key is None:
            raise ValueError("Приватний ключ не згенеровано")
        with open(filename, "wb") as key_file:
            key_file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

    def save_public_key(self, public_key, filename="public_key.pem"):
        if public_key is None:
            raise ValueError("Публічний ключ не згенеровано")
        with open(filename, "wb") as key_file:
            key_file.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def load_private_key(self, filename="private_key.pem"):
        with open(filename, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
            return private_key

    def load_public_key(self, filename="public_key.pem"):
        with open(filename, "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())
            return public_key

    def sign(self, message):
        private_key = self.load_private_key()
        if private_key is None:
            raise ValueError("Приватний ключ не згенеровано або не завантажено")
        signature = private_key.sign(
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        with open("signature.sig", "wb") as signature_file:
            signature_file.write(signature)
        return signature

    def load_signature(self, filename="signature.sig"):
        with open(filename, "rb") as signature_file:
            signature = signature_file.read()
            return signature

    def verify(self, message):
        signature = self.load_signature()
        public_key = self.load_public_key()
        if public_key is None:
            raise ValueError("Публічний ключ не згенеровано або не завантажено")
        try:
            public_key.verify(
                signature,
                message.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
