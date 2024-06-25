from dataclasses import dataclass
from uuid import UUID

from todoapp.application.auth import dto
from todoapp.application.auth.interfaces.repository import TokensRepo, TokenKey
from todoapp.application.auth.jwt import JWTAuthenticator
from todoapp.application.common.command import Command, CommandHandler
from todoapp.domain.user.entities import UserId


@dataclass(frozen=True)
class ProduceTokens(Command[dto.Tokens]):
    user_id: UUID


@dataclass
class ProduceTokensHandler(CommandHandler[ProduceTokens, dto.Tokens]):
    repo: TokensRepo
    auth: JWTAuthenticator

    async def __call__(self, command: ProduceTokens) -> dto.Tokens:
        user_id = UserId(command.user_id)

        access_token = self.auth.create_access_token(user_id=user_id)
        refresh_token = self.auth.create_refresh_token(user_id)

        await self.repo.save_token(
            TokenKey(
                user_id=user_id,
                refresh_token_id=refresh_token.token_id,
            ),
            access_token_id=access_token.token_id
        )

        return dto.Tokens(
            access_token=access_token.raw,
            refresh_token=refresh_token.raw,
        )
