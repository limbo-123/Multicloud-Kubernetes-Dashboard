from kubernetes import client, config
from django.shortcuts import render, redirect
from django.contrib import messages
import boto3
import subprocess
from azure.identity import DefaultAzureCredential, AzureCliCredential
from azure.mgmt.containerservice import ContainerServiceClient
from django.urls import reverse
from datetime import datetime
import yaml
import time
import json


class FakeEventTime:
    def __get__(self, obj, objtype=None):
        return obj._event_time

    def __set__(self, obj, value):
        obj._event_time = value

def home(request):
     start_time = time.time()
     #Importing Clusters from all AWS regions
     all_clusters = []
        #####Azure Cluster###########
     credential = AzureCliCredential()
     clienting = ContainerServiceClient(
     credential=credential,
     subscription_id="2639848210932904",
        )
     response = clienting.managed_clusters.list()
     cloud = "azure"
     for item in response:
            all_clusters.append({'cluster_region': item.location, 'cluster_name': item.name, 'cluster_region_svc': cloud })
     #Loading Essential Configs
     client.EventsV1Event.event_time = FakeEventTime()
     config.load_kube_config()
     connection = client.CoreV1Api() 
     deploy = client.AppsV1Api()
     network = client.NetworkingV1Api()
     batch = client.BatchV1Api()
     asg = client.AutoscalingV1Api()
     #Fetching Common Resources
     pod_data = connection.list_pod_for_all_namespaces()
     my_deploy = deploy.list_deployment_for_all_namespaces()
     my_ds = deploy.list_daemon_set_for_all_namespaces()
     my_sts = deploy.list_stateful_set_for_all_namespaces()
     my_nodes = connection.list_node()
     my_secret = connection.list_secret_for_all_namespaces()
     my_configmap = connection.list_config_map_for_all_namespaces()
     my_pvc = connection.list_persistent_volume_claim_for_all_namespaces()
     my_pv = connection.list_persistent_volume()
     total_ns = connection.list_namespace()
     total_ingress = network.list_ingress_for_all_namespaces()
     total_svc = connection.list_service_for_all_namespaces()
     total_cjob = batch.list_cron_job_for_all_namespaces()
     total_job = batch.list_cron_job_for_all_namespaces()
     total_asg = asg.list_horizontal_pod_autoscaler_for_all_namespaces()
     total_rs = deploy.list_replica_set_for_all_namespaces()
     total_nodes = connection.list_node()
     
     load_events = client.EventsV1Api()
     events_ns_all = load_events.list_event_for_all_namespaces() 
     
        #####AWS Cluster Details######
     aws_regions = [
        "us-east-1", "us-west-2",
        "eu-central-1"
     ]
     for my_region in aws_regions:
         eks_client = boto3.client('eks', region_name=my_region)
         ecs_client = boto3.client('ecs', region_name=my_region)
         eks_cluster_list = eks_client.list_clusters()
         ecs_cluster_list =ecs_client.list_clusters()

         for my_eks_cluster in eks_cluster_list['clusters']:
        # Describe the current EKS cluster
          describe_cluster = eks_client.describe_cluster(name=my_eks_cluster)
        
        # Extract details from the EKS cluster
          eks_cluster_name = describe_cluster['cluster']['arn'].split('/')[1]
          eks_cluster_svc = describe_cluster['cluster']['arn'].split(':')[2]
          eks_cluster_region = describe_cluster['cluster']['arn'].split(':')[3]

        # Append the cluster details to all_clusters
          all_clusters.append({
            'cluster_name': eks_cluster_name,
            'cluster_region': eks_cluster_region,
            'cluster_region_svc': eks_cluster_svc
          })

     # eks_cluster_name = describe_cluster['cluster']['arn'].split('/')[1]
     # eks_cluster_svc = describe_cluster['cluster']['arn'].split(':')[2]
     # eks_cluster_region= describe_cluster['cluster']['arn'].split(':')[3]
          for ecs_cluster_details in ecs_cluster_list['clusterArns']:
            ecs_cluster_name = ecs_cluster_details.split('/')[1]
            ecs_cluster_svc = ecs_cluster_details.split(':')[2]
            ecs_cluster_region = ecs_cluster_details.split(':')[3]
            all_clusters.append({'cluster_name':ecs_cluster_name, 'cluster_region': ecs_cluster_region, 'cluster_region_svc': ecs_cluster_svc})
     try:
     #Fetching Cluster Details from config for detail.
        cluster_info = config.list_kube_config_contexts()
        filter_region_name = cluster_info[1]['name'].split(':')[3]
     # filter_region_name = cluster_info[1]['cluster']
        filtered_cluster_name = cluster_info[1]['name'].split('/')[1]
        filtered_service_name = cluster_info[1]['name'].split(':')[2]
        print("Machine Learning Detected AWS")  
        context = {'pods': pod_data, 
                   'moka': my_deploy, 
                   'my_ds': my_ds, 
                   'my_sts': my_sts, 
                   'config': filtered_cluster_name, 
                   'region': filter_region_name, 
                   'mata': events_ns_all,
                   'list': all_clusters,
                   'my_nodes': my_nodes,
                   'my_secret': my_secret,
                   'my_configmap': my_configmap,
                   'my_pvc': my_pvc,
                   'my_pv': my_pv,
                   'total_ns' : total_ns,
                   'total_ingress': total_ingress,
                   'total_svc': total_svc,
                   'total_cjob': total_cjob,
                   'tatal_job': total_job,
                   'asg': total_asg,
                   'service': filtered_service_name,
                   'total_rs': total_rs,
                   'total_nodes': total_nodes}
        return render(request, 'index.html', context)
     except:
        azure_cluster_details = item.name
        azure_location = item.location
        print("Machine Learning Detected Azure")   
        context = {'pods': pod_data, 
                   'moka': my_deploy, 
                   'my_ds': my_ds, 
                   'my_sts': my_sts, 
                   'mata': events_ns_all,
                   'list': all_clusters,
                   'my_nodes': my_nodes,
                   'my_secret': my_secret,
                   'my_configmap': my_configmap,
                   'my_pvc': my_pvc,
                   'my_pv': my_pv,
                   'total_ns' : total_ns,
                   'total_ingress': total_ingress,
                   'total_svc': total_svc,
                   'total_cjob': total_cjob,
                   'tatal_job': total_job,
                   'asg': total_asg,
                   'az_cluster': azure_cluster_details,
                   'az_region': azure_location,
                   'total_rs': total_rs,
                   'total_nodes': total_nodes}

        return render(request, 'index.html', context)

