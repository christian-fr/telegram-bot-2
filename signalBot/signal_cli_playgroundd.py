import json
from tinydb import TinyDB, Query
from pathlib import Path
import asyncio

from typing import Any, List
import subprocess
import shutil
import time

from overlayImageRenderer import OverlayImageRenderer

import os

from pydantic import BaseSettings

# load secrets (phone number)
secret = Path('secret').read_text()

# load phonebook
phonebook_dict = json.loads(Path('phonebook').read_text())

# f
# font_file = Path('../overlayImageRenderer/segoeui.ttf')
# font_file = Path('/home/christian/.local/share/fonts/TwitterColorEmoji-SVGinOT.ttf')
font_file = Path('/usr/share/fonts/truetype/ttf-bitstream-vera/VeraMoIt.ttf')
assert font_file.exists()


def convert_epoch_timestamp_into_str(epoch_timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(epoch_timestamp) / 1000))


class Settings(BaseSettings):
    signal_config_path: str = os.environ.get(
        "SIGNAL_CONFIG_PATH", os.path.expanduser("~/.local/share/signal-cli")
    )
    signal_upload_path: str = f"{signal_config_path}/uploads/"
    signal_attachments_path: str = f"{signal_config_path}/attachments/"
    signal_cli_executable: str = os.environ.get('SIGNAL_EXEC_PATH',
                                                os.path.expanduser('~/signal-cli_built/bin/signal-cli'))
    signal_cli_phonebook: dict = phonebook_dict
    assert Path(signal_cli_executable).exists()
    assert Path(signal_config_path).exists()
    signal_number: str = secret


settings = Settings()


def run_signal_cli_command(cmd: List[str], wait: bool = True) -> Any:
    base_cmd = [settings.signal_cli_executable, "--config", settings.signal_config_path]

    full_cmd = " ".join(base_cmd + cmd)

    return subprocess.run(full_cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def get_messages(number: str) -> Any:
    """
    get messages
    """

    response = run_signal_cli_command(["-u", number, "receive", "--json"])
    list_of_bytes = [entry for entry in response.split(b'\n') if entry != b'']
    list_of_json = [json.loads(length_of_bytes.decode('utf-8')) for length_of_bytes in list_of_bytes if
                    json.loads(length_of_bytes.decode('utf-8'))['envelope']['dataMessage'] is not None]
    return list_of_json


json_data_list = get_messages(settings.signal_number)
print(json_data_list)

if json_data_list != []:

    db = TinyDB('database.json')
    for envelope_dict in json_data_list:
        envelope = envelope_dict['envelope']
        sender = envelope['source']
        timestamp = envelope['timestamp']
        timestamp_str = convert_epoch_timestamp_into_str(timestamp)

        attachment = envelope_dict['envelope']['dataMessage']['attachments']

        attachment_path_str_list = []
        if attachment:
            for attachment_item in attachment:
                attachment_path = Path(settings.signal_attachments_path, attachment_item['id'])
                if attachment_path.exists():
                    attachment_path_str_list.append(
                        (os.path.splitext(attachment_item['filename'])[1], attachment_path.as_posix()))
        db.insert(
            {'timestamp': envelope_dict['envelope']['timestamp'], 'timestamp_str': timestamp_str, 'sender': sender,
             'has_attachment': bool(attachment), 'attachment_path_str_list': attachment_path_str_list,
             'envelope': envelope_dict['envelope']})

    Message = Query()
    messages_with_attachment_list = db.search(Message.has_attachment == True)
    messages_with_attachment_list.sort(key=lambda k: k['timestamp'])
    last_message_with_attachment = messages_with_attachment_list[-1]

    sender = last_message_with_attachment['sender']
    text = last_message_with_attachment['envelope']['dataMessage']['message']
    text_escaped = json.dumps(text)

    attachment_ext, attachment_path = last_message_with_attachment['attachment_path_str_list'][0]

    allowed_extensions_list = ['.jpg', '.jpeg', '.png', '.svg', '.tif']

    if attachment_ext in allowed_extensions_list and sender in phonebook_dict.keys():
        sender_name = phonebook_dict[sender]

        full_text = f'{sender_name}: {text}'

        background_file_path = os.path.expanduser('~/background' + attachment_ext)

        shutil.copyfile(attachment_path, background_file_path)

        OverlayImageRenderer.overlay_text(background_image_filename=background_file_path,
                                          overlay_text_string=full_text,
                                          output_file=background_file_path, font_file=font_file.as_posix())

        # run_signal_cli_command(['-u', settings.signal_number, 'send', '-m', '"Data received. This is how the picture will look like."', sender])

        response = run_signal_cli_command(['-u', settings.signal_number, 'send', '-a', background_file_path, '-m', "Picture_Preview", sender])
        print('test')
