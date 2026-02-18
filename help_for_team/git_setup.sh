#!/bin/bash

# Git Setup Script for Teams Clone Project

echo "🚀 Initializing Git repository..."

# Initialize git
git init

echo "📝 Creating .gitattributes..."
# Create .gitattributes
cat > .gitattributes << EOF
# Auto detect text files and perform LF normalization
* text=auto

# Python
*.py text eol=lf
*.pyx text eol=lf

# Documents
*.md text eol=lf
*.txt text eol=lf

# Config
*.yml text eol=lf
*.yaml text eol=lf
*.json text eol=lf
*.toml text eol=lf
*.ini text eol=lf
*.cfg text eol=lf

# Binary files
*.db binary
*.sqlite3 binary
*.pyc binary
*.pyo binary
EOF

echo "📦 Adding files to git..."
# Add all files
git add .

echo "💾 Creating initial commit..."
# Initial commit
git commit -m "Initial project setup

- Project structure according to requirements
- Django settings configuration
- Requirements files (base, dev, prod)
- README with setup instructions
- Corporoom tasks breakdown
- Git workflow setup"

echo "🌳 Creating main project branch..."
# Create and switch to main project branch
git branch -M teams-clone-project

echo "✅ Git repository initialized successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Create a repository on GitHub/GitLab"
echo "2. Add remote: git remote add origin <repository-url>"
echo "3. Push: git push -u origin teams-clone-project"
echo ""
echo "👥 For team members:"
echo "1. Clone repository: git clone <repository-url>"
echo "2. Create your feature branch: git checkout -b feature/your-feature-name"
echo "3. Start working on your tasks!"