# import time
# from concurrent.futures import ThreadPoolExecutor
# from django.shortcuts import render
# from django.core.cache import cache
# from azure.identity import AzureCliCredential
# from azure.mgmt.containerservice import ContainerServiceClient
# from kubernetes import client, config
# import boto3

# def get_aws_clusters(region):
#     clusters = []
#     try:
#         eks_client = boto3.client('eks', region_name=region)
#         ecs_client = boto3.client('ecs', region_name=region)

#         eks_clusters = eks_client.list_clusters().get('clusters', [])
#         for cluster_name in eks_clusters:
#             cluster_info = eks_client.describe_cluster(name=cluster_name)['cluster']
#             clusters.append({
#                 'cluster_name': cluster_info['arn'].split('/')[1],
#                 'cluster_region': cluster_info['arn'].split(':')[3],
#                 'cluster_region_svc': cluster_info['arn'].split(':')[2]
#             })

#         ecs_clusters = ecs_client.list_clusters().get('clusterArns', [])
#         for arn in ecs_clusters:
#             clusters.append({
#                 'cluster_name': arn.split('/')[1],
#                 'cluster_region': arn.split(':')[3],
#                 'cluster_region_svc': arn.split(':')[2]
#             })
#     except Exception as e:
#         print(f"Error fetching AWS data for region {region}: {e}")
#     return clusters

# def home(request):
#     start_time = time.time()
#     all_clusters = []

#     # ---------------- Azure Clusters ----------------
#     try:
#         credential = AzureCliCredential()
#         clienting = ContainerServiceClient(
#             credential=credential,
#             subscription_id="28e1e42a-4438-4c30-9a5f-7d7b488fd883"
#         )
#         response = clienting.managed_clusters.list()
#         for item in response:
#             all_clusters.append({
#                 'cluster_region': item.location,
#                 'cluster_name': item.name,
#                 'cluster_region_svc': 'azure'
#             })
#     except Exception as e:
#         print("Azure cluster fetch failed:", e)

#     # ---------------- AWS Clusters (Cached + Parallel) ----------------
#     cached_clusters = cache.get('aws_clusters')
#     if cached_clusters:
#         all_clusters.extend(cached_clusters)
#     else:
#         aws_regions = ["us-east-1", "us-west-1", "us-west-2", "eu-west-1", "eu-central-1", "ap-southeast-1"]
#         with ThreadPoolExecutor(max_workers=6) as executor:
#             results = executor.map(get_aws_clusters, aws_regions)
#             aws_clusters = [item for sublist in results for item in sublist]
#         all_clusters.extend(aws_clusters)
#         cache.set('aws_clusters', aws_clusters, timeout=300)

