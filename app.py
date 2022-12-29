from telethon import TelegramClient
import os
import json
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import (
    PeerChannel
)

api_id = os.environ['TELEGRAM_API_ID']
api_hash = os.environ['TELEGRAM_API_HASH']
client = TelegramClient('anon', api_id, api_hash)

async def pp():
    catalog = await client.get_dialogs()
    all_participants = {}
    for dialog in catalog:
        offset = 0
        limit = 100
        try:
            if dialog.is_group:
                all_participants[dialog.name] = []
                curr_participants = []
                my_channel = await client.get_entity(dialog.id)

                while True:
                    participants = await client(GetParticipantsRequest(
                        my_channel, ChannelParticipantsSearch(''), offset, limit,
                        hash=0
                    ))
                    if not participants.users:
                        break
                    curr_participants.extend(participants.users)
                    offset += len(participants.users)

                for participant in curr_participants:
                    all_participants[dialog.name].append(participant.username)

        except Exception as e:
            print(e)

    with open('/Users/georgebredis/Data/TelegramNetworkData/data_v1.json', 'w') as outfile:
        json.dump(all_participants, outfile)

with client:
    client.loop.run_until_complete(pp())
