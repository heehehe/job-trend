filepath="./Dockerfile"
imagename="ansible-server"
containername="ansible-container"


if docker images | grep -q "$imagename" ; then 
    if docker ps -a | grep -q "$containername" ; then
        echo "exist container $containername so will remove previous container"
        docker rm -f $containername
    fi
    echo "exist image $imagename so will remove previous image"
    docker rmi -f $imagename
fi

if [ -e "$filepath" ] ; then
    echo "build start {{ $imagename }} "
    docker build -t "$imagename" .
    echo "create container $containername"
    docker run -d -it --name $containername --rm -v $HOME/.ssh:/home/.ssh -v ./ansible-setup:/home/ansible-setup -e REMOTE_USER=$TF_VAR_vm_user -e VM_SSH_KEY=$TF_VAR_vm_ssh_key $imagename
else 
    echo "file not exist"
fi