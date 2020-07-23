from setuptools import setup

setup(name='thalesians.tsa',
      version='0.6',    # This version should match that in thalesians/tsa/__init__.py
      description='The Thalesians\' Time Series Analysis (TSA) library',
      url='https://github.com/thalesians/tsa',
      author='Thalesians Ltd',
      author_email='info@thalesians.com',
      license='Apache-2.0',
      packages=[
            'thalesians',
            'thalesians.tsa',
            'thalesians.tsa.datasets',
            'thalesians.tsa.filtering',
            'thalesians.tsa.neural',
            'thalesians.tsa.optimization',
            'thalesians.tsa.q'],
      zip_safe=False)
