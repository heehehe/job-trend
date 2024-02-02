filepath="./Dockerfile"
imagename="ansible-server"


if docker images | grep -q "$imagename" ; then 
    echo "exist image $imagename"
    docker run -d -it --name ansible-container -v /home/song/.ssh:/home/song/.ssh $imagename
elif [ -e "$filepath" ] ; then
    echo "build start {{ $imagename }} "
    docker build -t "$imagename" .
else 
    echo "file not exist"
fi