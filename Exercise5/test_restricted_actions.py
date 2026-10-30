
import docker

client = docker.from_env()

container = client.containers.run(
    "flask-apparmor",
    ports={"5000/tcp": 5002},
    security_opt=["apparmor=flask-apparmor"],
    detach=True
)

try:
    exit_code, output = container.exec_run("cat /etc/passwd")
    print(
        f"Attempt to read /etc/passwd: "
        f"Exit Code {exit_code}, Output: {output.decode()}"
    )

    exit_code, output = container.exec_run("/bin/bash")
    print(
        f"Attempt to execute /bin/bash: "
        f"Exit Code {exit_code}, Output: {output.decode()}"
    )
finally:
    container.stop()
    container.remove()
