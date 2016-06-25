# -*- coding: utf-8 -*-
import os.path
import setuptools


def read(*path_elements):
    """Read file."""
    return file(os.path.join(*path_elements)).read()


version = '1.1'
long_description = '\n\n'.join([
    read('README.rst'),
    read('CHANGES.rst'),
])

setuptools.setup(
    name='icemac.ab.calexport',
    version=version,
    description="Calendar export feature for icemac.ab.calendar",
    long_description=long_description,
    keywords='icemac addressbook calendar export html',
    author='Michael Howitz',
    author_email='icemac@gmx.net',
    download_url='http://pypi.python.org/pypi/icemac.ab.calexport',
    url='https://bitbucket.org/icemac/icemac.ab.calexport',
    license='ZPL 2.1',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Paste',
        'Framework :: Zope3',
        'License :: OSI Approved',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Natural Language :: German',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['icemac', 'icemac.ab'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'grokcore.component >= 2.5.1.dev1',
        'icemac.ab.calendar >= 1.8.dev0',
        'icemac.addressbook >= 2.7.dev0',
        'setuptools',
    ],
    extras_require=dict(
        test=[
            'icemac.ab.calendar [test]',
        ]),
)
