# Contributing to GPToggle

Thank you for your interest in contributing to GPToggle! This document provides guidelines and information for contributors.

## 🤝 Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and constructive in all interactions.

### Our Standards

- **Be Respectful**: Treat everyone with respect and kindness
- **Be Constructive**: Provide helpful feedback and suggestions
- **Be Inclusive**: Welcome contributors from all backgrounds and experience levels
- **Be Patient**: Help newcomers learn and grow

### Unacceptable Behavior

- Harassment, discrimination, or offensive language
- Personal attacks or trolling
- Spam or off-topic discussions
- Sharing private information without permission

## 🚀 Getting Started

### Development Environment Setup

1. **Fork and Clone**
   ```bash
   git fork https://github.com/yourusername/gptoggle.git
   cd gptoggle
   ```

2. **Install Dependencies**
   ```bash
   # Python dependencies
   pip install -e .[dev]
   
   # JavaScript dependencies
   npm install
   ```

3. **Set Up Environment Variables**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Add your API keys
   export OPENAI_API_KEY="your-key-here"
   export ANTHROPIC_API_KEY="your-key-here"
   # ... other API keys
   ```

4. **Run Tests**
   ```bash
   # Python tests
   python -m pytest tests/ -v
   
   # JavaScript tests
   npm test
   
   # Module system tests
   python test_modules_demo.py
   ```

## 🔧 Development Guidelines

### Code Style

#### Python
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for function parameters and return values
- Maximum line length: 100 characters
- Use meaningful variable and function names

```python
def create_module_with_umid(self, module_type: str, 
                           context_keywords: List[str], 
                           initial_data: Any) -> Dict[str, Any]:
    """Create a new module with Universal Module Identifier"""
    pass
```

#### JavaScript/TypeScript
- Use TypeScript for all new JavaScript code
- Follow [ESLint](https://eslint.org/) recommendations
- Use async/await for asynchronous operations
- Use meaningful interface definitions

```typescript
interface ModuleData {
  type: string;
  keywords: string[];
  data: any;
  metadata: ModuleMetadata;
}
```

### Commit Messages

Use clear, descriptive commit messages following this format:

```
type(scope): brief description

Detailed explanation if needed

- Additional details
- Bug fixes or features
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions or modifications
- `chore`: Build process or auxiliary tool changes

**Examples:**
```
feat(modules): add UMID generation for cross-platform compatibility

- Implement UMIDGenerator class with service-specific IDs
- Add context hash generation from keywords
- Include timestamp and random components for uniqueness
```

### Branch Naming

Use descriptive branch names:
- `feature/module-lifecycle-management`
- `fix/provider-selection-bug`
- `docs/api-reference-update`
- `refactor/umid-generator-optimization`

## 📝 Types of Contributions

### 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear Description**: What happened vs. what was expected
2. **Reproduction Steps**: Minimal steps to reproduce the issue
3. **Environment Details**: OS, Python/Node version, GPToggle version
4. **Error Messages**: Full error messages and stack traces
5. **Sample Code**: Minimal code example that demonstrates the issue

**Bug Report Template:**
```markdown
## Bug Description
Brief description of the bug.

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should have happened.

## Actual Behavior
What actually happened.

## Environment
- OS: [e.g., macOS 12.0]
- Python: [e.g., 3.9.0]
- GPToggle: [e.g., 2.0.0]
- Provider: [e.g., OpenAI]

## Error Messages
```
[Paste error messages here]
```

## Sample Code
```python
# Minimal code that reproduces the issue
```
```

### 💡 Feature Requests

For new features, please provide:

1. **Clear Use Case**: Why is this feature needed?
2. **Detailed Description**: How should it work?
3. **Examples**: Code examples of the proposed API
4. **Alternatives Considered**: Other approaches you've considered
5. **Breaking Changes**: Will this require breaking changes?

### 🔧 Code Contributions

#### Process

1. **Create an Issue**: Discuss your idea before starting work
2. **Fork and Branch**: Create a feature branch from `main`
3. **Implement**: Write code following our guidelines
4. **Test**: Add tests and ensure all tests pass
5. **Document**: Update documentation as needed
6. **Pull Request**: Submit PR with clear description

#### Pull Request Guidelines

- **One Feature Per PR**: Keep PRs focused on a single feature or fix
- **Clear Description**: Explain what the PR does and why
- **Tests Required**: All new code must include tests
- **Documentation**: Update docs for new features
- **No Breaking Changes**: Unless discussed in an issue first

**PR Template:**
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests added for new functionality
- [ ] Documentation updated
```

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── test_core.py              # Core functionality tests
├── test_modules.py           # Module system tests
├── test_providers.py         # AI provider tests
├── test_umid.py             # UMID system tests
├── test_integration.py       # End-to-end tests
└── fixtures/                # Test data and fixtures
```

### Writing Tests

