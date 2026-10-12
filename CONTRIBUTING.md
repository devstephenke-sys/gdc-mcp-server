# Contributing to GDC MCP Server

Thank you for your interest in contributing to the GDC MCP Server! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/gdc-mcp-server.git
   cd gdc-mcp-server
   ```
3. Create a virtual environment:
   ```bash
   uv sync
   ```
4. Install development dependencies:
   ```bash
   uv sync --all-extras
   ```

## Making Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the code style guidelines

3. Add tests for new functionality

4. Run tests:
   ```bash
   uv run pytest
   ```

5. Run linting:
   ```bash
   uv run ruff check gdc_mcp
   uv run black --check gdc_mcp
   uv run mypy gdc_mcp
   ```

6. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

8. Create a Pull Request on GitHub

## Code Style

- Use type hints for all functions
- Write docstrings for all public functions and classes
- Follow PEP 8 style guide
- Use async/await for all I/O operations
- Keep functions focused and small

## Testing

- Write tests for all new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage
- Use pytest and pytest-asyncio for async tests

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions
- Update CHANGELOG.md for significant changes
- Add examples for new features

## Pull Request Process

1. Ensure your PR description clearly describes the changes
2. Link to relevant issues
3. Include screenshots for UI changes
4. Wait for CI checks to pass
5. Address review feedback

## Reporting Bugs

- Use GitHub Issues with the bug template
- Provide steps to reproduce
- Include error messages and stack traces
- Specify your Python version and OS

## Feature Requests

- Use GitHub Issues with the feature request template
- Describe the use case
- Explain why the feature would be useful
- Consider if you can implement it yourself

## Questions?

Feel free to open an issue for discussion!
