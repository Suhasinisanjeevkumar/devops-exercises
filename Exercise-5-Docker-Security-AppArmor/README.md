\# Exercise 5 - Docker Security with AppArmor and Python



\## Objective



Secure a Dockerized Flask application using an AppArmor security profile and Python Docker SDK, and test restricted actions inside the container.



\## Environment



\- Windows 11

\- Docker Desktop with WSL2

\- Ubuntu WSL2

\- Python

\- Docker Python SDK



\## Files



\- `app.py` - Flask application

\- `Dockerfile` - Docker image definition

\- `my-apparmor-profile` - AppArmor security profile

\- `apply\_apparmor.py` - Python Docker SDK script

\- `test\_restricted\_actions.py` - Restricted action testing script

\- `README.md` - Exercise documentation



\## Task 1 - Flask Application



The Flask application exposes `/` and returns:



> Hello, this is a secure Flask application running inside a Docker container!



The application listens on `0.0.0.0:5000`.



\## Task 2 - Docker Image



The image was built successfully using:



```powershell

docker build -t flask-apparmor .

```



The Flask container was tested using:



```powershell

docker run -d --name flask-apparmor-test -p 5000:5000 flask-apparmor

```



The endpoint returned HTTP 200 with the expected Flask response.



\## Task 3 - AppArmor Profile



The `my-apparmor-profile` file was created using the profile provided in the exercise.



The profile attempts to restrict:



\- `/etc/`

\- `/var/`

\- `/bin/`

\- `/usr/bin/`

\- `sys\_admin` capability



It allows the required network capability and access to `/app/`.



\## Task 4 - Python Docker SDK



Docker SDK for Python was installed successfully:



```powershell

pip install docker

```



The `apply\_apparmor.py` script successfully started the container and inspected its security configuration.



Observed output:



```text

Container started: 294aba8014b2

AppArmor profile applied: \['apparmor=my-apparmor-profile']

```



This confirms that Docker accepted the AppArmor security option in the container configuration.



\## Task 5 - Restricted Action Testing



The following actions were tested using `test\_restricted\_actions.py`.



\### Read `/etc/passwd`



```text

Exit Code 0

```



The file was readable.



\### Execute `/bin/bash`



```text

Exit Code 0

```



The command was executable.



\## Docker Security Verification



The Docker engine security options were checked using:



```powershell

docker info --format '{{json .SecurityOptions}}'

```



Observed result:



```text

\["name=seccomp,profile=builtin","name=cgroupns"]

```



AppArmor was not listed as an active Docker engine security option.



In WSL2, `aa-status` showed:



```text

apparmor module is loaded.

apparmor filesystem is not mounted.

```



\## Result and Platform Limitation



The Docker SDK accepted the AppArmor profile configuration, but the restricted actions were not blocked.



Therefore, AppArmor enforcement could not be fully validated on the current Windows + Docker Desktop + WSL2 environment.



The exercise successfully demonstrated:



\- Flask application containerization

\- Docker image building

\- AppArmor profile creation

\- Docker SDK usage

\- Docker security option inspection

\- Restricted action testing

\- Identification and documentation of the platform limitation



The expected restriction results from the original exercise were \*\*not observed\*\*, so they are not falsely claimed as successful.



\## Questions and Answers



\### 1. What is the purpose of AppArmor in Docker?



AppArmor provides mandatory access control that restricts what processes inside a container can access or execute.



\### 2. Why restrict sensitive directories?



Directories such as `/etc` and `/var` can contain configuration files, credentials, system information, and logs. Restricting access reduces security risks.



\### 3. Why restrict Linux capabilities?



Restricting unnecessary capabilities follows the principle of least privilege and reduces the container's attack surface.



\### 4. How can the AppArmor profile be verified?



The container configuration can be inspected using Docker SDK or Docker CLI. In this exercise, Docker SDK reported:



```text

\['apparmor=my-apparmor-profile']

```



However, the restriction tests showed that actual AppArmor enforcement was unavailable in the current environment.



\## Conclusion



This exercise demonstrated how an AppArmor profile can be specified for a Docker container and how Python Docker SDK can configure and inspect container security settings. Testing also identified that the current Windows/WSL2 Docker Desktop environment does not provide active AppArmor enforcement.

