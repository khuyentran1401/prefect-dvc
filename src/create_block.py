from prefect_gcp.cloud_run import CloudRunJob
from prefect_gcp.credentials import GcpCredentials

cred = GcpCredentials(
    service_account_file="/Users/khuyen/Documents/helpful-cat-364614-1276d324f379.json"
)
cred.save(name="gcp-cred", overwrite=True)

job = CloudRunJob(
    image="gcr.io/helpful-cat-364614/custom-segmentation",
    region="us-central1",
    credentials=cred,
    cpu=1.0,
)
job.save(name="gcp-run", overwrite=True)
