#!/bin/bash

extensions=( 
"ms-python.python" 
"njpwerner.autodocstring"
"formulahendry.code-runner"
"shardulm94.trailing-spaces"
"christian-kohler.path-intellisense"
"kevinrose.vsc-python-indent"
"ypresto.vscode-intelli-refactor"
)

#script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#echo $script_dir
#pushd $script_dir
#extensions=$(sed -e '/^[ \t]*\/\//d' devcontainer.json | jq '.extensions[]' | xargs)
#popd

# make extensions arguments
extensions_arg_str=
for i in ${extensions[@]};  do
    extensions_arg_str="$extensions_arg_str --install-extension $i"
done

pushd $HOME/.vscode-server/bin

server_sh=$(find ./ -name server.sh)
export VSCODE_AGENT_FOLDER=$HOME/.vscode-server
./$server_sh \
--extensions-download-dir $HOME/.vscode-server/extensionsCache \
$extensions_arg_str \
--force

popd
