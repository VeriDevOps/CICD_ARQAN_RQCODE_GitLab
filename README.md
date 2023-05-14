# Installation

To set it up, you will need to use GitLab webhooks, Docker, and Docker-Compose. The configuration process is as follows:

1. Download the project from the source repository.
2. Copy the file `.env.dist` to `.env`.
3. Go to the GitLab project or organization settings and generate the project deployment token for the bot.
4. Change the variables in the `.env` file:
    * `WEBHOOK_PREFIX`: The path prefix of the webhook. The final webhook URL will be `http://your_host:port/prefix`.
    * `WEBHOOK_TOKEN`: The authentication token for the webhook. It must be the same as will be specified later in GitLab configuration.
    * `GITLAB_INSTANCE`: The URL to the GitLab instance that hosts the project.
    * `GITLAB_REPO`: The path to the repository relative to the GitLab instance. As an example for the variable could be the path `gitlab-organization/vdo_test_project`
    * `GITLAB_TOKEN`: The previously generated token that allows bot to post messages to the repository.
    * `ARQAN_SERVICES_API`: The URL to the ARQAN services that will be used to process the text of the issues.
    * `ARQAN_USERNAME` and `ARQAN_PASSWORD`: The credentials to access ARQAN server.
    * `ARQAN_PLATFORM`: The platform on which the project is going to be deployed.
5. Start the project using docker compose with the command `docker-compose up`.
6. Configure GitLab webhook to point to the project: Go to the project settings, webhooks, and create the webhook for Issues events for the previously specified URL with the previously specified token.
