# Accounts Service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SP23-001/shopcarts/branch/master/graph/badge.svg?token=451S6FLDI3)](https://codecov.io/gh/CSCI-GA-2820-SP23-001/shopcarts)
[![Build Status](https://github.com/CSCI-GA-2820-SP23-001/shopcarts/actions/workflows/tdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP23-001/shopcarts/actions)

This repository contains  code for the Customer shopcart for an e-commerce web site. This shows how to create a REST API with subordinate resources like shopcarts that have items:

Note: This repo has a both a .devcontainer folder and a Vagrantfile for two ways to bring up a development environment.

## Automatic Setup

The best way to use this repo is to start your own repo using it as a git template. To do this just press the green **Use this template** button in GitHub and this will become the source for your repository.

## Manual Setup

You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own `README.md` file so be selective in what you copy.

There are 4 hidden files that you will need to copy manually if you use the Mac Finder or Windows Explorer to copy files from this folder into your repo folder.

These should be copied using a bash shell as follows:

```bash
    cp .gitignore  ../<your_repo_folder>/
    cp .flaskenv ../<your_repo_folder>/
    cp .gitattributes ../<your_repo_folder>/
```

## Running the service

The project uses *honcho* which gets it's commands from the `Procfile`. To start the service simply use:

```shell
$ honcho start
```

You should be able to reach the service at: http://localhost:8000. The port that is used is controlled by an environment variable defined in the `.flaskenv` file which Flask uses to load it's configuration from the environment by default.

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

## Information about this repo
These are the RESTful routes for `shopcarts` and `items`
```
Endpoint          Methods  Rule
----------------  -------  -----------------------------------------------------
index             GET      /

list_shopcarts     GET      /shopcarts
create_shopcarts   POST     /shopcarts
get_shopcarts      GET      /shopcarts/<shopcart_id>
update_shopcarts   PUT      /shopcarts/<shopcart_id>
delete_shopcarts   DELETE   /shopcarts/<shopcart_id>

list_items    GET      /shopcarts/<int:shopcart_id>/items
create_items  POST     /shopcarts/<shopcart_id>/items
get_items     GET      /shopcarts/<shopcart_id>/items/<item_id>
update_items  PUT      /shopcarts/<shopcart_id>/items/<item_id>
delete_items  DELETE   /shopcarts/<shopcart_id>/items/<item_id>
```

The test cases have 95% test coverage and can be run with `nosetests`.
