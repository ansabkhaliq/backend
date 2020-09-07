until mysql --user=root --password=squizz -h 0.0.0.0  <<EOF
exit
EOF
do
   sleep 3
   echo "waiting for mysql ..."
done
echo "starting the main script"