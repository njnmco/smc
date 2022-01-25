import setuptools

setuptools.setup(
    name='eonacs',
    version='1.0.0',
    url='https://github.com/njnmco/smc',
    author='Neal Fultz',
    author_email='neal@njnm.co',
    description='Description of my package',
    packages=find_packages(),
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires='>=3.7',
    install_requires=['numpy >= 1.11.1', 'matplotlib >= 1.5.1'],
)
