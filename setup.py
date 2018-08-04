# -*- coding: utf-8 -*-
import setuptools


def read(path):
    """Read a file."""
    with open(path) as f:
        return f.read()


version = '1.9.dev0'
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
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Zope :: 3',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: German',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
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
        'icemac.addressbook >= 7.0.dev0',
        'setuptools',
        'zope.securitypolicy >= 4.1',
    ],
    extras_require=dict(
        test=[
            'icemac.ab.calendar [test]',
        ]),
)
