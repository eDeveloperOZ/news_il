# news_il
This is a project to manage the telegeram channel [news_il](https://t.me/@newssil)
## Description

## Development guide

### Adding a feature to the bot
1. Create a new branch from `main` with the name of the feature you are adding like `feature/feature_name`

### Fixing a bug
1. Create a new branch from `main` with the name of the bug you are fixing like `bug/bug_name`

### Commit messages
1. Commit messages should be in the format of `type: message` where type is one of the following:
    - `feat`: A new feature
    - `fix`: A bug fix
    - `docs`: Documentation only changes
    - `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
    - `refactor`: A code change that neither fixes a bug nor adds a feature
    - `perf`: A code change that improves performance
    - `test`: Adding missing or correcting existing tests
    - `chore`: Changes to the build process or auxiliary tools and libraries such as documentation generation

## Deployment guide
YOU MUST NOT DEPLOY!
Deployment is done automatically by github actions when a new commit is pushed to the `main` branch

## List of features: 
- [ ] Add a feature to get the latest news from the [news_il](https://t.me/@newssil) channel
- [ ] create a centrlize place to manage the news flow 
- [ ] For evey incoming message to the channel, the bot will append username, link to each social platform and the name of the channel on top. 
