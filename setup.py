from setuptools import setup, find_packages
import os

version = '0.1.dev0'

setup(name='uvc.restvalidation',
      version=version,
      description="",
      long_description=(open("README.txt").read() + "\n" +
                        open(os.path.join("docs", "HISTORY.txt")).read()),
      classifiers=[
          "Programming Language :: Python",
      ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['uvc'],
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zope.schema',
          'zope.interface'
      ],
      extras_require={
      },
      entry_points={
         'z3c.autoinclude.plugin': 'target=uvcsite', 
      }
      )
