# Exercise 7 - Introduction to CI and Jenkins Installation

## Objectives

- Understand continuous integration (CI) and how CI/CD tools help teams deliver software.
- Install and unlock Jenkins in Docker on Windows.
- Create a Jenkins Pipeline that checks the exercise files and runs an automated shell test.

## What is Continuous Integration?

Continuous Integration (CI) is the practice of frequently combining developers' code changes in a shared source-code repository. Whenever a change is submitted, automated jobs can build the project and run checks and tests. Finding problems soon after a change is made usually makes them easier to understand and fix.

CI is often part of CI/CD:

- **Continuous Integration** repeatedly combines changes and checks that the software still works.
- **Continuous Delivery** keeps tested changes ready to release.
- **Continuous Deployment** automatically releases changes that pass the required checks.

### Key features and benefits

- **Automation:** Builds, tests, and other repeatable checks run without someone doing each step by hand.
- **Frequent feedback:** A failed check can alert the team soon after a change is submitted.
- **Consistent checks:** Changes are checked using the same defined steps.
- **Shared visibility:** Build and test results help developers see whether a change is ready for the next step.
- **Lower integration risk:** Combining small changes often can make conflicts and regressions easier to identify.
- **Faster, more dependable releases:** Teams can spend less time on manual repetitive work and more time improving the software.

### How a CI workflow works

1. A developer changes code and submits it to a shared version-control repository.
2. A CI server notices the change or is asked to start a run.
3. The server checks out the source code into a workspace.
4. It runs the configured steps, such as validation, building, and tests.
5. It reports success or failure so the team can act on the result.
6. If the checks pass, the change can move to a delivery or deployment step.

## Ten CI/CD tools

These tools help automate some or all of building, testing, delivery, and deployment. Their features and hosting options differ.

1. **GitLab CI/CD** - CI/CD is integrated with GitLab repositories. Pipelines are commonly described in a `.gitlab-ci.yml` file and run on GitLab Runners.
2. **CircleCI** - A CI/CD service that runs configured workflows for projects connected to it.
3. **Travis CI** - A hosted CI service that runs build and test workflows, commonly configured in `.travis.yml`.
4. **Bamboo** - Atlassian's build and deployment automation server, often used with other Atlassian products.
5. **TeamCity** - JetBrains' CI server for configuring and monitoring build pipelines.
6. **Azure DevOps** - Microsoft's suite for source control, planning, CI pipelines, and release/deployment workflows.
7. **GitHub Actions** - GitHub's workflow automation service. YAML workflow files can run in response to repository events.
8. **Spinnaker** - An open-source, multi-cloud continuous-delivery platform focused on release and deployment workflows; it is not primarily a build-and-test CI server.
9. **Buildkite** - A CI/CD platform that coordinates pipelines and uses agents to run jobs in an environment you manage.
10. **Drone** - A container-based CI/CD platform that can run pipeline steps in containers.

## Introduction to Jenkins

Jenkins is an automation server used to build, test, and deliver software. It is open source and can run on a computer, a server, or in a container.

### Jenkins concepts

- **Job (or project):** A configured task Jenkins can run, such as a Pipeline.
- **Build:** One execution of a job. Its result and console output help explain what happened.
- **Pipeline:** A repeatable workflow made of stages and steps. A `Jenkinsfile` can store a Pipeline as code alongside a project's source.
- **Plugin:** An add-on that extends Jenkins, for example with integrations or additional job features. Plugins should be chosen and maintained thoughtfully.
- **Node (or agent):** A machine or execution environment where Jenkins runs build steps. The controller coordinates work; agents can provide separate or specialized environments.

### Benefits

- Automates repeatable development and delivery tasks.
- Pipelines can be reviewed and versioned as code.
- A large plugin ecosystem supports integrations and additional capabilities.
- Jobs can run on separate agents and environments as a project grows.
- Build history and console logs make results visible and help with troubleshooting.

## Install Jenkins with Docker on Windows

