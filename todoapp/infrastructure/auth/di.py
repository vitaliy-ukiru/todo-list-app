import os

import aiofiles
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from todoapp.common.settings import AuthConfig
from todoapp.infrastructure.auth.jwt import RSAAuthenticator


async def _read_file(path: str) -> bytes:
    async with aiofiles.open(path, 'rb') as f:
        return await f.read()


async def get_jwt_authenticator(
    config: AuthConfig
):
    try:
        private_key_bytes = await _read_file(config.private_key_path)
    except FileNotFoundError as err:
        raise ValueError("JWT Private key file not found") from err

    private_key = serialization.load_pem_private_key(private_key_bytes, password=None)
    if not isinstance(private_key, RSAPrivateKey):
        raise ValueError("Private key must be RSA")

    public_key = private_key.public_key()
    return RSAAuthenticator(
        access_token_expires=config.access_token_expires,
        refresh_token_expires=config.refresh_token_expires,
        private_key=private_key,
        public_key=public_key,
        hash_alg=config.jwt_alg,
    )
