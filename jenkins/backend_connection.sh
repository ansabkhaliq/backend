for i in `seq 1 10`;
    do
        nc -z localhost 5000 && echo Success && exit 0
        echo -n .
        sleep 10
    done
echo Failed waiting for Postgress && exit 1