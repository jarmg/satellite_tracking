root=/home/jared/satellite_imager/ 
main_dir=${root}src 
obs_dir=${root}server/static/observations



sudo PYTHONPATH=$main_dir ROOT_DIR=$root IMAGE_OUTPUT_DIR=$obs_dir python3.5 /home/jared/satellite_imager/server/main.py
