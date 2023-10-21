import re
import pexpect

# Define variables
ip_address = '192.168.56.101'
username = input('Enter Username (e.g., prne): ')
password = input('Enter Password (e.g., cisco123!): ')
password_enable = 'class123!'
output_file_path = 'running_config.txt'  # Specify the local file name

# Create the SSH session
session = pexpect.spawn('ssh ' + username + '@' + ip_address, encoding='utf-8', timeout=20)
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if it exists then display an error and exit
if result != 0:
    print('Failed to create an SSH session for IP address:', ip_address)
    exit()

# Session expecting a password, entering details...
session.sendline(password)
result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if it exists then display an error and exit
if result != 0:
    print('Failed to enter the password:', password)
    exit()

# Entering enable mode...
session.sendline('enable')
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if it exists then display an error and exit
if result != 0:
    print('Failed to enter enable mode')
    exit()

# Sending enable password...
session.sendline(password_enable)
result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if it exists then display an error and exit
if result != 0:
    print('Failed to enter enable mode after sending the password')
    exit()

# Set the hostname to "Router3"
session.sendline('configure terminal')
result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('Failed to enter configuration mode')
    exit()

session.sendline('hostname Router3')  # Setting the hostname to "Router3"
result = session.expect([r'Router3\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('Failed to set the hostname to Router3')

session.sendline('exit')

# Send the command to show the running configuration
session.sendline('show running-config')
result = session.expect([r'#', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if it exists then display an error and exit
if result != 0:
    print('Failed to execute the command: show running-config')
    exit()

# Get the command output (running configuration)
running_config = session.before

# Save the running configuration to a local file
with open(output_file_path, 'w') as output_file:
    output_file.write(running_config)

# Display a success message
print('------------------------------------------------------')
print('')
print('Successfully connected to IP address:', ip_address)
print('Username:', username)
print('Password: ********')  # Masking the password for security
print('Hostname: Router3')
print('Running Configuration saved to:', output_file_path)
print('')
print('------------------------------------------------------')

# Terminating the SSH session
session.close()
