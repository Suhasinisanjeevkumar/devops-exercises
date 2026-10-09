# Exercise 9 - Python Flask Multi-Stage Jenkins Pipeline

## Purpose

Build, test, deploy, start, and verify a small Flask application using a
five-stage Jenkins Declarative Pipeline. The pipeline creates one virtual
environment in the Jenkins workspace and reuses it for the unit and HTTP
checks.

## Folder and files

```text
Exercise-9-Python-MultiStage-Pipeline/
|-- app.py
|-- requirements.txt
|-- test_app.py
|-- Jenkinsfile
`-- README.md
```

- `app.py` - Flask application serving the exercise response at `/`.
- `requirements.txt` - Pins Flask to `2.1.2` and Werkzeug to a compatible
  version.
- `test_app.py` - Built-in `unittest` checks for the route, HTTP status, and
  exact response body.
- `Jenkinsfile` - Declarative pipeline with five stages and process cleanup.
- `README.md` - Setup and execution instructions.

## Pipeline stages

1. **Build** - Checks that Python 3 and pip are available and reports their
   versions. Creates `.venv-exercise-9` in the Jenkins workspace and installs
   `requirements.txt` into it. It fails explicitly if the runtime, pip,
   virtual-environment support, or dependency installation is unavailable.
2. **Test** - Runs `python -m unittest -v test_app` using that same virtual
   environment.
3. **Deploy** - Copies `app.py` to the workspace-relative
   `python-app-deploy` directory.
4. **Run Application** - Starts the deployed app on loopback port `5000` and
   records its process ID and log in the deployment directory.
5. **Test Application** - Waits up to 30 seconds for the app, then checks that
   `/` returns HTTP `200` and exactly
   `Hello, Jenkins Multi-Stage Pipeline!`.

The `post` section stops the application process after success or failure and
prints a completion or failure message. Concurrent builds are disabled to
avoid collisions on the workspace and application port.

## Jenkins prerequisites

- A Jenkins agent that can run the Jenkinsfile's POSIX `sh` steps (the
  container-based Jenkins agent should be Linux).
- Python 3 with `pip` and `venv`/`ensurepip` support on the agent's `PATH`.
- A writable Jenkins workspace and permission to bind loopback port `5000`.
- Network access to the configured Python package index, or a configured
  package mirror containing the pinned dependencies.
- Jenkins Pipeline support and the Git plugin for Pipeline script from SCM.

The pipeline checks for Python and pip rather than assuming either exists. It
does not install system packages or modify the Jenkins container. If one of
these prerequisites is missing, resolve it through your normal Jenkins agent
image or administrator-managed configuration; do not add it by running
package-install commands in this pipeline.

## Configure a Pipeline job using Pipeline script from SCM

1. In Jenkins, select **New Item**, enter a job name, choose **Pipeline**, and
   select **OK**.
2. In the job configuration, find the **Pipeline** section.
3. Set **Definition** to **Pipeline script from SCM**.
4. Set **SCM** to **Git** and enter this repository URL:

   `https://github.com/Suhasinisanjeevkumar/devops-exercises.git`

5. Set **Branches to build** to `*/main`.
6. Set **Script Path** to:

   `Exercise-9-Python-MultiStage-Pipeline/Jenkinsfile`

7. Save the job. For a private repository, configure Jenkins-managed
   credentials in the Git SCM settings rather than embedding credentials in
   the repository URL.

## Run the job and inspect Console Output

Open the job and select **Build Now**. Select the resulting build number, then
select **Console Output** to follow each stage and see test and HTTP-check
results. The Pipeline view should show the five named stages in order.

## Expected result

- Build reports Python and pip versions and installs the pinned requirements.
- Test reports one passing unittest.
- Deploy reports the destination under the Jenkins workspace.
- Test Application prints:
  `PASS: HTTP 200; response body matches exactly.`
- The build finishes with:
  `SUCCESS: Exercise 9 multi-stage pipeline completed successfully.`

The success message is expected only after the pipeline has actually completed
successfully; configuring the job alone does not run it.

## Troubleshooting

- **Python 3 not found** - Make Python 3 available on the agent's `PATH` or
  use an administrator-managed agent image that includes it.
- **pip or `venv` unavailable** - Install/enable Python's pip and virtual
  environment support in the managed agent image, then rerun the job.
- **Dependency installation failed** - Check agent network access, DNS,
  package-index configuration, and any Jenkins proxy settings. Use an
  approved package mirror if direct package-index access is unavailable.
- **Unit test import failure** - Confirm the Build stage installed the
  requirements successfully and inspect the reported virtual-environment
  Python path.
- **HTTP check times out or returns an error** - Review the Run Application
  output and the application log printed by Test Application. Confirm port
  `5000` is available to the Jenkins agent.
- **SCM checkout or Jenkinsfile not found** - Check repository credentials,
  branch `*/main`, and the exact Script Path above.
- **Pipeline syntax or `sh` step unavailable** - Confirm the Pipeline plugin
  is installed and that the job is running on an agent that supports POSIX
  shell steps.

## Successful-pipeline screenshot checklist

- [ ] Pipeline view shows Build, Test, Deploy, Run Application, and Test
  Application as successful.
- [ ] Console Output shows the Python/pip version checks and successful
  dependency installation.
- [ ] Console Output shows the unittest passing and the exact HTTP `200`
  response verification.
- [ ] Console Output shows the Exercise 9 success message.
