# =============================================================================
# Scenario 32: Wheel Diff Attack and Malicious setup.py
# Demonstrates: Setup.py code execution, eval chains, HuggingFace model risks
# Triggers: SCA-058, SCA-053
# INTENTIONALLY VULNERABLE - DO NOT USE IN PRODUCTION
# =============================================================================
from setuptools import setup
import os

# SCA-058: Malicious setup.py with exec/eval
exec(open('version.py').read())
config = eval(open('config.json').read())
code = compile(open('helper.py').read(), 'helper.py', 'exec')

# SCA-058: __import__ in setup.py
__import__('os').system('echo setup running')

setup(
    name='example-package',
    version='1.0.0',
    packages=['example'],
    install_requires=[
        'requests>=2.28.0',
    ],
)
