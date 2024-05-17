import os
import subprocess

def install_packages():
    print("Updating package list...")
    os.system('sudo apt-get update')
    
    print("Installing OpenSSH server...")
    os.system('sudo apt-get install -y openssh-server')
    os.system('sudo systemctl start sshd')

def configure_sftp():
    sshd_config_path = '/etc/ssh/sshd_config'
    
    with open(sshd_config_path, 'a') as sshd_config:
        sshd_config.write('\n')
        sshd_config.write('PasswordAuthentication yes')
        sshd_config.write('\n')
        sshd_config.write('Match Group sftpusers\n')
        sshd_config.write('    ChrootDirectory /srv/sftp\n')
        sshd_config.write('    ForceCommand internal-sftp\n')
        sshd_config.write('    AllowTcpForwarding no\n')
        sshd_config.write('    X11Forwarding no\n')
    
    print("Configuration complete.")

def create_sftp_user(username):
    print(f"Creating user {username}...")
    os.system('sudo mkdir /srv/sftp')
    os.system('sudo groupadd sftpusers')
    os.system(f'sudo useradd -G sftpusers -d /srv/sftp/{username} -s /sbin/nologin {username}')
    os.system(f'sudo passwd {username}')
    print(f"User {username} created and configured for SFTP.") 

def restart_sshd():
    print("Restarting SSH service...")
    os.system('sudo systemctl restart sshd')
    print("SSH service restarted.")
    
def create_start_directory(username):
    name=input("Enter the name of first directory: ")
    os.system(f'sudo mkdir /srv/sftp/{name}')
    os.system(f'sudo chown {username}:sftpusers /srv/sftp/{name}')
    

def main():
    install_packages()
    configure_sftp()
    
    username = input("Enter the username for the SFTP user: ").strip()
    create_sftp_user(username)
    
    restart_sshd()
    create_start_directory(username)
    print("SFTP server setup complete.")

if __name__ == '__main__':
    main()