#     # ---------------- Kubernetes API Setup ----------------
#     try:
#         config.load_kube_config()
#         v1 = client.CoreV1Api()
#         deploy = client.AppsV1Api()
#         network = client.NetworkingV1Api()
#         batch = client.BatchV1Api()
#         asg = client.AutoscalingV1Api()
#         events_api = client.EventsV1Api()

#         # Safely load current context
#         kube_contexts, current_context = config.list_kube_config_contexts()
#         if not current_context or 'name' not in current_context:
#             raise Exception("No current kubeconfig context found.")

#         context_name = current_context['name']
#         context_parts = context_name.split(':')

#         filter_region_name = context_parts[3] if len(context_parts) > 3 else 'unknown'
#         filtered_service_name = context_parts[2] if len(context_parts) > 2 else 'unknown'
#         last_part = context_parts[-1]
#         filtered_cluster_name = last_part.split('/')[-1] if '/' in last_part else last_part

#         # ---------------- Fetch Kubernetes Resources ----------------
#         context = {
#             'pods': v1.list_pod_for_all_namespaces(limit=100),
#             'moka': deploy.list_deployment_for_all_namespaces(),
#             'my_ds': deploy.list_daemon_set_for_all_namespaces(),
#             'my_sts': deploy.list_stateful_set_for_all_namespaces(),
#             'config': filtered_cluster_name,
#             'region': filter_region_name,
#             'service': filtered_service_name,
#             'mata': events_api.list_event_for_all_namespaces(limit=100),
#             'list': all_clusters,
#             'my_nodes': v1.list_node(),
#             'my_secret': v1.list_secret_for_all_namespaces(limit=100),
#             'my_configmap': v1.list_config_map_for_all_namespaces(limit=100),
#             'my_pvc': v1.list_persistent_volume_claim_for_all_namespaces(),
#             'my_pv': v1.list_persistent_volume(),
#             'total_ns': v1.list_namespace(),
#             'total_ingress': network.list_ingress_for_all_namespaces(),
#             'total_svc': v1.list_service_for_all_namespaces(),
#             'total_cjob': batch.list_cron_job_for_all_namespaces(),
#             'tatal_job': batch.list_job_for_all_namespaces(),
#             'asg': asg.list_horizontal_pod_autoscaler_for_all_namespaces(),
#             'total_rs': deploy.list_replica_set_for_all_namespaces(),
#             'total_nodes': v1.list_node()
#         }

#     except Exception as e:
#         print("Kube API or context load failed:", e)
#         context = {
#             'list': all_clusters,
#             'error': 'Could not fetch Kubernetes cluster info'
#         }

#     print(f"Home view loaded in {time.time() - start_time:.2f}s")
#     return render(request, 'index.html', context)



def update_cluster(request):
    # Switching cluster post UI selection
     if request.method == 'POST':
          selected_cluster = request.POST.get('cluster')  # Get the full selected value

          if selected_cluster:
            # Split the selected cluster into its components
               cluster_name, cluster_region, cluster_svc = selected_cluster.split('|')
               if cluster_svc == 'eks':
            
               # Run the command to update kubeconfig
                    command = [
                    "aws", "eks", "update-kubeconfig",
                    "--name", cluster_name, '--region', cluster_region
                    ]
                    subprocess.run(command, check=True)
                    print("Cluster has been changed")
                    return redirect(home) 
               elif cluster_svc == 'azure':
                    command = [
                         "az", "aks", "get-credentials", "--resource-group", "1-b56a4dd3-playground-sandbox", "--name", "prod-aks", "--overwrite-existing"
                     ]
                    subprocess.run(command, check=True)
                    print("Cluster has been changed")
                    return redirect(home)
               elif cluster_svc == 'ecs':
               #      all_cluster_specific_service = []
               #      all_cluster_specific_tasks = []
               #      ecs_client = boto3.client('ecs', region_name = cluster_region)
               #      describe_ecs_cluster = ecs_client.describe_clusters(
               #           clusters = [
               #                cluster_name
               #           ],
               #           include=[
               #             'ATTACHMENTS',
               #             'CONFIGURATIONS',
               #             'SETTINGS',
               #             'STATISTICS',
               #             'TAGS',
               #           ])
               #      ecs_service = ecs_client.list_services(
               #           cluster = cluster_name
               #      )
               #      ecs_tasks = ecs_client.list_tasks(
               #           cluster = cluster_name
               #      )
               #      for task in ecs_tasks['taskArns']:
               #           all_cluster_specific_tasks.append(task)
               #      for service in ecs_service['serviceArns']:
               #           all_cluster_specific_service.append(service)
               #      for clusterarn in describe_ecs_cluster['clusters']:
               #           clusterarn
               #      context = {
               #           'clusterArn' : clusterarn,
               #           'region': cluster_region,
               #           'service': all_cluster_specific_service, 
               #           'task': all_cluster_specific_tasks
               #      }
