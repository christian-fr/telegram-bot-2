import json
from tinydb import TinyDB, Query
from pathlib import Path
import asyncio

from typing import Any, List
import subprocess
import time

import os

from pydantic import BaseSettings

# load secrets (phone number)
secret = Path('secret').read_text()


def convert_epoch_timestamp_into_str(epoch_timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(epoch_timestamp) / 1000))


class Settings(BaseSettings):
    signal_config_path: str = os.environ.get(
        "SIGNAL_CONFIG_PATH", os.path.expanduser("~/.local/share/signal-cli")
    )
    signal_upload_path: str = f"{signal_config_path}/uploads/"
    signal_attachments_path: str = f"{signal_config_path}/attachments/"
    signal_cli_executable: str = os.environ.get('SIGNAL_EXEC_PATH', os.path.expanduser('~/signal-cli_built/bin/signal-cli'))
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

db = TinyDB('database.json')
for envelope_dict in json_data_list:
    envelope = envelope_dict['envelope']
    sender = envelope['source']
    timestamp = envelope['timestamp']
    timestamp_str = convert_epoch_timestamp_into_str(timestamp)

    attachment = envelope_dict['envelope']['dataMessage']['attachments']

    attachment_file_str_list = []
    attachment_path_str_list = []
    if attachment:
        for attachment_item in attachment:
            attachment_path = Path(settings.signal_attachments_path, attachment_item['id'])
            if attachment_path.exists():
                attachment_path_str_list.append(attachment_path)
    db.insert({'timestamp': envelope_dict['envelope']['timestamp'], 'timestamp_str': timestamp_str, 'sender': sender,
               'has_attachment': bool(attachment), 'attachment_file_str_list': attachment_file_str_list,
               'envelope': envelope_dict['envelope']})
