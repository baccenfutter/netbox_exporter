from setuptools import setup

setup(
    install_requires=[
        'click',
        'netbox-client',
        'requests',
        'pyyaml',
    ],
    extras_require={
        'dev': [
            'build',
            'ipython',
            'prompt-toolkit',
            'pylint',
            'twine',
        ]
    },
)

