# from kubernetes import client, config
import boto3
# config.load_kube_config()

# data = client.EventsV1Api()

# class FakeEventTime:
#     def __get__(self, obj, objtype=None):
#         return obj._event_time

#     def __set__(self, obj, value):
#         obj._event_time = value
# client.EventsV1Event.event_time = FakeEventTime()
# my_data = data.list_event_for_all_namespaces()
# for my_fata in my_data.items:
#     # if my_fata.regarding.name == 'prometheus-eks-prometheus-node-exporter-shp57':
#     #    print(my_fata.note)
#     print(my_fata.event)

# client = boto3.client('eks')
# data = client.list_clusters()
# for mta in data['clusters']:
#     print(mta)


# class Student():
#     def details(self):
#         self.school = "Sun shine"
#         self.address = "Muzaffarpur"
#         return self.school, self.address
#     def more_details(self):
#         return self.address
    
#     @staticmethod
#     def welcome():
#         return f"Welcome to school everyone"

# a1 = Student()
# a1.details()
# a1.welcome()
# print(a1.more_details())


# class Student:
#     def __init__(self, name, marks, school_name, school_address, **kwargs):
#         self.school_name = school_name
#         self.school_address = school_address
#         self.name = name
#         self.marks = marks
#         self.kwargs = kwargs

#     def basic(self):
#         #Logic
#         return self.name, self.marks, self.school_address, self.school_name, self.kwargs

#     @staticmethod
#     def main():
#         s1 = Student(name="Amit", marks="40", school_name="Sunshine", school_address="Mfp", dob="Jan")
#         name, marks, school_name, school_address, dob = s1.basic()
#         print(name, marks, school_name, school_address, dob)

# Student.main()


import boto3
import time
eks_client = boto3.client('eks')
ecs_client = boto3.client('ecs')

start_time = time.time()

eks_cluster_list = eks_client.list_clusters()
ecs_cluster_list =ecs_client.list_clusters()

for my_eks_cluster in eks_cluster_list['clusters']:
    my_eks_cluster
    for data in eks_cluster_list:
#    print(data.get('clusters', []), data.get('clusterArns', []))
        describe_cluster = eks_client.describe_cluster(
        name = my_eks_cluster
    )
    eks_cluster_name = describe_cluster['cluster']['arn'].split('/')[1]
    eks_cluster_svc = describe_cluster['cluster']['arn'].split(':')[2]
    eks_cluster_region= describe_cluster['cluster']['arn'].split(':')[3]
for mata in ecs_cluster_list['clusterArns']:
    eks_cluster_name = mata.split('/')[1]
    eks_cluster_svc = mata.split(':')[2]
    eks_cluster_region = mata.split(':')[3]
end_time = time.time()

# # Print execution time
print(f"Execution time: {end_time - start_time:.2f} seconds")
