import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))




setup(name="django-fhir",
      version="0.0.0.6",
      license='GPL2', 
      packages=['fhir', 'fhir.views', 'fhir.tests',],
      description="A FHIR Server as a reusable Django application",
      long_description=README,
      author="Alan Viars (contributions - Mark Scrimshire)",
      author_email="sales@videntity.com",
      url="https://github.com/videntity/django-fhir",
      download_url="https://gitbub.com/videntity/django-fhir/tarball/master",
      install_requires=[
        'django>1.8', 'django-oauth-toolkit',
        'django-cors-headers', 'jsonschema'],
      include_package_data=True,
      scripts=[],
      classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],




      )


