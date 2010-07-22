from setuptools import setup, find_packages
 
setup(name='django-oembed-field',
    version='0.1',
    description='A django model field which validates an oEmbed URL',
    long_description=open('README').read(),
    author='Simon Meers'
    author_email='simon@simonmeers.com',
    url='http://github.com/ozan/django-oembed-field',
    packages=find_packages(),
    classifiers=[
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
    ]
)
