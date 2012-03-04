from paver.easy import *
from paver.setuputils import setup
from setuptools import find_packages
import os

#logging.basicConfig(level=logging.DEBUG)

try:
    # Optional tasks, only needed for development
    import paver.doctools
    import paver.virtual
    import paver.misctasks
    from paved import *
    from paved.dist import *
    from paved.util import *
    from paved.docs import *
    from paved.pycheck import *
    from paved.pkg import *
    from sphinxcontrib import paverutils
    from pyavrutils import support
#    sys.path.insert(0, path('.').abspath())
    ALL_TASKS_LOADED = True
except ImportError, e:
    info("some tasks could not not be imported.")
    debug(str(e))
    ALL_TASKS_LOADED = False

def read_project_version(py=None, where='.', exclude=['bootstrap', 'pavement', 'doc', 'docs', 'test', 'tests', ]):
    if not py:
        py = path(where) / find_packages(where=where, exclude=exclude)[0]
    py = path(py)
    if py.isdir():
        py = py / 'version.py'
    __version__ = None
    for line in py.lines():
        if '__version__' in line:
            exec line
            break
    return __version__

NAME = 'softusbduino'
URL = 'https://github.com/ponty/softusbduino'
DESCRIPTION = 'Arduino software USB interface'
VERSION = read_project_version()


classifiers = [
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    "License :: OSI Approved :: BSD License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    ]

install_requires = open("requirements.txt").read().split('\n')

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open('README.rst', 'r').read(),
    classifiers=classifiers,
    keywords='arduino usb',
    author='ponty',
    #author_email='',
    url=URL,
    license='BSD',
    packages=find_packages(exclude=['bootstrap', 'pavement', ]),
    include_package_data=True,
    test_suite='nose.collector',
    zip_safe=False,
    install_requires=install_requires,
    )

options(
    sphinx=Bunch(
        docroot='docs',
        builddir="_build",
        ),
    pdf=Bunch(
        builddir='_build',
        builder='latex',
    ),
    )




if ALL_TASKS_LOADED:
    
    options.paved.clean.patterns += ['*.pickle',
                                     '*.doctree',
                                     '*.gz' ,
                                     'nosetests.xml',
                                     'sloccount.sc',
                                     '*.pdf', '*.tex',
                                     '*.png',
                                     
                                     'generated_*', # generated files
                                     
                                     '*.axf',
                                     '*.elf',
                                     '*.o',
                                     '*.a',
                                     '*.eep',
                                     '*.hex',
                                     '*.lss',
                                     '*.map',
                                     '*.lst',
                                     '*.sym',
                                     '*.vcd',
                                      ]
    
    options.paved.dist.manifest.include.remove('distribute_setup.py')
    options.paved.dist.manifest.recursive_include.add('softusbduino *.csv')

    docroot = path(options.sphinx.docroot)
    root = path(__file__).parent.parent.abspath()
    examples = support.find_examples(root)
    
    @task
    @needs(
#           'clean',
           'codegen',
           'sloccount', 
           'build_test', 
           'boards', 
           'doxy', 
           'cog', 
           'html', 
           'pdf', 
           'sdist',
           'nose',
           )
    def alltest():
        'all tasks to check'
        pass
    
    @task
    @needs('sphinxcontrib.paverutils.html')
    def html():
        pass

    @task
    @needs('sphinxcontrib.paverutils.pdf')
    def pdf():
        fpdf = list(path('docs/_build/latex').walkfiles('*.pdf'))[0]
        d = path('docs/_build/html')
        d.makedirs()
        fpdf.copy(d)

    @task
    def doxy():
        path('docs/_build/html/doxy').makedirs()
        sh('doxygen doxy.ini')

    ARDUINO_VERSIONS=[
                      '0022', 
                      '0023', 
                      '1.0',
                      ]
    
    @task
    def build_test():
        for ver in ARDUINO_VERSIONS:
            os.environ['ARDUINO_HOME'] = path('~/opt/arduino-{0}'.format(ver)).expanduser()
            csv = docroot / 'generated_build_test_{0}.csv'.format(ver)
            support.build2csv(
                              examples, 
                              csv, 
                              logdir=docroot / '_build' / 'html', 
                              logger=info, 
                              )

    @task
    def boards():
        for ver in ARDUINO_VERSIONS:
            support.set_arduino_path('~/opt/arduino-{0}'.format(ver))
            csv = docroot / 'generated_boards_{0}.csv'.format(ver)
            support.boards2csv(csv, logger=info)
    
    @task
    def codegen():
        sh('python softusbduino/codegen.py')
    
