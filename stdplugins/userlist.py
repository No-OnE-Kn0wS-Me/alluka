"""Get Administrators of any Chat*
Syntax: .userlist
for all users 
"""
from telethon import events
import os
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantAdmin, ChannelParticipantCreator
from uniborg.util import admin_cmd
from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                          MessageTooLongError)
                                          
@borg.on(admin_cmd(pattern="userlist"))
@borg.on(events.NewMessage(pattern=r"\.userlist ?(.*)", incoming=True))
async def get_users(show):
    """ For .userslist command, list all of the users of the chat. """
    if not show.text[0].isalpha() and show.text[0] not in ("/", "#", "@", "!"):
        if not show.is_group:
            await show.reply("Are you sure this is a group?")
            return
        info = await show.client.get_entity(show.chat_id)
        title = info.title if info.title else "this chat"
        mentions = 'Users in {}: \n'.format(title)
        try:
            if not show.pattern_match.group(1):
                async for user in show.client.iter_participants(show.chat_id):
                    if not user.deleted:
                        mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    else:
                        mentions += f"\nDeleted Account `{user.id}`"
            else:
                searchq = show.pattern_match.group(1)
                async for user in show.client.iter_participants(show.chat_id, search=f'{searchq}'):
                    if not user.deleted:
                        mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    else:
                        mentions += f"\nDeleted Account `{user.id}`"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        try:
            await show.reply_to(mentions)
        except MessageTooLongError:
            await show.reply("Damn, this is a huge group. Uploading users lists as file.")
            file = open("userslist.txt", "w+")
            file.write(mentions)
            file.close()
            await show.client.send_file(
                show.chat_id,
                "userslist.txt",
                caption='Users in {}'.format(title),
                reply_to=show.id,
            )
            os.remove("userslist.txt")
