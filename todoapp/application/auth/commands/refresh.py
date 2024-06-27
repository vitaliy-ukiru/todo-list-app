from dataclasses import dataclass

from didiator import CommandMediator

from todoapp.application.auth import dto
from todoapp.application.auth.exceptions import MismatchedAccessToken
from todoapp.application.auth.interfaces.repository import TokensRepo, TokenKey
from todoapp.application.auth.jwt import JWTAuthenticator
from todoapp.application.common.command import Command, CommandHandler
from .produce import ProduceTokens


@dataclass
class RefreshTokens(Command[dto.Tokens]):
    refresh_token: str
    access_token: str


@dataclass
class RefreshTokensHandler(CommandHandler[RefreshTokens, dto.Tokens]):
    repo: TokensRepo
    auth: JWTAuthenticator
    mediator: CommandMediator

    async def __call__(self, command: RefreshTokens) -> dto.Tokens:
        # validate refresh token
        refresh_token = self.auth.decode_refresh_token(command.refresh_token)
        access_token = self.auth.decode_access_token(command.access_token, False)

        if refresh_token.user_id != access_token.user_id:
            raise MismatchedAccessToken()

        key = TokenKey(user_id=refresh_token.user_id, refresh_token_id=refresh_token.token_id, )
        db_access_token_id = await self.repo.get_token(
            token_key=key
        )

        if access_token.token_id != db_access_token_id:
            raise MismatchedAccessToken()

        await self.repo.delete_token(key)

        new_tokens_pair = await self.mediator.send(ProduceTokens(
            refresh_token.user_id
        ))
        return new_tokens_pair
