from distutils.core import setup

setup(
	  name='HTTPSpy',
      version='1.0',
	  description='A very basic http sniffer',
	  long_description=open('README').read(),
	  author='Dardo Marasca, Alejandra Rodriguez, Tomas Scalli, Carlos Di Pietro',
	  author_email='sniffer.httpspy@gmail.com',
	  url='https://github.com/cdipietro/2012_1c_seginfo.git',
	  license='GPL',
	  scripts=['httpspy.py'],
	  packages=['core', 'plugins']
	)

