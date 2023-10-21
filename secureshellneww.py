import re
import pexpect

# Define variables
ip_address = '192.168.56.101'
username = input('Enter Username (e.g., prne): ')
password = input('Enter Password (e.g., cisco123!): ')
password_enable = 'class123!'
command_to_execute = input('Enter the command to execute (e.g., "show running-config"): ')

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

# Send the specified command
session.sendline(command_to_execute)
result = session.expect([r'#', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if it exists then display an error and exit
if result != 0:
    print('Failed to execute the command:', command_to_execute)
    exit()

# Get the command output
command_output = session.before

# Specify the full file path to save the output locally
output_file_path = 'command_output.txt'

# Save the output to the local file
with open(output_file_path, 'w') as output_file:
    output_file.write(command_output)

# Set the hostname to R3
session.sendline('configure terminal')
session.expect([r'#', pexpect.TIMEOUT, pexpect.EOF])
session.sendline('hostname R3')
session.expect([r'#', pexpect.TIMEOUT, pexpect.EOF])
session.sendline('exit')

# Display a success message
print('------------------------------------------------------')
print('')
print('Successfully connected to IP address:', ip_address)
print('Username:', username)
print('Password: ********')  # Masking the password for security
print('Command Output saved to:', output_file_path)
print('Hostname set to R3')
print('')
print('------------------------------------------------------')

# Terminating the SSH session
session.close()
