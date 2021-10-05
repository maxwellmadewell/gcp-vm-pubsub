import googleapiclient.discovery

PROJECT_ID = "myinstancepubsubapp"
ZONE_NAME = "us-west1-b"
VM_NAME = "dev-instance"

def start_vm(request):
    compute = googleapiclient.discovery.build('compute', 'v1')
    result = compute.instances().start(project=PROJECT_ID, zone=ZONE_NAME, instance=VM_NAME).execute()
    return result