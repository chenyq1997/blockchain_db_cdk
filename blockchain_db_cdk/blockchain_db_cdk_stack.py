from aws_cdk import core as cdk
import aws_cdk.aws_rds as rds
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_apigateway as apigateway
import aws_cdk.aws_ec2 as ec2

from pathlib import Path

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class BlockchainDbCdkStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # RDS - Placeholder

        vpc = ec2.Vpc(self, "VPC")
        cluster = rds.DatabaseCluster(self, "Database",
                                      engine = rds.DatabaseClusterEngine.aurora_postgres(),
                                      instance_props = {
                                          "vpc_subnets": {
                                              "subnet_type": ec2.SubnetType.PRIVATE
                                          },
                                          "vpc": vpc
                                      }
                              )

        ## RDS Instance Launching - TODO

        # Lambda - Placeholder

        dummy_func = lambda_.Function(self, "Dummy",
                                      runtime = lambda_.Runtime.PYTHON_3_8,
                                      handler = dummy_func.handler,
                                      code = lambda_.Code.from_asset(Path.joinpath(__dirname, "lambda_handler"))
                                      )

        # API - Placeholder

        api = apigateway.RestApi(self, "bc_data_backend_api")
        api.root.add_method("ANY")
