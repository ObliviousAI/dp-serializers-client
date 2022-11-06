import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

setup(
    name="dp serial",
    version="0.1.0",
    description="A serializer/deserializer of popular differential privacy frameworks for remote exectution.",
    url="https://github.com/ObliviousAI/dp-serializer-client",
    author='Oblivious',
    author_email='hello@oblivious.ai',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ], 
    keywords='opendp smartnoise diffprivlib logger ast',
    packages=find_packages(),
    python_requires=">=3.7, <4",
    install_requires=[
        "opendp == 0.6.1",
        "scikit-learn >= 1.1.2",
        "diffprivlib == 0.6.0",
        "numpy == 1.22.3",
        "requests == 2.28.1",
        "pandas==1.5.1",
        "pyyaml"
    ],
    package_data={"dp_serial": ["py.typed"]},
)