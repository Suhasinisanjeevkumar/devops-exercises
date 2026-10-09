# Hello World Jenkins Job

This project contains a small shell script for a Jenkins Freestyle job. When run, `hello-world.sh` prints:

```text
Hello, Jenkins!
```

## Publish this project to GitHub

If `Suhasinisanjeevkumar/devops-sample-code` does not exist yet, create a **public** repository with that name on GitHub first. Do not initialize it with a README, license, or `.gitignore`; the commands below create the first commit locally.

Open PowerShell in this folder and run:

```powershell
git init
git add README.md hello-world.sh
git commit -m "Add Hello World Jenkins sample"
git branch -M main
git remote add origin https://github.com/Suhasinisanjeevkumar/devops-sample-code.git
git push -u origin main
```

If Git says that `origin` already exists, inspect the configured URL with `git remote -v` rather than adding it again. To correct an incorrect URL, run:

```powershell
git remote set-url origin https://github.com/Suhasinisanjeevkumar/devops-sample-code.git
```

## Configure the Jenkins Freestyle project

1. Sign in to Jenkins and select **New Item**.
2. Enter `HelloWorld`, select **Freestyle project**, and click **OK**.
3. Under **Source Code Management**, select **Git**.
4. Set **Repository URL** to `https://github.com/Suhasinisanjeevkumar/devops-sample-code.git`.
5. Set **Branch Specifier** to `*/main`.
6. Under **Build Steps**, choose **Execute shell** and enter:

   ```sh
   sh hello-world.sh
   ```

7. Click **Save**, then **Build Now**.
8. Open the build in **Build History** and select **Console Output**. Confirm it contains `Hello, Jenkins!` and ends with `Finished: SUCCESS`.

The Jenkins agent running the job must have `sh` available. If **Execute shell** is not available or the command cannot find `sh`, use a Linux-based Jenkins agent (or configure the Windows agent with a compatible shell) before running this exercise.

## Troubleshooting

- **Git authentication fails while pushing:** Confirm you are signed in to the intended GitHub account. If Git prompts for HTTPS credentials, use Git Credential Manager or GitHub's supported sign-in flow; do not put a password or token in this file or in the remote URL.
- **Repository URL error:** Check that the public repository exists at the exact URL above and that there are no typos. If the remote URL is wrong, use the `git remote set-url origin ...` command above.
- **Jenkins Git checkout fails:** Verify the repository is public and accessible from the Jenkins machine, the URL is correct, and the branch specifier is `*/main`. Check the checkout error in the build's Console Output. For a private repository, configure credentials in Jenkins rather than embedding them in the URL.
- **Build fails to run the script:** Confirm the build step is `Execute shell`, the command is exactly `sh hello-world.sh`, and the Jenkins agent has `sh` installed and can execute it.
