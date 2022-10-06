from prefect import flow, task


@task
def task1():
    return 1


@task
def task2(a):
    return a + 1


@flow
def my_flow():
    a = task1()
    return task2(a)


if __name__ == "__main__":
    my_flow()
