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

        vpc = ec2.Vpc(self, "VPC",
                      nat_gateways=1,
                      subnet_configuration=[
                          ec2.SubnetConfiguration(
                              cidr_mask=24,
                              name="subnet-public",
                              subnet_type=ec2.SubnetType.PUBLIC,
                          ),
                          ec2.SubnetConfiguration(
                              cidr_mask=24,
                              name="subnet-private",
                              subnet_type=ec2.SubnetType.PRIVATE,
                          ),
                          ec2.SubnetConfiguration(
                              cidr_mask=28,
                              name="subnet-isolated",
                              subnet_type=ec2.SubnetType.ISOLATED,
                          ),
                      ]
                      )
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

        # Lambda

        # Role
        lambda_vpc_role = iam.Role(self, "lambda_vpc_role",
                                   assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
                                   managed_policies=
                                   [iam.ManagedPolicy.from_aws_managed_policy_name
                                    ("service-role/AWSLambdaVPCAccessExecutionRole"),
                                    iam.ManagedPolicy.from_aws_managed_policy_name
                                    ("service-role/AWSLambdaBasicExecutionRole")],
                                   )
        # Dependency Layer
        lambda_layer = lambda_.LayerVersion(self, "lambda_layer",
                                            code=lambda_.Code.from_asset("./lambda/layers/layer.zip"),
                                            compatible_runtimes=[lambda_.Runtime.PYTHON_3_8],
                                            description="Layer for Lambda dependencies",
                                            removal_policy=core.RemovalPolicy.DESTROY
                                            )
        # Function
        update_db = lambda_.Function(self, "update_db_function",
                                     vpc=vpc,
                                     vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
                                     runtime=lambda_.Runtime.PYTHON_3_8,
                                     handler='update_db.handler',
                                     code=lambda_.Code.from_asset("./lambda/update_db"),
                                     layers=[lambda_layer],
                                     role=lambda_vpc_role
                                     )
        db.grant_connect(update_db)
        db.connections.allow_from(update_db, ec2.Port.all_traffic())
        db.connections.allow_to(update_db, ec2.Port.all_traffic())
        # Env setter TODO Standalone method
        update_db.add_environment("db_endpoint_address", db.db_instance_endpoint_address)
        update_db.add_environment("db_endpoint_port", db.db_instance_endpoint_port)

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
        rule.add_target(targets.LambdaFunction(update_db))

        # API - Placeholder
        api = apigateway.RestApi(self, "bc_data_backend_api", endpoint_types=[apigateway.EndpointType.REGIONAL])
        # Add lambda integration
        get_data_entity = api.root.add_resource('get_data')
        dummy_integration = apigateway.LambdaIntegration(update_db, proxy=False,
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
