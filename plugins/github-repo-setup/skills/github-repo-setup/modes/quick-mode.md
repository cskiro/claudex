# Quick Mode

**Purpose**: Fast public repo setup with essentials (~30 seconds)

## Features Included

- README.md with basic structure
- LICENSE file (MIT default)
- .gitignore for technology stack
- Basic repository settings

## Features NOT Included

- ❌ CI/CD workflows
- ❌ Branch protection
- ❌ Issue/PR templates
- ❌ Security scanning setup
- ❌ CODEOWNERS

## When to Use

- Experiments and prototypes
- Quick test projects
- Personal projects
- Learning/tutorial repos

## Commands

```bash
# Create quick repo
gh repo create <name> --public --clone --description "<description>"
cd <name>

# Add essentials
echo "# <name>" > README.md
gh repo license create mit > LICENSE
curl -o .gitignore https://www.toptal.com/developers/gitignore/api/<tech>

# Initial commit
git add .
git commit -m "Initial commit"
git push -u origin main
```

## Next Steps After Setup

1. Add initial code
2. Push first commit
3. Consider upgrading to Enterprise mode for production
