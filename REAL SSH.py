import re
import pexpect

# Define variables
ip_address = '192.168.56.101'
username = input('Enter Username (e.g., prne): ')
password = input('Enter Password (e.g., cisco123!): ')
password_enable = 'class123!'

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

# Send a command to show the running configuration
session.sendline('show running-config')
result = session.expect([r'#', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if it exists then display an error and exit
if result != 0:
    print('Failed to execute the command')
    exit()

# Get the configuration output
config_output = session.before

# Save the configuration to a local file
with open('running-config.txt', 'w') as config_file:
    config_file.write(config_output)

# Displaying a success message if it works
print('------------------------------------------------------')
print('')
print('Successfully connected to IP address:', ip_address)
print('Username:', username)
print('Password: ********')  # Masking the password for security
print('New Hostname: R3')
print('Running configuration saved to running-config.txt')
print('')
print('------------------------------------------------------')

# Terminating the SSH session
session.close()
