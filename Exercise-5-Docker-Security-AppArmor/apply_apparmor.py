import docker

client = docker.from_env()

# Build the Docker image
client.images.build(path=".", tag="flask-apparmor")

# Attempt to run with the AppArmor profile
try:
    container = client.containers.run(
        "flask-apparmor",
        ports={'5000/tcp': 5000},
        security_opt=["apparmor=my-apparmor-profile"],
        detach=True
    )

    print(f"Container started: {container.short_id}")

    container_info = client.api.inspect_container(container.id)
    apparmor_profile = container_info['HostConfig']['SecurityOpt']

    print(f"AppArmor profile applied: {apparmor_profile}")

    container.stop()
    container.remove()

except Exception as e:
    print("AppArmor enforcement could not be applied in this environment.")
    print(f"Reason: {e}")