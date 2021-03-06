from setuptools import find_packages, setup

_version = '0.0.1'

setup(
    name='document-reporter',
    version=_version,
    description='a python module to create reports from text-based files (e.g., markdown, xml)',
    packages=find_packages(),
    author='Chia Jason',
    author_email='chia_jason96@live.com',
    url='https://github.com/toranova/document-reporter/',
    download_url='https://github.com/ToraNova/document-reporter/archive/refs/tags/v%s.tar.gz' % _version,
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    keywords = ['docx', 'md', 'xml'],
    install_requires=[
        'python-docx',
        'mistletoe',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
)
