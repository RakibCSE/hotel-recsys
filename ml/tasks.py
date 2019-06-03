from celery import task


@task()
def task_number_one():
    print("Task started!")


@task()
def task_number_two():
    print("Hello World!")
