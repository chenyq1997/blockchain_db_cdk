import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="blockchain_db_cdk",
    version="0.0.1",

    description="A Python CDK app/stack of a blockchain data backend",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="github.com/chenyq1997",

    package_dir={"": "blockchain_db_cdk"},
    packages=setuptools.find_packages(where="blockchain_db_cdk"),

    install_requires=[
        "aws-cdk.core==1.102.0",
        "aws-cdk.aws-apigateway==1.102.0",
        "aws-cdk.aws-rds==1.102.0",
        "aws-cdk.aws-ec2==1.102.0",
        "aws-cdk.aws-events==1.102.0",
        "aws-cdk.aws-event-targets==1.102.0",
        "aws-cdk.aws-iam==1.102.0",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 1 - Planning",

        "Intended Audience :: Developers",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
