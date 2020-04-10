if [ -z "$1" ]
then
  echo "No endpoint supplied"
  exit 1
fi

echo $HEALTH_DIR

mkdir -p $HEALTH_DIR
health_file=$HEALTH_DIR/mount

while true;
do
  ping -c1 $1 
  if [ $? -eq 0 ]
  then
    echo $(date +%s) > $health_file
    sleep 2
  else
    echo -1 > $health_file
  fi
done
