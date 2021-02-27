#!/bin/bash

# needs parameter: version number/tag!

SCRIPT_DIR=$(dirname "$0")
VERSION=$1
REPO="telegram-bot-2"
GITHUBUSER="christian-fr"

DIR=/home/$USER/$REPO
if [ -d "$DIR" ]; then
    printf '%s\n' "Deleting directory ($DIR)"
    rm -rf "$DIR"
fi

mkdir /home/$USER/tmp_$REPO

cp secrets_env_var.sh /home/$USER/tmp_$REPO

cd /home/$USER/

echo "latest release version is:"

echo "https://api.github.com/repos/christian-fr/telegram-bot-2/releases/latest"
curl --silent "https://api.github.com/repos/christian-fr/telegram-bot-2/releases/latest" | grep -Po '"tag_name": "\K.*?(?=")'
echo ""
echo "cloning version: "$1

echo "git clone --depth 1 --branch "$VERSION" https://github.com/"$GITHUBUSER"/"$REPO
git clone --depth 1 --branch $VERSION https://github.com/$GITHUBUSER/$REPO

cp /home/$USER/tmp_$REPO/secrets_env_var.sh /home/$USER/$REPO
rm -rf /home/$USER/tmp_$REPO
