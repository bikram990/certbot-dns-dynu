#!/usr/bin/zsh
git_setup() {
    git config --global --add safe.directory /opt/app
    git config --global pull.rebase true
    git config --global --add --bool push.autoSetupRemote true
}

zsh_setup() {
    sudo cp /root/.zshrc ~/.zshrc
    sudo cp -r /root/.oh-my-zsh ~/.oh-my-zsh
    sudo chown -R $UID.$GID ~/.zshrc ~/.oh-my-zsh
    zstyle ':omz:update' mode disabled
}

install_required_packages() {
    sudo apt-get update
    sudo apt install vim iputils-ping bind9-utils dnsutils -y
}

python_setup() {
    (echo '# Add user python packages bin to PATH'; echo 'export PATH="$HOME/.local/bin:$PATH"') >> ~/.zshrc
    export PATH="$HOME/.local/bin:$PATH"
    sudo rm -Rf .venv/*
    python3 -m venv .venv
    . .venv/bin/activate
    python -m pip install --upgrade pip
}

app_setup() {
    python -m pip install --no-cache-dir --force-reinstall -r .devcontainer/requirements.txt \
    -r .devcontainer/build-requirements.txt -r requirements.txt -r src/tests/requirements.txt
    pre-commit install
}

container_setup() {
    zsh_setup
    git_setup &
    install_required_packages &
    python_setup &

    wait

    . .venv/bin/activate
    app_setup
}

usage() {
    echo "$0 <action>"
    echo "$1 is invalid action"
    echo "valid actions setup, dep, python"
    echo "setup will run all the steps run at dev container creation"
    echo "dep will install python dependencies"
    echo "python will recreate the python venv and install python dependencies"
    exit 64
}

action=$1

case $action in
  dep)
    . .venv/bin/activate
    app_setup
    ;;
  python)
    python_setup
    . .venv/bin/activate
    app_setup
    ;;
  help)
    usage $action
    ;;
  *)
    container_setup
    ;;
esac
