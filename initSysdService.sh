#!/bin/bash

SERVICE_PATH="/etc/systemd/system/"

cd $(dirname $0)

function createServiceFile(){
    if [[ -z "$1" ]];then
        echo "$FUNCNAME - An argument is needed"
        return 1
    fi
    target="${SERVICE_PATH}$1"
    if [[ -f "$target" ]];then
        echo "$FUNCNAME - Systemd service file <${target}> already exists"
        return 1
    fi

    sed "s@{WORKING_DIR}@$PWD@g" "$PWD/$1" > "$target"
    return $?
}

function main(){

    pip3 install discord python-dotenv

    
    if [[ ! -d "${SERVICE_PATH}" ]];then
        echo "Systemd services path <$SERVICE_PATH> not found"
        return
    fi

    for f in *.service; do
        echo "Creating -- $f"
        createServiceFile "$f"
    done
}

main