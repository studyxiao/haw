from setuptools import setup, find_packages

setup(name='Haw',
      version='0.1.0',
      license='MIT',
      description='Flask resetful api core with user module',
      long_description_content_type="text/markdown",
      author='studyxiao',
      author_email='studyxiao@163.com',
      url='https://studyxiao.cn',
      keywords=['Flask', 'CMS', 'api', 'user'],
      packages=find_packages(),
      zip_safe=False,
      platforms='any',
      include_package_data=True,
      install_requires=[
          'celery==4.4.5', 'Flask==1.1.2', 'Flask-migrate==2.5.3',
          'Flask-Cors==3.0.8', 'Flask-JWT-Extended==3.24.1',
          'Flask-Mail==0.9.1', 'Flask-SQLAlchemy==2.4.3', 'Flask-WTF==0.14.3',
          'Pillow==7.1.2', 'PyMySQL==0.9.3', 'python-dotenv==0.13.0',
          'redis==3.5.3'
      ])
