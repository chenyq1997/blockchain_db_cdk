from aws_cdk import core as cdk
import aws_cdk.aws_rds as rds
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_apigateway as apigateway
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_events as events
import aws_cdk.aws_events_targets as targets
import aws_cdk.aws_iam as iam

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

pstr = "8fsB-F(('pQvK5eu"


class BlockchainDbCdkStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # RDS - Placeholder

        vpc = ec2.Vpc(self, "VPC")
        db = rds.DatabaseInstance(
            self, "RDS",
            database_name="db1",
            credentials=rds.Credentials.from_password(
                "admin", core.SecretValue(pstr)
            ),
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_5_7
            ),
            vpc=vpc,
            port=3306,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.MEMORY4,
                ec2.InstanceSize.LARGE,
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False
        )

        # Lambda - Placeholder
        lambda_vpc_role = iam.Role(self, "lambda_vpc_role",
                                   assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
                                   managed_policies=
                                   [iam.ManagedPolicy.from_aws_managed_policy_name
                                    ("service-role/AWSLambdaVPCAccessExecutionRole"),
                                    iam.ManagedPolicy.from_aws_managed_policy_name
                                    ("service-role/AWSLambdaBasicExecutionRole")],
                                   )
        dummy_func = lambda_.Function(self, "dummy_lambda_function",
                                      vpc=vpc,
                                      runtime=lambda_.Runtime.PYTHON_3_8,
                                      handler='dummy_func.handler',
                                      code=lambda_.Code.from_asset("./lambda/dummy/dummy_func.zip"),
                                      role=lambda_vpc_role
                                      )
        db.grant_connect(dummy_func)
        # Env setter TODO Standalone method
        dummy_func.add_environment("db_endpoint_address", db.db_instance_endpoint_address)
        dummy_func.add_environment("db_endpoint_port", db.db_instance_endpoint_port)

        # Run every hour at 0 minute mark
        # See https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='0',
                hour='*',
                month='*',
                week_day='*',
                year='*'),
        )
        rule.add_target(targets.LambdaFunction(dummy_func))

        # API - Placeholder
        api = apigateway.RestApi(self, "bc_data_backend_api", endpoint_types=[apigateway.EndpointType.REGIONAL])
        # Add lambda integration
        get_data_entity = api.root.add_resource('get_data')
        dummy_integration = apigateway.LambdaIntegration(dummy_func, proxy=False,
                                                         integration_responses=[
                                                             {
                                                                 'statusCode': '200',
                                                                 'responseParameters': {
                                                                     'method.response.header.Access-Control-Allow-Origin': "'*'",
                                                                 }
                                                             }
                                                         ])
        get_data_entity.add_method('GET', dummy_integration,
                                   method_responses=[{
                                       'statusCode': '200',
                                       'responseParameters': {
                                           'method.response.header.Access-Control-Allow-Origin': True,
                                       }
                                   }]
                                   )
        add_cors_options(self, get_data_entity)


# CORS Options helper
def add_cors_options(self, apigw_resource):
    apigw_resource.add_method('OPTIONS', apigateway.MockIntegration(
        integration_responses=[{
            'statusCode': '200',
            'responseParameters': {
                'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                'method.response.header.Access-Control-Allow-Origin': "'*'",
                'method.response.header.Access-Control-Allow-Methods': "'GET,OPTIONS'"
            }
        }
        ],
        passthrough_behavior=apigateway.PassthroughBehavior.WHEN_NO_MATCH,
        request_templates={"application/json": "{\"statusCode\":200}"}
    ),
                              method_responses=[{
                                  'statusCode': '200',
                                  'responseParameters': {
                                      'method.response.header.Access-Control-Allow-Headers': True,
                                      'method.response.header.Access-Control-Allow-Methods': True,
                                      'method.response.header.Access-Control-Allow-Origin': True,
                                  }
                              }
                              ],
                              )

# Set Lambda environmental variables
