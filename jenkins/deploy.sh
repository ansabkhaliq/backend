# .bash_profile
# Get the aliases and functions
sudo docker stop db  | echo "SUCCESS"
sudo docker rm db | echo "SUCCESS"
sudo docker stop backend  | echo "SUCCESS"
sudo docker rm backend | echo "SUCCESS"
echo "y" | sudo docker system prune -a
sudo docker network create myNetwork  | echo "SUCCESS"
sudo docker pull 80869538/db
sudo docker run -d -p 3306:3306 --name db --net=myNetwork 80869538/db:latest
until echo "squizz" | sudo  -S docker exec -i db mysql --user=root --password=squizz   <<EOF
exit
EOF
do
   sleep 3
   echo "waiting for mysql ..."
done
echo "starting the main script"
sudo docker pull 80869538/backend
sudo docker run -d -p 5000:5000 --name backend --net=myNetwork 80869538/backend:latest

