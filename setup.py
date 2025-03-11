from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    This function reads the requirements.txt file and returns a list of all the packages.
    """
    requirements_lst:List[str]=[]
    try:
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirements_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt File not found")
    return requirements_lst

setup(
    name='sample_project',
    version='0.0.1',
    author='Hitesh',
    packages=find_packages(),
    install_requires=get_requirements(),
)