These instructions use PowerShell and Docker Desktop. Docker Desktop must already be installed and running; this exercise does not install software.

1. Open PowerShell.
2. Check that Docker is available and the Docker engine is running:

   ```powershell
   docker version
   ```

3. Create a named volume so Jenkins data can persist when its container is restarted:

   ```powershell
   docker volume create jenkins_home
   ```

4. Start Jenkins:

   ```powershell
   docker run -d --name jenkins-ci `
     -p 8080:8080 `
     -p 50000:50000 `
     -v jenkins_home:/var/jenkins_home `
     jenkins/jenkins:lts-jdk21
   ```

5. Wait for Jenkins to start. You can check its container status and startup log:

   ```powershell
   docker ps --filter "name=jenkins-ci"
   docker logs jenkins-ci
   ```

   The first startup can take a few minutes.

### Retrieve the initial password and unlock Jenkins

1. In PowerShell, retrieve the one-time initial administrator password from the container:

   ```powershell
   docker exec jenkins-ci cat /var/jenkins_home/secrets/initialAdminPassword
   ```

2. Open **http://localhost:8080** in a browser.
3. Enter the initial password shown by the command to unlock Jenkins.
4. Choose **Install suggested plugins**, then wait for setup to finish.
5. Create your own administrator account and complete the setup prompts.

The password printed during setup is a secret. Do not put it in this README, source files, screenshots, or a public chat. Do not share a screenshot that reveals it.

## Configure and run the Pipeline

The [Jenkinsfile](./Jenkinsfile) has three stages:

1. **Checkout** - checks out the source configured for the Jenkins job.
2. **Validate Files** - fails if any of the four required exercise files is missing.
3. **Run Tests** - executes `sh ./test_hello.sh`.

The Pipeline also reports a success or failure message using `post` conditions. It expects a Jenkins node with a POSIX shell (`sh`) available.

### Configure a Pipeline job

1. Make sure the Jenkins job's source repository contains this Exercise 7 folder and all four files, and that Jenkins can access that repository. **These instructions do not commit or push the files for you.** Since these files are currently local to your workspace, an SCM-based Jenkins job cannot check them out from a remote repository until you choose to make them available there.
2. On the Jenkins home page, select **New Item**.
3. Enter a job name, select **Pipeline**, and select **OK**.
4. Under **Pipeline**, set **Definition** to **Pipeline script from SCM**.
5. Select **Git** as the SCM, enter the repository URL, and configure credentials if the repository requires them.
6. Set the branch to the branch containing the exercise and set **Script Path** to:

   ```text
   Exercise-7-Introduction-to-CI-and-Jenkins-Installation/Jenkinsfile
   ```

7. Select **Save**, then choose **Build Now**.
8. Open the build and select **Console Output** to follow the stages and see the final result.

If your project uses a different default branch or folder layout, adjust the branch and Script Path to match it. Do not put repository credentials in the Jenkinsfile.

## Verification

Run the shell test locally from PowerShell while the current directory is this Exercise 7 folder. The command requires Bash to be available (for example, through an existing Git for Windows or WSL installation); this exercise does not install it.

```powershell
bash ./test_hello.sh
```

Expected output:

```text
PASS: hello.sh printed the expected message.
```

To check the script's output directly:

```powershell
bash ./hello.sh
```

Expected output:

```text
Hello from Exercise 7 CI!
```

In Jenkins, verify that **Checkout**, **Validate Files**, and **Run Tests** complete successfully and that the post-build success message appears in Console Output.

## Screenshot checklist

Capture screenshots only after setup is complete. Useful evidence for the exercise includes:

- Jenkins home page showing that Jenkins is available at `http://localhost:8080`.
- The Pipeline job's configuration showing the Pipeline definition and Script Path (hide repository credentials and other private information).
- A successful build's stage view or Console Output showing all three stages and the success message.
- The local test's PASS output in PowerShell.

Never include the initial administrator password, account passwords, access tokens, or other credentials in a screenshot.
