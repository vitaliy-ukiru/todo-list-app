Translation: [RU](./README_ru.md) | EN

<!-- TOC -->
* [Description](#description)
* [Launch](#launch)
  * [Generating a private key](#generating-a-private-key)
  * [Configuration](#configuration)
  * [Run](#run)
* [Functional](#functional)
  * [Tasks](#tasks)
  * [Lists](#lists)
* [Sharing](#sharing)
  * [Public Lists](#public-lists)
  * [Collaboration](#collaboration)
  * [Special cases](#special-cases)
    * [Move a task to another list](#move-a-task-to-another-list)
    * [Editing a task](#editing-a-task)
<!-- TOC -->

# Description

This is a note management app.
In addition to the usual work with notes, the application allows
create shared access to task lists and tasks within.

# Launch

## Generating a private key

For JWT to work, you need to generate an RSA key in PEM format

```
openssl genrsa -out key_name.pem 2048
```

## Configuration

Configuration is done using environment variables or
using a .env file. An example of settings can be found in [.env.example](./.env.example)

A detailed description of the settings can be read [here](./docs/CONFIG.md).

## Run

```
docker compose up
```

# Functional

## Tasks

1. Creation
2. Search
3. Removal
4. Mark as completed
5. Search by filters
6. Putting into lists

## Lists

1. Creation
2. Removal
3. Search
4. Sharing (more details below)

# Sharing

## Public Lists

Every user can see tasks from the public list,
but only the creator can change anything in such lists and
those who have access to update.

Public lists cannot be found in search if there is no public access.

## Collaboration

Collaborators may be able to change the state of resources.
There are rules to limit their ability.
If the user is not provided with any of the rules, then the user will be in read-only mode.

Currently available rules:

- update_tasks - Allows you to update existing tasks.
- manage_tasks - Allows you to delete/add tasks.

## Special cases

### Move a task to another list

The user performing the transfer must have the rights: `manage_tasks` in both
lists, `update_task` in the original list.
The task creator must have at least read permission.

### Editing a task

A user can change their tasks if they have read permission.
This statement is also true for cases when:

- The user only has the `manage_tasks` right
- The user has limited editing access
