with open('version_number.txt') as vf:
    version = vf.read().strip()

with open('installer_template.iss') as src, open('installer_v{}.iss'.format(version), 'w') as dst:
    content = src.read().replace('{VERSION}', version)
    dst.write(content)

print('Installer script generated with version {}'.format(version))