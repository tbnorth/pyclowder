# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) 
and this project adheres to [Semantic Versioning](http://semver.org/).

## 2.0.3 - 2018-04-18

### Added
- push to pypi (can now do pip install pyclowder)

### Changed
- Now has onbuild version of pyclowder
- release.sh will now tag images (e.g. this will be tagged 2.0.3 2.0 and 2)
- RABBITMQ_URI is now set to amqp://guest:guest@rabbitmq/%2F to allow easy deployment
  using docker-compose of clowder