import os
import subprocess

def install_packages():
    print("Updating package list...")
    os.system('sudo apt-get update')
    
    print("Installing OpenSSH server...")
    os.system('sudo apt-get install -y openssh-server')
    
    print("Installation complete.")

def configure_sftp():
    sshd_config_path = '/etc/ssh/sshd_config'
    
    # Backup the original sshd_config file
    os.system(f'sudo cp {sshd_config_path} {sshd_config_path}.backup')
    
    with open(sshd_config_path, 'a') as sshd_config:
        sshd_config.write('\n')
        sshd_config.write('Match Group sftpusers\n')
        sshd_config.write('    ChrootDirectory %h\n')
        sshd_config.write('    ForceCommand internal-sftp\n')
        sshd_config.write('    AllowTcpForwarding no\n')
        sshd_config.write('    X11Forwarding no\n')
    
    print("Configuration complete.")

def create_sftp_user(username):
    print(f"Creating user {username}...")
    os.system(f'sudo useradd -m -G sftpusers -s /bin/false {username}')
    os.system(f'sudo passwd {username}')
    
    user_home_dir = f'/home/{username}'
    os.system(f'sudo chown root:root {user_home_dir}')
    os.system(f'sudo chmod 755 {user_home_dir}')
    
    sftp_dir = f'{user_home_dir}/uploads'
    os.system(f'sudo mkdir -p {sftp_dir}')
    os.system(f'sudo chown {username}:{username} {sftp_dir}')
    
    print(f"User {username} created and configured for SFTP.")

def restart_sshd():
    print("Restarting SSH service...")
    os.system('sudo systemctl restart sshd')
    print("SSH service restarted.")

def main():
    install_packages()
    configure_sftp()
    
    username = input("Enter the username for the SFTP user: ").strip()
    create_sftp_user(username)
    
    restart_sshd()
    print("SFTP server setup complete.")

if __name__ == '__main__':
    main()
