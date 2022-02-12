import typing
from typing import Dict
from ..api.rest import Route, RESTClient
from ..snowflake import Snowflakeish
from ..flags import MessageFlags
from ..types import allowed_mentions

class Commands:
    def __init__(self, rest: RESTClient):
        self.rest = rest
    
    def create_global_application_command(
        self,
        application_id: Snowflakeish,
        name: str,
        description: str,
        options: typing.Optional[typing.List[Dict]] = None,
        default_permission: typing.Optional[bool] = True,
        type: int = 1,
    ):
        json = {
            'name': name,
            'description': description,
            'type': type,
        }
        if default_permission is False:
            json['default_permission'] = False
        if options:
            json['options'] = options
        return self.rest.send(
            Route('POST', f'/applications/{application_id}/commands'), json=json
        )

    def get_global_application_command(
        self, application_id: Snowflakeish, command: Snowflakeish
    ):
        return self.rest.send(
            Route('GET', f'/applications/{application_id}/commands/{command}')
        )

    def edit_global_application_command(
        self,
        application_id: Snowflakeish,
        command_id: Snowflakeish,
        name: str,
        description: str,
        options: typing.Optional[typing.List[Dict]] = None,
        default_permission: typing.Optional[bool] = True,
    ):
        json = {
            'name': name,
            'description': description,
            'default_permission': default_permission,
        }
        if options:
            json['options'] = options
        return self.rest.send(
            Route('PATCH', f'/applications/{application_id}/commands/{command_id}'),
            json=json,
        )

    def get_global_application_commands(self, application_id: Snowflakeish):
        return self.rest.send(Route('GET', f'/applications/{application_id}/commands'))

    def delete_global_application_command(
        self,
        application_id: int,
        command: int,
    ):
        return self.rest.send(
            Route(
                'DELETE',
                f'/applications/{application_id}/commands/{command}',
            )
        )

    # Guild Commands

    def create_guild_application_command(
        self,
        application_id: Snowflakeish,
        guild_id: Snowflakeish,
        name: str,
        description: str,
        options: typing.Optional[typing.List[Dict]],
        default_permission: typing.Optional[bool] = True,
        type: int = 1,
    ):
        json = {
            'name': name,
            'description': description,
            'default_permission': default_permission,
            'type': type,
        }
        if default_permission is False:
            json['default_permission'] = False
        if options:
            json['options'] = options
        return self.rest.send(
            Route('POST', f'/applications/{application_id}/guilds/{guild_id}/commands'),
            json=json,
        )

    def get_guild_application_command(
        self,
        application_id: Snowflakeish,
        guild_id: Snowflakeish,
        command: Snowflakeish,
    ):
        return self.rest.send(
            Route(
                'GET',
                f'/applications/{application_id}/guilds/{guild_id}/commands/{command}',
            )
        )

    def get_guild_application_commands(
        self,
        application_id: Snowflakeish,
        guild_id: Snowflakeish,
    ):
        return self.rest.send(
            Route(
                'GET',
                f'/applications/{application_id}/guilds/{guild_id}/commands',
            )
        )

    def delete_guild_application_command(
        self,
        application_id: int,
        guild_id: int,
        command: int,
    ):
        return self.rest.send(
            Route(
                'DELETE',
                f'/applications/{application_id}/guilds/{guild_id}/commands/{command}',
                guild_id=guild_id,
            )
        )

    def edit_guild_application_command(
        self,
        application_id: Snowflakeish,
        command_id: Snowflakeish,
        guild_id: Snowflakeish,
        name: str,
        description: str,
        options: typing.Optional[typing.List[Dict]] = None,
        default_permission: typing.Optional[bool] = True,
    ):
        json = {
            'name': name,
            'description': description,
            'default_permission': default_permission,
        }
        if options:
            json['options'] = options
        return self.rest.send(
            Route(
                'PATCH',
                f'/applications/{application_id}/guilds/{guild_id}/commands/{command_id}',
            ),
            json=json,
        )

    # interaction response.

    def create_interaction_response(
        self,
        interaction_id: int,
        interaction_token: str,
        content: str,
        embeds: typing.Optional[typing.List[typing.Dict]] = None,
        tts: typing.Optional[bool] = False,
        allowed_mentions: typing.Optional[allowed_mentions.MentionObject] = None,
        flags: typing.Optional[MessageFlags] = None,
        components: typing.Optional[dict] = None,
    ):
        json = {
            'content': content,
        }
        if embeds is not None:
            json['embeds'] = embeds
        if tts is not False:
            json['tts'] = tts
        if allowed_mentions is not None:
            json['allowed_mentions'] = allowed_mentions
        if flags is not None:
            json['flags'] = flags
        if components is not None:
            json['components'] = components
        return self.rest.send(
            Route(
                'POST',
                f'/interactions/{interaction_id}/{interaction_token}/callback',
            ),
            json=json,
        )

    def get_initial_response(self, application_id, interaction_token):
        return self.rest.send(
            Route('GET', f'/webhooks/{application_id}/{interaction_token}/@original')
        )

    # TODO: Edit and Delete initial reponse.

    def create_followup_message(
        self,
        application_id,
        interaction_token,
        content: str,
        embeds: typing.Optional[typing.List[dict]] = None,
        allowed_mentions: typing.Optional[allowed_mentions.MentionObject] = None,
        components: typing.Optional[typing.List[Dict]] = None,
        flags: typing.Optional[MessageFlags] = None,
    ):
        json = {'content': content}
        if embeds is not None:
            json['embeds'] = embeds
        if allowed_mentions is not None:
            json['allowed_mentions'] = allowed_mentions
        if components is not None:
            json['components'] = components
        if flags is not None:
            json['flags'] = flags
        return self.rest.send(
            Route('POST', f'/webhooks/{application_id}/{interaction_token}'), json=json
        )

    def get_followup_message(
        self,
        application_id,
        interaction_token,
        message,
    ):
        return self.rest.send(
            Route(
                'GET',
                f'/webhooks/{application_id}/{interaction_token}/messages/{message}',
            ),
        )

    # TODO: Edit and Delete followup message