
# BU Git - A web tool for git management

## Overview

Provides a nice web interface for creating and managing repos with
gitolite. Users can add their own repos and share their collaborations
with other people on the site. This makes it easy for organizations that
want to allow users to use source control to do so without the management
burden of configuring gitolite and without the cost of a hosted solution.

This was developed for use at Boston University and the intended users of
it are students, researchers, and professors. The collaboration tools are
intended to make it easy to run a research lab or class on top of the
system. Access is flexible and can be used for small projects between a few
individuals, shared code for an assignment, or code written by a research
lab.

Please feel free to contact me with any issues you encounter as well as any
suggestsions or other comments you may have. You can reach me via
mgabed@bu.edu.

## Technical Overview

This project is implemented as a django frontend, and a backend worker
script. The heavy lifting is all done by gitolite and cgit. This project
merely facilitates its configuration in a nice way.

The web side is a django app. User authentication is either through django
(for development) or through Django's RemoteUser support. This allows it to
easily integrate with an organization's SSO system.

The Django app talks to Redis which is used as a job queue. It queues
changes made by users which are consumed by a worker script. The queue is
merely a list of usernames. The worker script is given a username, and
regenerates the gitolite config files for that use. These consist of their
public keys and repositories. As a result of this, there has to be an
ultimate owner of each repository.

Gitolite is configured through extensive use of its group feature. Each
user is in fact a "group" in gitolite. This group consists of all of that
users public keys.


