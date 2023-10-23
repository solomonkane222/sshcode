import re
import pexpect

# Define variables
ip_address = '192.168.56.101'
username = input('Enter Username (e.g., prne): ')
password = input('Enter Password (e.g., cisco123!): ')
password_enable = 'class123!'
output_file_path = 'running_config.txt'

# Function to handle errors and exit
def handle_error(message):
    print(message)
    exit()

# Function to execute a command and check for errors
def execute_command(session, command, expected_prompt):
    session.sendline(command)
    result = session.expect([expected_prompt, pexpect.TIMEOUT, pexpect.EOF])
    if result != 0:
        handle_error(f'Failed to execute the command: {command}')

# Create an SSH session
session = pexpect.spawn(f'ssh {username}@{ip_address}', encoding='utf-8', timeout=20)
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    handle_error(f'Failed to create an SSH session for IP address: {ip_address}')

# Enter the password
session.sendline(password)
result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    handle_error(f'Failed to enter the password: ********')

# Enter enable mode
execute_command(session, 'enable', 'Password: ********')

# Send enable password
execute_command(session, password_enable, '#')

# Set the hostname to "Router3"
execute_command(session, 'configure terminal', r'.\(config\)#')
execute_command(session, 'hostname Router3', r'Router3\(config\)#')
execute_command(session, 'exit', '#')

# Execute the "show running-config" command
execute_command(session, 'show running-config', r'#')

# Get the running configuration
running_config = session.before

# Save the running configuration to a local file
with open(output_file_path, 'w') as output_file:
    output_file.write(running_config)

# Display success message
print('------------------------------------------------------')
print('')
print(f'Successfully connected to IP address: {ip_address}')
print(f'Username: {username}')
print('Password: ********')  # Masking the password for security
print('Hostname: Router3')
print(f'Running Configuration saved to: {output_file_path}')
print('')
print('------------------------------------------------------')

# Terminate the SSH session
session.close()