#                    return render(request, 'ecs_details.html', context)
                     return redirect(reverse('view_ecs_cluster', args=[cluster_name, cluster_region]))
     return render(request, 'ecs_details.html')

def view_ecs_cluster(request, cluster_name, cluster_region):
    ecs_client = boto3.client('ecs', region_name=cluster_region)

    # Describe ECS cluster
    describe_ecs_cluster = ecs_client.describe_clusters(
        clusters=[cluster_name],
        include=[
            'ATTACHMENTS',
            'CONFIGURATIONS',
            'SETTINGS',
            'STATISTICS',
            'TAGS',
        ]
    )

    ecs_service = ecs_client.list_services(cluster=cluster_name)
    ecs_tasks = ecs_client.list_tasks(cluster=cluster_name)

    all_cluster_specific_service = ecs_service['serviceArns']
    filtered_svc_name = [service.split('/')[2] for service in all_cluster_specific_service]
    all_cluster_specific_tasks = ecs_tasks['taskArns']

    clusterarn = describe_ecs_cluster['clusters'][0] if describe_ecs_cluster['clusters'] else None
    list_container_instance = ecs_client.list_container_instances(
         cluster=cluster_name
    )
    
    # Fetch and describe each container instance
    all_described_instances = []
    for instance_list in list_container_instance['containerInstanceArns']:
        describe_instance = ecs_client.describe_container_instances(
            cluster=cluster_name,
            containerInstances=[instance_list]
        )
        
        # Append only the container instance data
        if 'containerInstances' in describe_instance:
            all_described_instances.extend(describe_instance['containerInstances'])


    # Prepare context for the template
    context = {
        'clusterArn': clusterarn,
        'region': cluster_region,
        'services': zip(all_cluster_specific_service, filtered_svc_name),  # Pass services with names
        'tasks': all_cluster_specific_tasks,
        'list_container_instance': all_described_instances # Pass all container instances
    }

    # Render the ECS details page with the context
    return render(request, 'ecs_details.html', context)

#Listing Task Defitioniton for TD Menu

def list_task_definition(request, cluster_region):
     ecs_client = boto3.client('ecs', region_name=cluster_region)
     listing_td = ecs_client.list_task_definitions(

     )
     context = {
          'listing_td': listing_td,
          'region': cluster_region
     }
     return render(request, 'ecs_details.html', context)


def ecs(request, clutser, svc, cluster_region):
     svc_name = svc
     cluster_name = clutser

     ecs_client = boto3.client('ecs', region_name=cluster_region)
     describe_ecs = ecs_client.describe_services(
              cluster = cluster_name,
              services = [svc_name]
         )
     for more_details in describe_ecs['services']:
          more_details
     list_tasks = ecs_client.list_tasks(
          cluster = clutser,
          serviceName = more_details['serviceName']

     )
     
     context = {
              'describe_svc': describe_ecs,
              'more_details': more_details,
              'list_tasks': list_tasks
         }
     
     return render(request, 'details.html', context)

def convert_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # or use obj.strftime('%Y-%m-%d %H:%M:%S') for custom format
    raise TypeError("Type not serializable")

def describe_task(request, cluster, task):
     print(f"MyCluster{cluster}")
     print(f"Task{task}")
     
     ecs_client = boto3.client('ecs')
     cw_client = boto3.client('logs')
     describe_tasks = ecs_client.describe_tasks(
          cluster = cluster,
          tasks = [
               task
          ]
     )
     for td in describe_tasks['tasks']:
          my_td = td['taskDefinitionArn']
          task_arn = td['taskArn']
          task_id = task_arn.split('/')[-1]

     describe_td = ecs_client.describe_task_definition(
          taskDefinition = my_td
     )
     for data in describe_td['taskDefinition']['containerDefinitions']:
          try:
             if data['logConfiguration']['logDriver'] == 'awslogs':
                log_group = data['logConfiguration']['options']['awslogs-group']
                log_stream = data['logConfiguration']['options']['awslogs-stream-prefix']
                container_name = data['name']
          except:
             return None 
     final_stream = f"{log_stream}/{container_name}/{task_id}"
     logs = cw_client.get_log_events(
            logGroupName=log_group,
            logStreamName=final_stream,
            startFromHead=True
     )
     describe_td_formatted = json.dumps(describe_td,default=convert_datetime, indent=4)
     context = {
          'describe_tasks': describe_tasks,
          'describe_td': describe_td_formatted,
          'logs': logs
     }
     return render(request, 'details.html', context)

