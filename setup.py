import setuptools

try:
      with open("README.md", "r") as fh:
          long_description = fh.read()
except:
      long_description = ''

setuptools.setup(name='adrf',
      version='0.1.2',
      description='ADRF Python Client',
      url='https://github.com/NYU-Chicago-data-facility/adrf_py',
      author='Daniel Castellani',
      author_email='daniel.castellani@nyu.edu',
      long_description=long_description,
      packages=setuptools.find_packages(),
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
)