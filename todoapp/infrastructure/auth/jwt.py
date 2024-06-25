from datetime import timedelta
from typing import Any

import jwt
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from todoapp.application.auth.jwt import JWTAuthenticator

ALLOWED_RSA_ALGORITHMS = frozenset({"RS256", "RS384", "RS512"})


class RSAAuthenticator(JWTAuthenticator):

    def __init__(
        self,
        access_token_expires: timedelta,
        refresh_token_expires: timedelta,
        private_key: RSAPrivateKey | str | bytes,
        public_key: RSAPublicKey | str | bytes,
        hash_alg: str = "RS256"
    ):
        super().__init__(access_token_expires, refresh_token_expires)

        self.__private_key = private_key
        self.__public_key = public_key
        if hash_alg not in ALLOWED_RSA_ALGORITHMS:
            raise ValueError(f"hash_alg {hash_alg} is not a valid RSA hash algorithm")
        self.__hash_alg = hash_alg

    def _encode(self, payload: dict[str, Any]) -> str:
        return jwt.encode(payload, self.__private_key, self.__hash_alg)

    def _decode(self, token: str, verify_exp: bool) -> dict[str, Any]:
        return jwt.decode(
            jwt=token,
            key=self.__public_key,
            algorithms=[self.__hash_alg],
            options={
                "verify_exp": verify_exp,
            }
        )
