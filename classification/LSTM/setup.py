from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [
    'scikit-learn==0.21.3',
    'numpy==1.16.4',
    'pandas==0.24.2',
    'tensorflow-gpu==2.0.0b1',
    'nltk==3.4.1',
    'Keras==2.3.0'
]

setup(
    name='trainer',
    version='0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True
)
