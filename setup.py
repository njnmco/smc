import setuptools

setuptools.setup(
    name='eonacs',
    version='1.0.0',
    url='https://github.com/njnmco/smc',
    author='Neal Fultz',
    author_email='neal@njnm.co',
    description='Description of my package',
    package_dir={"eonacs": "src"},
    packages=['eonacs', 'eonacs.common'],
    python_requires='>=3.7',
    install_requires=['transformers', 'numpy', 'pacmap'],
)
