
# BU Git - A user-facing gitolite frontend

## Overview

This project aims to provide something resembling a Github or BitBucket
clone in the form of a web-based frontend to
[gitolite](https://github.com/sitaramc/gitolite). This project provides an
easy to use interface for people who want a Github like system in their
organization but cannot use Github for whatever reason.

In addition, this provides a simple interface for organizations who want to
use gitolite. It provides a nice web UI for creating, viewing, and
collaborating with git repositories that does not require giving users
access to gitolite directly and does not require forcing all changes
through and administrator. The prime audience for this application are
large businesses and universities.

This was developed for use at Boston University with an intended audience
of students, professors, and researchers. Use cases for BU include homework
collaboration and turn-in, secure hosting for projects that cannot leave BU
networks, and as a supported solution for groups who want a revision
control system.

Please feel free to contact me with any issues you encounter as well as any
suggestsions or other comments you may have. You can reach me via
mgabed@bu.edu.

## Components

### Frontend

What a user interacting with this application will see is just a website.
From the site, they can create repos and grant other users permisisons on
them. They can also set up public keys for accessing repos with.

A README file from the user's repo is displayed to them when viewing the
repo, and in addition they can view details of the repository. This viewer
is powered by [cgit](http://git.zx2c4.com/cgit/).

### Backend

On the backend, there is a daemon that receives messages whenever a user
makes a change to one of their repositories. It securely updates the
gitolite-admin repo and pushes the changes back to gitolite. The canonical
source for the gitolite-admin repo is what Django has put into the
database.

## Requirements

Everything needed to run this application should be easily installable from
repositories in CentOS 6. Other operating systems should also work, but
only CentOS is explicitly supported as that's what BU uses.

Here are some of the core components of the app though.

* Django
* Gitolite
* MySQL
* Redis
* Cgit


## Gitolite Usage

Only a basic subset of what gitolite can do is used to power this app. In
particular, gitolite's wild repos could probably replace most of what is
here. The downside though, is it becomes difficult for users to control
access to their repositories, and less-technical users will find it
difficult. This application only uses gitolite to propogate hooks, normal
repo creation and permissions, and a small abuse of gitolite's groups.

### Repos

This project uses gitolite repos just like one would expect. Each repo in
the app maps to one repo in gitolite. They are partitioned on user, so each
user's repos are in a separate file in gitolite.

### Users

Each user in this application maps to a group in gitolite. That group
consists of all of their public keys. This makes it relatively trivial for
users to use as many public-keys as they want.

### Hooks

The post-receive hook is used to update the readme for each repo after it
is pushed.

## Cgit

Cgit is used to allow users to browse through their repos. To embed cgit
into a Django app, a small hack is used. Cgit is run in a separate Apache
virtual host which Django then proxies requests to and injects the response
into its templates. This allows for a relatively seamless transition
between the cgit parts of the site and the rest of the UI.

In addition to injeting cgit, Djagno also renders some of the cgit toolbars
itself to provide a UX more in line with the rest of the site (i.e.
Bootstrap).


