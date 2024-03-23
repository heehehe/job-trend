if command -v docker &> /dev/null ; then
    echo "Docker already installed"
else
    echo "Docker not installed so will install docker"
    bash $HOME/ansible-setup/docker_install.sh
fi 
