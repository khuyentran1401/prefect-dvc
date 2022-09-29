from dvc.api import DVCFileSystem

url = "https://github.com/khuyentran1401/dvc-demo"
fs = DVCFileSystem(url, rev="master")

print(fs.find("/", detail=False))
