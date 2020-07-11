# DJANGO | Virender Bhargav

This README includes instructions for developers and maintainers for this repository.

# 1. Problem Statement


# 2. Solution Approach
* User: model(extends Django's AbstractUser) to represent any user who can use the system


# 3. Instructions for Developers

## 3.1 Branches & Environments

### 3.1.1 Branches
    There are 3 main branches namely, master, beta and develop. Other then that you must follow git flow to push your code to develop branch.
    So there are some strict rules when it comes to merging. These rules are given below
        a) You can merge "master" into "beta".
        b) You can merge "beta" into "master" and "develop".
        c) You must have to create apull request to merge code into beta and master branch.

## 3.2 Commit Process

### 3.2.1 Commit Format

Use the multi-line format defined below (do not use `-m` and go through editor):

```
[<task-id>] <task-summary>
<blank line>
- <commit description line 1>
- <commit description line 2>
- <commit description line 3>
```

In the header line `<task-id>` is the JIRA task id, and `<task-summary>` is the JIRA task summary.

**NOTE**: The blank line is important. That's what makes git know that you have a header line.

Also, optionally, you may include lines using the [smart commit syntax](https://confluence.atlassian.com/bitbucket/processing-jira-software-issues-with-smart-commit-messages-298979931.html) in your summary.

### 3.2.2 Pre-commit checks

1. Run `coverage run ./manage.py test` to run Django tests and ensure no errors
2. Run `cov-check.sh` to check code coverage and ensure it give a pass message

### 3.2.3 commit and Merge

1. `$ git add <your files..>`
2. `$ git commit` to create a commit
3. `$ git pull --rebase` to get changes from repository.
4. In case the above steps gives you any conflicts:
    1. Resolve the conflicted files by manually inspecting
    2. `git add` all conflicted files resolved manually by you
    3. `$ git rebase --continue` to tell git that you have resolved the conflicts. This may ask you to create another commit.

### 3.2.4 Push to remote

```
$ git push
```

## 2.3 Coding Standards

### 2.3.1 Python

#### 2.3.1.1 Coding Standards

We would follow the following standards:

- [PEP8](https://www.python.org/dev/peps/pep-0008/)
- [PEP257](https://www.python.org/dev/peps/pep-0257/)

Additionally, look at this [presentation](http://python.net/~goodger/projects/pycon/2007/idiomatic/presentation.html)


# 4. Development Environment Setup

## 4.1 Ubuntu 16.04

### 4.1.1 Download and Installation

-Suggested OS is Ubuntu 16.04. Install python3.7 before proceeding further: https://tecadmin.net/install-python-3-6-ubuntu-linuxmint/

### 4.1.2 How to setup new development workspace
    a) create a directory let say "uber-referral"
    b) run "cd path_to_directory"
    c) run "sudo apt-get install python3-venv"
    d) run "python3 -m venv ."
    e) run "git init"
    f) run "git remote add origin your_repo_path_url"
    g) run "git fetch --all"
    h) run "git checkout develop"
    i) run "git pull origin develop"
    j) run "source bin/activate"
    k) run "pip install -r requirements.txt"
    l) run "cp sample-file.env .env" and change env variable values accordingly
    m) run "mkdir log". This directory will used to store app logs.
    n) run "cd src"
    0) run "python manage.py runserver 0.0.0.0:8000"

# 5. Developer:
    a) Virender Bhargav (raif.viren@gmail.com)

# 6 Tech Stack:
    In this project we are using
        a) Django 3.0.7 with python 3.7.5
        b) postgresql with psycopg2
        c) EC2 of AWS for servers
        d) RDS for postgresql deployment

    
# 7. How to run test cases:
1. Run `coverage run ./manage.py test` to run Django tests and ensure no errors
2. Run `cov-check.sh` to check code coverage and ensure it give a pass message


# 8. Work Flow:


# 9. Postman Collection:
