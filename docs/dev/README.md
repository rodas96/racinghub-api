# Developer Documentation

Welcome to the developer documentation! This directory contains comprehensive guides for working with this project's features, tools, and workflows.

## Getting Started

New to this project? Start here:

1. **[Makefile](./makefile.md)** - Essential commands for development, testing, and building
2. **[Dependencies](./dependencies.md)** - Managing project dependencies, virtual environments, and package installation
3. **[Settings](./settings.md)** - Environment configuration and settings management
4. **[Docker](./docker.md)** - Containerization, deployment, and local development with Docker

## Core Features

### [Database](./database.md)

SQLAlchemy ORM integration, models, and database patterns.

### [Caching](./cache.md)

Redis-backed caching with aiocache for performance optimization.

### [REST API](./api.md)

FastAPI web framework, endpoints, middleware, and API development.

## Development Practices

### [Testing](./testing.md)

Comprehensive testing guide covering pytest, fixtures, async testing, mocking, and code coverage.

### [Documentation](./documentation.md)

Standards and best practices for writing and maintaining project documentation.

### [GitHub Actions](./github.md)

CI/CD workflows for testing, linting, building, and deployment automation.

## Quick Reference

- **Setup**: Run `make install` to set up your development environment
- **Testing**: Run `make tests` for full test suite, see [testing.md](./testing.md) for details
- **Formatting**: Run `make chores` before committing to fix formatting issues
- **Configuration**: See [settings.md](./settings.md) for environment variables and settings
- **Local Development**: Use `docker compose up` for local services, see [docker.md](./docker.md)
- **All Make Commands**: See [makefile.md](./makefile.md) for complete reference
