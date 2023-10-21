import telnetlib

# Define Variables
ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'
new_hostname = 'NewHostname'

# Establish Telnet Connection
telnet_connection = telnetlib.Telnet(ip_address)
print('11')
# Login to the device
telnet_connection.read_until(b'Username: ')
telnet_connection.write(username.encode('ascii') + b'\n')
telnet_connection.read_until(b'Password: ')
telnet_connection.write(password.encode('ascii') + b'\n')
print('17')
# Enter Privileged EXEC Mode
telnet_connection.read_until(b'#')
#telnet_connection.write(b'enable\n')
#telnet_connection.read_until(b'Password: ')
#telnet_connection.write(password.encode('ascii') + b'\n')
print('23')
# Configure the device
telnet_connection.write(b'configure terminal\n')
telnet_connection.read_until(b'#')
telnet_connection.write(f'hostname {new_hostname}\n'.encode('ascii'))
telnet_connection.read_until(b'#')

# Save the configuration
telnet_connection.write(b'end\n')
telnet_connection.read_until(b'#')
telnet_connection.write(b'write memory\n')
telnet_connection.read_until(b'#')
print("35")
# Close the Telnet Connection
telnet_connection.write(b'quit\n')
print("38")
