# Get version number from text file
with open('version_number.txt') as vf:
    version = vf.read().strip()

# Find and replace in installer template to insert version number
with open('installer_template.iss') as src, open('installer_v{}.iss'.format(version), 'w') as dst:
    content = src.read().replace('{VERSION}', version)
    dst.write(content)

print('Installer script generated with version {}'.format(version))

# Convert version number to ffi-friendly format
vers_list = version.split('.')

if len(vers_list) < 4:
    for i in range(4-len(vers_list)):
        vers_list.append('0')
        
vers_ffi = ', '.join(vers_list)

# Find and replace in version template to insert version number
with open('version_template.txt') as src, open('version_v{}.txt'.format(version), 'w') as dst:
    content = src.read().replace('{VERSION}', version).replace('{VERSION_FFI}', vers_ffi)
    dst.write(content)

print('Version file generated with version {}'.format(version))