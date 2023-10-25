from netmiko import ConnectHandler

# Define the device parameters
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': input('Enter a username: '),
    'password': input('Enter a password: '),
    'secret': input('Enter enable password: '),
}

# Connect to the device
net_connect = ConnectHandler(**device)
net_connect.enable()

# Define the new hostname
new_hostname = input('Enter the new hostname: ')

# Send configuration commands to change the hostname
config_commands = [f'hostname {new_hostname}']
output = net_connect.send_config_set(config_commands)

# Send command to output the running configuration
running_config = net_connect.send_command('show running-config')

# Save the running configuration to a local file
with open(f'{new_hostname}_running_config.txt', 'w') as file:
    file.write(running_config)

# Display success message
print('-------------------------------------')
print('')
print('--- Success! connecting to :', device['ip'])
print('---                  Username:', device['username'])
print('---                  Password:', device['password'])
print(f'---           New Hostname: {new_hostname}')
print('--- Running configuration saved to', f'{new_hostname}_running_config.txt')
print('')
print('-------------------------------------')

# Disconnect from the device
net_connect.disconnect()
