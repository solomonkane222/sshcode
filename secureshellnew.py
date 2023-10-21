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

# Save the output to a local file
with open('command_output.txt', 'w') as output_file:
    output_file.write(command_output)

# Display a success message
print('------------------------------------------------------')
print('')
print('Successfully connected to IP address:', ip_address)
print('Username:', username)
print('Password: ********')  # Masking the password for security
print('Command Output saved to command_output.txt')
print('')
print('------------------------------------------------------')

# Terminating the SSH session
session.close()
