__author__ = 'Lewis'

# Please not that you need to have the cloud.ppk file loaded in putty pageant in order to deploy to the server...
# Please email ilewis_isradd@hotmail.com for a copy of the key.

# You will also need 7zip installed locally.

# Import the Fabric api
from fabric.api import *

# Specify our host
env.user = 'pi'
env.password = 'raspberry'
env.hosts = ['192.168.1.250']

staging_directory = "c:\\Temp\\"
staging_file_name = "Staging.zip"

remote_temp_path = "/tmp/"
remote_running_dir = "/var/feduni_pi_app/"

start_file = "main.py"


def deploy():
    # del might fail if the staging file does not exist...
    with settings(warn_only=True):
        local("del " + staging_directory + staging_file_name)

    local("7z a -tzip " + staging_directory + staging_file_name + " *.py")
    put(staging_directory + staging_file_name, remote_temp_path)

    # kill any python instances, create the remote directory and remove all the files
    with settings(warn_only=True):
        sudo("pkill -9 python")
        sudo("mkdir " + remote_running_dir)
        sudo("rm -R " + remote_running_dir + "*")

    sudo("unzip " + remote_temp_path + staging_file_name + " -d " + remote_running_dir)

    # Spawning this python process in the background was a bit tricky... But this should work.
    #sudo("nohup python " + remote_running_dir + start_file + " & sleep 5")
    #execute("python " + remote_running_dir + start_file)