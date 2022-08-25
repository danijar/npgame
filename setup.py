import setuptools
import pathlib

setuptools.setup(
    name='npgame',
    version='0.2.0',
    author='Danijar Hafner',
    author_email='mail@danijar.com',
    description='Write simple games in Numpy!',
    url='http://github.com/danijar/npgame',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['pygame', 'numpy', 'pillow'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
