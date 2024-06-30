import boto3
import os
import uuid

resource_explorer_client = boto3.client('resource-explorer-2')
ec2_client = boto3.client('ec2')
rds_client = boto3.client('rds')
client_token = uuid.uuid1()


def get_view():
    return os.environ['RESOURCE_EXPLORER_VIEW_ARN']


def get_ec2_instances_in_view(view_arn):
    result = resource_explorer_client.search(
        QueryString='resourcetype:ec2:instance tag:cdpm=true',
        ViewArn=view_arn
        )

    instances = []

    for instance in result['Resources']:
        instances.append(instance['Arn'].split('/')[-1])
    print(f"found the following ec2 instances ${instances}")
    return instances


def stop_ec2_instances(ec2_instances):
    res = ec2_client.stop_instances(InstanceIds=ec2_instances, Force=True)
    print(res)


def get_rds_instances_in_view(view_arn):
    result = resource_explorer_client.search(
        QueryString='resourcetype:rds:db tag:cdpm=true',
        ViewArn=view_arn
        )

    instances = []

    for instance in result['Resources']:
        instances.append(instance['Arn'].split(':')[-1])
    print(f"found the following rds instances ${instances}")
    return instances


def stop_rds_instances(rds_instances):
    res = []
    for instance in rds_instances:
        try:
            res.append(
                rds_client.stop_db_instance(
                    DBInstanceIdentifier=instance
                )
            )
        except Exception:
            res.append(f"${instance} could not be stopped")

    print(res)


if __name__ == '__main__':
    view_arn = get_view()
    ec2_instances = get_ec2_instances_in_view(view_arn)
    rds_instances = get_rds_instances_in_view(view_arn)
    stop_ec2_instances(ec2_instances)
    stop_rds_instances(rds_instances)
