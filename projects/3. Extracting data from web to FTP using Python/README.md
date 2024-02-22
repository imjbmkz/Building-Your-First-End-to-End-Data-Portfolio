# Extracting data from web to FTP using Python

## Setting-up 

### Python
Install the latest version of Python [here](https://www.python.org/).

### WSL
Install WSL in Windows. See guide [here](https://learn.microsoft.com/en-us/windows/wsl/install).

**Steps to install WSL:**
1. Open PowerShell as an administrator.
2. Run `wsl -l -o` to see available distros that can be installed.
3. Run `wsl --install` to install the default distro (Ubuntu). To select a different distro, run `wsl --install -d <Distribution Name>`.
4. You may need to restart your device after installation for the changes to take effect.
5. You will be prompted to create a new user. Enter your preferred username and set a password.

**Steps to install `vsftpd`:**
1. Open PowerShell and run `wsl` to login to WSL.
2. Check for available updates and install them by running `sudo apt update && sudo apt upgrade`.
3. Install `vsftpd` by running `sudo apt install vsftpd`.

**Update `vsftpd` configuration**
1. Create a copy of the `vsftpd.conf` file by running `sudo cp /etc/vsftpd.conf /etc/vsftpd.conf_original`. 
2. Open the `vsftpd.conf` in a text editor (`nano`) to edit some settings. To do so, run `sudo nano etc/vsftpd.conf`. 
3. Ensure that the following parameters has their corresponding values. Leave everything as default.
```
local_enable=YES
write_enable=YES
chroot_local_user=YES
chroot_list_enable=YES
chroot_list_file=/etc/vsftpd.chroot_list # or just uncomment 
ssl_enable=YES
require_ssl_reuse=NO # add to the bottom of the file
```
4. To save the changes, press `CTRL` + `S` or `CTRL` + `O`. To close the file, press `CTRL` + `X`.
5. Create the `vsftpd.chroot_list` file which will contain the list of users to chroot. Run `sudo nano /etc/vsftpd.chroot_list` to create a blank file called `vsftpd.chroot_list`. On the first line, simply add your WSL username (or the user that you will use for FTP).  
6. Restart the `vsftpd` service by running `sudo systemctl restart vsftpd`. Check the status by running `sudo systemctl status vsftpd` to ensure that the service is running.
7. Take WSL ip address by running `ip address`.

**Create FTP user**
1. Create a Linux user by running `sudo adduser ftpuser`. You may use a different username by replacing `ftpuser` with your preferred username. Enter the password for the new user. Optionally, you can add the user details on the prompt. Press enter to skip.
2. Create a directory that we will use for the exercise. `sudo mkdir /home/ftpuser/ftp`. 
3. Change the ownership of the new folder. `sudo chown nobody:nogroup /home/ftpuser/ftp`.
4. Remove the root access from the new user. `sudo chmod a-w /home/ftpuser/ftp`.
5. Add the new user to the `vsftpd.chroot_list` file. `echo "ftpuser" | sudo tee -a /etc/vsftpd.chroot_list`.

**Testing FTP connection in Python**
Here's a simple Python script that tests connection to the FTP server.
```
from ftplib import FTP_TLS

# FTP details
ftphost = "ip_address" # replace with your FTP ip address or just localhost
ftpuser = "username" # replace with your FTP username
ftppass = "password" # replace with your FTP password

# Login to FTP
ftp = FTP_TLS()
ftp.connect(ftphost, ftpport)
ftp.login(ftpuser, ftppass)
ftp.prot_p() # Fix on 522 Data connections must be encrypted.

# Create sample file
with open("test.txt", "w") as fp:
    fp.write("This is my sample message\n")
    fp.write("Another sample message\n")
    fp.write("bye\n")

# Upload file to FTP 
with open("test.txt", "rb") as fp:
    ftp.storbinary("STOR test_ftp.txt", fp)

# Download file from FTP 
with open("test_download.txt", "wb") as fp:
    ftp.retrbinary("RETR test_ftp.txt",fp.write)

# Delete file from FTP
ftp.delete("test_ftp.txt")

# If this line gets printed, you have successfully 
# established connection to the WSL FTP Server. 
print("Upload, download, delete tests complete")
```

### Creating virtual environment and storing FTP credentials 
1. Open PowerShell and run `python -m venv env` to create a virtual environment called `env`.
2. Open the file `.\env\Scripts\Activate.ps1`.
3. At the bottom of the file, add the following values.
```
# Add FTP user details here
$Env:FTPHOST = "ip_address" # replace with your FTP ip address or just localhost
$Env:FTPUSER = "username" # replace with your FTP username
$Env:FTPPASS = "password" # replace with your FTP password
```
4. You may also add the same details on `.\env\Scripts\activate.bat` for you to store these values when activating virtual environment in Command Prompt.
```
set FTPHOST="ip_address" # replace with your FTP ip address or just localhost
set FTPUSER="ftpuser" # replace with your FTP username
set FTPPASS="password" # replace with your FTP password
```
5. Activate the virtual environment by running `.\env\Scripts\Activate.ps1` on PowerShell or `.\env\Scripts\activate.bat` on Command Prompt.
6. Install the project dependencies by running `pip install -r requirements.txt`.
7. Deactivate the virtual environment by running the command `deactivate`.

## Running the app
1. Activate the virtual environment by running `.\env\Scripts\Activate.ps1` on PowerShell or `.\env\Scripts\activate.bat` on Command Prompt.
2. Run `python app.py`

## Take-home activity
1. Create your version of the pipeline that uses the dataset from [OFAC Consolidated Sanctions List (Non-SDN Lists)](https://ofac.treasury.gov/consolidated-sanctions-list-non-sdn-lists).
2. You may use whichever data format you like. 
3. Download the file, then upload to your local FTP server. 
4. To make you submission, do the following:
   - Post the link to your repository on [Data Engineering Pilipinas](https://www.facebook.com/groups/1225639754738756) Facebook page. Don't be shy to tag me, [Josh Dev](https://www.facebook.com/profile.php?id=100087019650476), and [Data Engineering Pilipinas](https://www.facebook.com/DataEngineeringPilipinas).
   - Post the link to your repository on your LinkedIn page. Feel free to [connect](https://www.linkedin.com/in/josh-valdeleon-2a8984150/) and tag me on the post.