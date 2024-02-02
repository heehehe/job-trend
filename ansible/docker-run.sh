imagename="ansible-server"
if docker images | grep -q "$imagename" ; then 
    echo "exist image $imagename"
    docker run -d -it --name ansible-container -v ./ansible-setup:/home/song/ansible-setup $imagename
else
    echo "fail"
fi