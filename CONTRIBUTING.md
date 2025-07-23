# Contributing to Esk Estoic API

Thank you for your interest in contributing to the Esk Estoic API! This document provides guidelines and information for contributors.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples and sample code
- Describe the behavior you observed and what you expected
- Include your environment details (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:

- Use a clear and descriptive title
- Provide a detailed description of the suggested enhancement
- Explain why this enhancement would be useful
- List any alternatives you've considered

### Pull Request Process

1. **Fork the repository** and create your branch from `main`
2. **Follow the development setup** instructions below
3. **Make your changes** with clear, atomic commits
4. **Add tests** for any new functionality
5. **Ensure all tests pass** before submitting
6. **Update documentation** if needed
7. **Submit a pull request** with a clear description

#### Pull Request Guidelines

- Keep pull requests focused on a single feature or bug fix
- Write clear commit messages following conventional commit format
- Include tests for new features or bug fixes
- Update documentation as needed
- Ensure your code follows the project's style guidelines

## Development Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Local Development

1. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/esk_estoic_api.git
   cd esk_estoic_api
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the development server:**
   ```bash
   python -m src.main
   ```

5. **Run tests:**
   ```bash
   pytest src/ -v
   ```

### Testing

We maintain comprehensive test coverage. Please ensure:

- All existing tests pass
- New features include appropriate tests
- Bug fixes include regression tests
- Test coverage remains above 90%

**Running specific test categories:**
```bash
# API and endpoint tests
pytest src/test_main.py -v

# Static file serving tests
pytest src/test_static.py -v

# Security and middleware tests
pytest src/test_middleware.py -v

# Rate limiting tests
pytest src/test_rate_limit.py -v
```

### Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions small and focused
- Use meaningful variable and function names

### Commit Message Format

We follow the conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(api): add new endpoint for author search
fix(rate-limit): correct rate limiting headers
docs(readme): update installation instructions
```

## Project Structure

```
esk_estoic_api/
├── src/                    # Source code
│   ├── main.py            # Main application
│   ├── data/              # Data files
│   └── test_*.py          # Test files
├── static/                # Static assets
│   ├── css/               # Stylesheets
│   └── js/                # JavaScript files
├── .github/               # GitHub templates and workflows
├── docs/                  # Documentation
└── requirements.txt       # Dependencies
```

## Areas for Contribution

We welcome contributions in these areas:

### High Priority
- Adding more stoic quotes and translations
- Improving API performance and caching
- Expanding test coverage
- Security enhancements

### Medium Priority
- UI/UX improvements
- Additional language support
- API documentation improvements
- DevOps and deployment automation

### Low Priority
- New API features
- Integration examples
- Performance optimizations

## Getting Help

If you need help or have questions:

1. Check existing [GitHub Issues](https://github.com/seskelsen/esk_estoic_api/issues)
2. Read the [documentation](README.md)
3. Create a new issue with the "question" label
4. Check our [support guidelines](SUPPORT.md)

## Recognition

Contributors will be recognized in:

- The [CONTRIBUTORS.md](CONTRIBUTORS.md) file
- Release notes for significant contributions
- The project's documentation

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

Thank you for contributing to the Esk Estoic API! 🏛️