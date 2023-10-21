import pexpect

# Define Variables
ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'
hostname = 'R3'  # Add the hostname variable

# Create telnet session
session = pexpect.spawn('telnet ' + ip_address, encoding='utf-8', timeout=20)

result = session.expect(['Username:', pexpect.TIMEOUT])

# Check for error, if exists then display error and exit
if result != 0:
    print('--- FAILURE! creating session for: ', ip_address)
    exit()

# Session is expecting username, enter details
session.sendline(username)
result = session.expect(['Password:', pexpect.TIMEOUT])

# Check for error, if exists then display error and exit
if result != 0:
    print('--- FAILURE! entering username:', username)
    exit()

# Session is expecting password, enter details
session.sendline(password)
result = session.expect(['#', pexpect.TIMEOUT])

# Check for error, if exists then display error and exit
if result != 0:
    print('--- FAILURE! entering password:', password)
    exit()

# Send the hostname command
session.sendline('conf t')
session.expect(['\(config\)#'])
session.sendline('hostname R3')  # Set the hostname to 'R3'
session.expect(['\(config\)#'])
session.sendline('end')
session.expect(['#'])

# Save the running configuration to a file locally
session.sendline('term len 0')  # Set terminal length to 0 to prevent pagination
session.sendline('show running-config')  # Display running configuration
session.logfile = open('running-config.txt', 'w')  # Open a file to save the output
session.expect(['#'])
session.logfile = None  # Close the file

# Display a success message if it works
print('-------------------------------------------------')
print('')
print('--- Success! connecting to:', ip_address)
print('---               Username:', username)
print('---               Password:', password)
print('---               Hostname:', hostname)
print('--- Running configuration saved as running-config.txt')
print('')
print('---------------------------------')

# Terminate telnet to the device and close the session
session.sendline('quit')
session.close()
