filepath="./Dockerfile"
imagename="ansible-server"
containername="ansible-container"
REMOTE_USER="songprem94"


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
    docker run -d -it --name $containername -v /home/song/.ssh:/home/song/.ssh -v ./ansible-setup:/home/song/ansible-setup -e REMOTE_USER=$REMOTE_USER $imagename
else 
    echo "file not exist"
fi