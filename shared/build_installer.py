# This script contains a number of small functions that prepare repo files for building.
import os, markdown2, html2text, glob

def get_version(loc:str):
    '''Get version number from text file'''
    with open(os.path.join(os.path.dirname(__file__), '..', loc, 'version_number.txt')) as vf:
        return vf.read().strip()

def remove_copies(loc:str):
    '''Remove non-template installer and version files.'''
    for filename in glob.iglob(os.path.join(os.path.dirname(__file__), '..', loc, 'installer_v*')):
        os.remove(filename)
    for filename in glob.iglob(os.path.join(os.path.dirname(__file__), '..', loc, 'version_v*')):
        os.remove(filename)
    print('Old copies of installer and version templates deleted')

def update_installer(loc:str, version:str):
    '''Find and replace in installer template to insert version number'''
    with (open(os.path.join(os.path.dirname(__file__), '..', loc, 'installer_template.iss')) as src,
          open(os.path.join(os.path.dirname(__file__), '..', loc, 'installer_v{}.iss'.format(version)), 'w') as dst):
        content = src.read().replace('{VERSION}', version)
        dst.write(content)

    print('Installer script generated with version {}'.format(version))

def update_verfile(loc:str, version:str):
    '''Find and replace in version template to insert version number'''
    # Convert version number to ffi-friendly format
    vers_list = version.split('.')

    if len(vers_list) < 4:
        for i in range(4-len(vers_list)):
            vers_list.append('0')
            
    vers_ffi = ', '.join(vers_list)

    # Find and replace in version template to insert version number
    with (open(os.path.join(os.path.dirname(__file__), '..', loc, 'version_template.txt')) as src,
          open(os.path.join(os.path.dirname(__file__), '..', loc, 'version_v{}.txt'.format(version)), 'w') as dst):
        content = src.read().replace('{VERSION}', version).replace('{VERSION_FFI}', vers_ffi)
        dst.write(content)

    print('Version file generated with version {}'.format(version))

def update_readme(loc:str):
    '''Strip markdown formatting from readme and save as unformatted text file'''
    with open(os.path.join(os.path.dirname(__file__), '..', loc, 'README.md'), encoding='utf-8') as md:
        content = md.read()

    html = markdown2.markdown(content)
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_emphasis = True
    text_maker.body_width = 0
    text = text_maker.handle(html).replace('# ', '').replace('#', '')

    with open(os.path.join(os.path.dirname(__file__), '..', loc, 'README.txt'), 'w', encoding='utf-8') as f:
        f.write(text)

    print('README.txt updated based on current contents of README.md')


if __name__ == '__main__':
    loc = input('Folder with files to be updated (hivdr or vhf): ')
    version = get_version(loc)
    remove_copies(loc)
    update_installer(loc, version)
    update_verfile(loc, version)
    update_readme(loc)