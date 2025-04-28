# from azure.identity import DefaultAzureCredential, AzureCliCredential
# from azure.mgmt.containerservice import ContainerServiceClient

# def main():
#     # Use Azure CLI credential explicitly
#     credential = AzureCliCredential()

#     client = ContainerServiceClient(
#         credential=credential,
#         subscription_id="9734ed68-621d-47ed-babd-269110dbacb1",
#     )

#     response = client.managed_clusters.list()
#     for item in response:
#         print(item.location)

# main()

# import boto3
# client = boto3.client('ecs')
# cli = client.list_tasks(
#     cluster = 'support'
# )
# for data in cli['taskArns']:
#    print(data)

# class FakeEventTime:
#     def __get__(self, obj, objtype=None):
#         return obj._event_time

#     def __set__(self, obj, value):
#         obj._event_time = value

# from kubernetes import config, client


# config.load_kube_config()
# client.EventsV1Event.event_time = FakeEventTime()
# connect = client.EventsV1Api()
# list_node = connect.list_event_for_all_namespaces()
# print(list_node)

# import boto3
# ecs_client = boto3.client('ecs')
# describe = ecs_client.describe_task_definition(
#     taskDefinition='arn:aws:ecs:us-east-1:022085345551:task-definition/dashboard-test:1'
# )
# for data in describe['taskDefinition']['containerDefinitions']:
#     try:
#         print(data['logConfiguration']['logDriver'])
#         if data['logConfiguration']['logDriver'] == 'awslogs':
#           print(data['logConfiguration']['options']['awslogs-group'])
#           print(data['name'])
#     except:
#         print("hello")


# import boto3
# ecs_client = boto3.client('ecs')
# describe_tasks = ecs_client.describe_tasks(
#     cluster = 'support',
#     tasks = [
#         'e03af2402aa5442bbca7a3978eb54b3a'
#     ]
# )
# print(describe_tasks['tasks']['taskArn'])




# [2024-04-23 10:15:34] 192.168.1.100 "GET /page.html HTTP/1.1" 200 1234
# [2024-04-23 10:16:21] 192.168.1.101 "POST /submit.php HTTP/1.1" 404 4321
# [2024-04-23 10:17:45] 192.168.1.102 "GET /index.html HTTP/1.1" 200 5678
# [2024-04-23 10:18:02] 192.168.1.103 "GET /about.html HTTP/1.1" 200 7890
# [2024-04-23 10:19:15] 192.168.1.104 "POST /contact.php HTTP/1.1" 403 9876
# [2024-04-23 10:20:30] 192.168.1.105 "GET /faq.html HTTP/1.1" 200 6543
# [2024-04-23 10:21:34] 192.168.1.106 "GET /page.html HTTP/1.1" 502 12



with open('data.txt', 'r') as file:
    for data in file:
        splitting_ip = data.split(']')
        print(splitting_ip[1])