from sqlalchemy import Column, String, UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
import os
from base64 import b64encode
from passlib.context import CryptContext

from nacl.signing import SigningKey
from nacl.secret import SecretBox
from nacl.pwhash import argon2id
from nacl.utils import random
from nacl.encoding import RawEncoder

def decrypt_with_password(encrypted_data_b64: str, password: str) -> bytes:
    data = b64decode(encrypted_data_b64)
    salt = data[:argon2id.SALTBYTES]
    ciphertext = data[argon2id.SALTBYTES:]
    key = derive_key_argon2(password, salt)
    box = SecretBox(key)
    private_key_bytes = box.decrypt(ciphertext)
    return private_key_bytes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Base = declarative_base()

def generate_identity_keys():
    signing_key = SigningKey.generate()
    verify_key = signing_key.verify_key
    return {
        "private_key_bytes": signing_key.encode(RawEncoder),
        "public_key_hex": verify_key.encode(RawEncoder).hex()
    }


# Derive key using Argon2id
def derive_key_argon2(password: str, salt: bytes) -> bytes:
    return argon2id.kdf(
        SecretBox.KEY_SIZE,             # 32 bytes
        password.encode(),
        salt,
        opslimit=argon2id.OPSLIMIT_MODERATE,
        memlimit=argon2id.MEMLIMIT_MODERATE
    )

def encrypt_with_password(private_key_bytes: bytes, password: str) -> str:
    salt = random(argon2id.SALTBYTES)
    key = derive_key_argon2(password, salt)
    box = SecretBox(key)
    ciphertext = box.encrypt(private_key_bytes)  
    return b64encode(salt + ciphertext).decode()

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    identity_key_public = Column(String, nullable=False)
    identity_key_private_encrypted = Column(String, nullable=False)

    @staticmethod
    def create_user(username: str, password: str):
        # Ed25519 SigningKey
        signing_key = SigningKey.generate()
        verify_key = signing_key.verify_key

        
        private_key_bytes = signing_key.encode(RawEncoder)
        public_key_bytes = verify_key.encode(RawEncoder)

       
        encrypted_private_key = encrypt_with_password(keys["private_key"], password)

        
        hashed_password = pwd_context.hash(password)

        return User(
            username=username,
            password_hash=hashed_password,
            identity_key_public=public_key_bytes.hex(),
            identity_key_private_encrypted=encrypted_private_key
        )
