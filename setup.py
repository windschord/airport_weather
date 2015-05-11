from setuptools import setup, find_packages

setup(name='airport weather',
      version='0.1',
      description='airport weather',
      long_description=__doc__,
      author='windschord.com',
      author_email='support@windschord.com',
      url='http://www.windschord.com',
      packages = find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['flask', 'Flask-Babel','SQLAlchemy'],
      keywords='weather',
      classifiers=[''],
     )