def deploy_re(request):
     if request.method == 'POST':
          deployment_name = request.POST.get('deployment_name')
          deployment_ns = request.POST.get('deployment_ns')
          command = [
               "kubectl", "rollout", "restart", "deployment", deployment_name, "-n", deployment_ns
          ]
          subprocess.run(command, check=True)
          messages.success(request, f'Deployment "{deployment_name}" restarted successfully!')
          return redirect(home)

def restart_ds(request):
     if request.method == 'POST':
          deployment_name = request.POST.get('deployment_name')
          deployment_ns = request.POST.get('deployment_ns')
          command = [
               "kubectl", "rollout", "restart", "ds", deployment_name, "-n", deployment_ns
          ]
          subprocess.run(command, check=True)
          messages.success(request, f'Daemonset "{deployment_name}" restarted successfully!')
          return redirect(home)
     
def restart_sts(request):
     if request.method == 'POST':
          deployment_name = request.POST.get('deployment_name')
          deployment_ns = request.POST.get('deployment_ns')
          command = [
               "kubectl", "rollout", "restart", "sts", deployment_name, "-n", deployment_ns
          ]
          subprocess.run(command, check=True)
          messages.success(request, f'Statefulset "{deployment_name}" restarted successfully!')
          return redirect(home)
     
def details(request, namespace, id):
     client.EventsV1Event.event_time = FakeEventTime()
     pod_name = id
     pod_namespace = namespace

     config.load_kube_config()

     # Initialize the API client
     podq = client.CoreV1Api()
     describe_pod = podq.read_namespaced_pod(pod_name, pod_namespace)
     #log_read = podq.read_namespaced_pod_log(pod_name, pod_namespace, timestamps=True, tail_lines=70)
     load_events = client.EventsV1Api()
     read_events = load_events.list_namespaced_event(namespace=pod_namespace)
     all_containers= []
     all_images = []
     all_id = []
     restart_count = []
     container_id = []
     command_list = []   
     resources_request = []
     resources_limits = []
     final_volume = []
     full_logs = []
     return_none = []
     for data in describe_pod.spec.containers:
     #     all_containers.append(data.name)
          all_containers = data
          all_images.append(data.image)
          command = data.command or []  # Entrypoint/Command
          args = data.args or []  # Arguments to the command
          full_command = ' '.join(command + args)
          command_list.append(full_command)
          resources_request.append(data.resources.requests)
          resources_limits.append(data.resources.limits)
     if describe_pod.status.phase == 'Pending':
               return_none
     else:
          for container_state in describe_pod.spec.containers:
             print(describe_pod.status.phase)
             log_read = podq.read_namespaced_pod_log(pod_name, pod_namespace, timestamps=True, tail_lines=70, container=container_state.name) 
             full_logs.append(log_read)
     if describe_pod.status.container_statuses == None:
          return_none
     else:
          for fata in describe_pod.status.container_statuses:
#         all_id.append(fata.image_id)
              all_id.append(fata)
     pod_data = client.ApiClient().sanitize_for_serialization(describe_pod)
     pod_yaml = yaml.dump(pod_data, default_flow_style=False)

     
     # for volume_details in describe_pod.spec.containers:
     #     final_volume.append(volume_details.volume)
     context = {
          'pod_detail': describe_pod,
          'containers': all_containers,
          'images': all_images,
          'image_id': all_id,
          'restart_count': restart_count,
          'container_id': container_id,
          'command_list': command_list,
          'resources_req': resources_request,
          'resources_limits' : resources_limits,
          'fina_volume': final_volume,
          'logs': full_logs,
          'read_events': read_events,
          'pod_yaml': pod_yaml
          }
     return render(request, 'details.html', context)


def delete_pod(request):
     if request.method == 'POST':
          pod_n = request.POST.get('pod_name')
          pod_ns = request.POST.get('pod_ns')
     pod_name = pod_n
     pod_namespace = pod_ns
     command = [
               "kubectl", "delete", "pod",  pod_name, "-n", pod_namespace
          ]
     subprocess.run(command, check=True)
     messages.success(request, f'Pod "{pod_name}" deleted successfully!')
     return redirect(home)





          
     