#### Python Tests (pytest)
```python
import pytest
from gptoggle_v2 import GPToggle, UserProfile

class TestModuleSystem:
    def test_create_shopping_list_module(self):
        """Test automatic shopping list module creation"""
        profile = UserProfile.create_default("test-user")
        
        result = profile.update_profile_with_modules(
            "I need to buy milk and eggs", 
            "general"
        )
        
        assert len(result['moduleActions']) == 1
        assert result['moduleActions'][0]['action'] == 'create'
        assert result['moduleActions'][0]['moduleType'] == 'list'
```

#### JavaScript Tests (Jest)
```javascript
import { UMIDGenerator } from '../modules/umidGenerator';

describe('UMIDGenerator', () => {
  test('generates valid UMID format', () => {
    const generator = new UMIDGenerator('test-service');
    const umid = generator.generateUMID('list', ['shopping', 'groceries']);
    
    expect(umid).toMatch(/^test-service\.list\.[a-f0-9]{8}\.\d{10}\.[a-z0-9]{4}$/);
  });
});
```

### Running Tests

```bash
# Run all Python tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_modules.py -v

# Run with coverage
python -m pytest tests/ --cov=gptoggle --cov-report=html

# Run JavaScript tests
npm test

# Run specific test suite
npm test -- --testNamePattern="UMID"
```

## 📚 Documentation

### Types of Documentation

1. **API Documentation**: Function and class documentation
2. **User Guides**: How-to guides for users
3. **Developer Docs**: Technical documentation for contributors
4. **Examples**: Code examples and tutorials

### Documentation Standards

- Use clear, concise language
- Include code examples for all features
- Keep examples up-to-date with current API
- Use proper markdown formatting
- Include performance considerations where relevant

### Updating Documentation

When adding new features:
1. Update relevant files in `docs/`
2. Add examples to `examples/`
3. Update the main `README.md`
4. Update `CHANGELOG.md`

## 🏗️ Architecture Guidelines

### Core Principles

1. **Modularity**: Keep components loosely coupled
2. **Extensibility**: Make it easy to add new providers and module types
3. **Backward Compatibility**: Avoid breaking changes
4. **Performance**: Optimize for speed and memory usage
5. **Security**: Handle API keys securely, validate inputs

### Adding New Features

#### New AI Providers
1. Create provider class inheriting from `BaseProvider`
2. Implement required methods (`query`, `get_models`, etc.)
3. Add provider to registry
4. Add configuration options
5. Write tests and documentation

#### New Module Types
1. Define module schema in `userProfileSchema.json`
2. Add parsing logic to `ModuleService`
3. Implement data extraction methods
4. Add lifecycle management rules
5. Write tests and examples

#### New UMID Components
1. Update `UNIVERSAL_MODULE_ID_SCHEMA.md`
2. Modify `UMIDGenerator` classes
3. Update parsing and validation logic
4. Ensure backward compatibility
5. Add migration support

## 🚀 Release Process

### Version Numbers

We follow [Semantic Versioning](https://semver.org/):
- **Major** (X.0.0): Breaking changes
- **Minor** (0.X.0): New features, backward compatible
- **Patch** (0.0.X): Bug fixes, backward compatible

### Release Steps

1. **Update Version**: Bump version in `package.json` and `pyproject.toml`
2. **Update Changelog**: Add new version entry to `CHANGELOG.md`
3. **Run Tests**: Ensure all tests pass
4. **Create Tag**: Create git tag for the version
5. **Publish**: Publish to npm and PyPI
6. **GitHub Release**: Create GitHub release with notes

## 🎯 Areas for Contribution

### High Priority
- **Performance Optimization**: Improve module operation speed
- **Additional AI Providers**: Support for new AI services
- **Mobile Support**: React Native or mobile web optimizations
- **Documentation**: Improve examples and tutorials

### Medium Priority
- **Visual Modules**: Support for image and diagram-based planning
- **Team Collaboration**: Shared modules across users
- **Advanced Analytics**: Usage insights and patterns
- **Integration APIs**: Connections to productivity tools

### Good First Issues
- **Bug Fixes**: Simple bug fixes and improvements
- **Documentation**: Improve existing documentation
- **Examples**: Add new usage examples
- **Tests**: Increase test coverage

## 💬 Communication

### Where to Get Help

- **GitHub Discussions**: General questions and discussions
- **GitHub Issues**: Bug reports and feature requests
- **Discord/Slack**: Real-time chat (if available)
- **Email**: Direct contact for sensitive issues

### Response Times

- **Issues**: We aim to respond within 48 hours
- **Pull Requests**: Initial review within 72 hours
- **Discussions**: Community-driven, typically within 24 hours

## 🙏 Recognition

Contributors are recognized in:
- `CONTRIBUTORS.md` file
- GitHub contributor graphs
- Release notes for significant contributions
- Special mentions in documentation

Thank you for contributing to GPToggle! Your efforts help make AI assistance more intelligent and accessible for everyone.