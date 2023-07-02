from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
import base64
import os


def generate_keys():
    # Gera uma chave privada e sua chave pública correspondente
    modulus_length = 4096
    private_key = RSA.generate(modulus_length)
    public_key = private_key.publickey()
    return private_key, public_key


def encrypt_message(message, public_key):
    # Criptografa uma mensagem usando a chave pública fornecida
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_msg = cipher.encrypt(message)
    encoded_encrypted_msg = base64.b64encode(encrypted_msg)
    return encoded_encrypted_msg


def decrypt_message(encrypted_msg, private_key):
    # Descriptografa uma mensagem criptografada usando a chave privada fornecida
    cipher = PKCS1_OAEP.new(private_key)
    decoded_encrypted_msg = base64.b64decode(encrypted_msg)
    decrypted_msg = cipher.decrypt(decoded_encrypted_msg)
    return decrypted_msg


def generate_secret_key_for_AES_cipher():
    # Gera uma chave secreta para o algoritmo AES
    AES_key_length = 32
    secret_key = os.urandom(AES_key_length)
    encoded_secret_key = base64.b64encode(secret_key)
    return encoded_secret_key


def encrypt_message_AES(private_msg, encoded_secret_key, padding_character):
    # Criptografa uma mensagem usando o algoritmo AES com a chave secreta fornecida
    secret_key = base64.b64decode(encoded_secret_key)
    cipher = AES.new(secret_key, AES.MODE_ECB)
    padded_private_msg = private_msg + (padding_character * ((16 - len(private_msg)) % 16))
    encrypted_msg = cipher.encrypt(padded_private_msg)
    encoded_encrypted_msg = base64.b64encode(encrypted_msg)
    return encoded_encrypted_msg


def decrypt_message_AES(encoded_encrypted_msg, encoded_secret_key, padding_character):
    # Descriptografa uma mensagem criptografada usando o algoritmo AES com a chave secreta fornecida
    secret_key = base64.b64decode(encoded_secret_key)
    encrypted_msg = base64.b64decode(encoded_encrypted_msg)
    cipher = AES.new(secret_key, AES.MODE_ECB)
    decrypted_msg = cipher.decrypt(encrypted_msg)
    unpadded_private_msg = decrypted_msg.rstrip(padding_character)
    return unpadded_private_msg
