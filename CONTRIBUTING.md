# Contributing to ETF Tracker

Thank you for your interest in contributing! This document provides guidelines for contributing to the ETF Tracker project.

## 🚀 Quick Start

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/etf-tracker.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test locally: `python test_local.py`
6. Commit: `git commit -m "Add: your feature description"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## 🎯 Ways to Contribute

### Report Bugs
- Check if the bug already exists in Issues
- Include detailed steps to reproduce
- Provide Python version, OS, and error messages
- Share logs if applicable

### Suggest Features
- Describe the feature and its benefits
- Explain use cases
- Consider backwards compatibility

### Code Contributions
- Follow Python PEP 8 style guide
- Add docstrings to functions
- Include error handling
- Test your changes locally
- Update README.md if needed

### Documentation
- Fix typos and grammatical errors
- Improve explanations
- Add examples
- Translate to other languages

## 📝 Code Style

### Python
```python
def function_name(param1, param2):
    """
    Brief description of function.
    
    Args:
        param1: Description
        param2: Description
    
    Returns:
        Description of return value
    """
    # Your code here
    pass
```

### Commit Messages
- Use present tense: "Add feature" not "Added feature"
- Use imperative mood: "Fix bug" not "Fixes bug"
- Prefix with type:
  - `Add:` for new features
  - `Fix:` for bug fixes
  - `Update:` for improvements
  - `Docs:` for documentation
  - `Refactor:` for code restructuring

## 🧪 Testing

Before submitting a PR:

```bash
# Run local tests
python test_local.py

# Test actual tracker
python etf_tracker.py

# Check for Python errors
python -m py_compile etf_tracker.py
```

## 📋 Feature Ideas

Here are some ideas for contributions:

- [ ] Add more ETFs (GOLDBEES, SILVERBEES, etc.)
- [ ] Historical price tracking and charts
- [ ] Price alerts via Telegram
- [ ] Web dashboard
- [ ] Support for other messaging platforms (Discord, Slack)
- [ ] Database storage for historical data
- [ ] Machine learning price predictions
- [ ] Portfolio tracking
- [ ] Multi-language support
- [ ] Mobile app integration

## 🤝 Pull Request Process

1. Update README.md with any new dependencies or setup steps
2. Update CHANGELOG.md with your changes
3. Ensure all tests pass
4. Request review from maintainers
5. Address review comments
6. Squash commits if requested

## ⚖️ Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Accept feedback gracefully
- Focus on what's best for the community

## 📧 Contact

Questions? Open an issue or discussion on GitHub.

## 🙏 Thank You!

Every contribution, no matter how small, is appreciated!
