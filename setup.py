# -*- coding: utf-8 -*-
import setuptools


def read(path):
    """Read a file."""
    with open(path) as f:
        return f.read()


version = '1.7'
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
    download_url='https://pypi.org/project/icemac.ab.calexport',
    url='https://bitbucket.org/icemac/icemac.ab.calexport',
    license='ZPL 2.1',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
        'icemac.ab.calendar >= 3.0.dev0',
        'icemac.addressbook >= 5.0.dev0',
        'setuptools',
        'zope.securitypolicy >= 4.1',
    ],
    extras_require=dict(
        test=[
            'icemac.ab.calendar [test]',
        ]),
)
