# Accounts Service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SP23-001/shopcarts/branch/master/graph/badge.svg?token=451S6FLDI3)](https://codecov.io/gh/CSCI-GA-2820-SP23-001/shopcarts)
[![Build Status](https://github.com/CSCI-GA-2820-SP23-001/shopcarts/actions/workflows/tdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP23-001/shopcarts/actions)

This repository contains  code for the Customer shopcart for an e-commerce web site. This shows how to create a REST API with subordinate resources like shopcarts that have items:

Note: This repo has a both a .devcontainer folder and a Vagrantfile for two ways to bring up a development environment.

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
