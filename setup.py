from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='qyxycjh.policy',
      version=version,
      description="a site policy for qyxycjh web site",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='python plone',
      author='Adam tang',
      author_email='yuejun.tang@gmail.com',
      url='https://github.com/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['qyxycjh'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.membrane',
          'plone.directives.dexterity',
          'plone.app.dexterity',
          'plone.namedfile',
          'plone.formwidget.namedfile',
          'collective.autopermission',
          'collective.dexteritytextindexer',                    
          'Products.CMFPlone',      
          'five.grok',
          'z3c.jbot',
          'z3c.caching',
                                                                     
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': ['plone.app.testing',]
      },         
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
#      setup_requires=["PasteScript"],
#      paster_plugins=["ZopeSkel"],
      )
