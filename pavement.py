from paver.easy import *
from paver.setuputils import setup
from setuptools import find_packages
import os

# logging.basicConfig(level=logging.DEBUG)
import paver.doctools
import paver.virtual
import paver.misctasks
from paved import *
from paved.dist import *
from paved.util import *
from paved.docs import *
from paved.pycheck import *
from paved.pkg import *
from pyavrutils import support

# get info from setup.py
setup_py = ''.join(
    [x for x in path('setup.py').lines() if 'setuptools' not in x])
exec(setup_py)


options(
    sphinx=Bunch(
        docroot='docs',
        builddir="_build",
    ),
#    pdf=Bunch(
#        builddir='_build',
#        builder='latex',
#    ),
)


options.paved.clean.rmdirs += ['.tox',
                               'dist',
                               'build',
                               ]
options.paved.clean.patterns += ['*.pickle',
                                 '*.doctree',
                                 '*.gz',
                                 'nosetests.xml',
                                 'sloccount.sc',
                                 '*.pdf', '*.tex',
                                 '*.png',

                                 'generated_*',  # generated files

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
                                 '*.zip',
                                 'distribute_setup.py',
                                 ]

options.paved.dist.manifest.include.remove('distribute_setup.py')
options.paved.dist.manifest.include.remove('paver-minilib.zip')
options.paved.dist.manifest.include.add('requirements.txt')
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
#     'boards',
    'doxy',
    'cog',
    'html',
    #'pdf',
    'sdist',
    'nose', 'tox',
)
def alltest():
    'all tasks to check'
    pass


@task
def doxy():
    path('docs/_build/html/doxy').makedirs_p()
    sh('doxygen doxy.ini')

ARDUINO_VERSIONS = [
#     '0022',
#     '0023',
    '1.0.3',
]


@task
def build_test():
    for ver in ARDUINO_VERSIONS:
        os.environ['ARDUINO_HOME'] = path(
            '~/opt/arduino-{0}'.format(ver)).expanduser()
        csv = docroot / 'generated_build_test_{0}.csv'.format(ver)
        support.build2csv(
            examples,
            csv,
            logdir=docroot / '_build' / 'html',
            logger=info,
        )


# @task
# def boards():
#     for ver in ARDUINO_VERSIONS:
#         support.set_arduino_path('~/opt/arduino-{0}'.format(ver))
#         csv = docroot / 'generated_boards_{0}.csv'.format(ver)
#         support.boards2csv(csv, logger=info)


@task
def codegen():
#    from softusbduino import codegen
#    codegen.main()
    sh('python softusbduino/codegen/__init__.py')


@task
@needs('manifest', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our MANIFEST.in is generated.
    """
    pass


@task
@needs('codegen')
def build():
    """
    """
    pass
