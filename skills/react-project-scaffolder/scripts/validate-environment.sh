#!/bin/bash

# React Project Scaffolder - Environment Validation Script
# Validates prerequisites before scaffolding a project

set -e

echo "🔍 Validating environment prerequisites..."
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track validation status
VALIDATION_PASSED=true

# Check Node.js version
echo -n "Checking Node.js version... "
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version | sed 's/v//')
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d. -f1)

    if [ "$NODE_MAJOR" -ge 18 ]; then
        echo -e "${GREEN}✓${NC} Node.js $NODE_VERSION (required: >= 18.x)"
    else
        echo -e "${RED}✗${NC} Node.js $NODE_VERSION found, but >= 18.x required"
        echo "   Upgrade: https://nodejs.org/ or use nvm: nvm install 18"
        VALIDATION_PASSED=false
    fi
else
    echo -e "${RED}✗${NC} Node.js not found"
    echo "   Install from: https://nodejs.org/"
    VALIDATION_PASSED=false
fi

# Check npm version
echo -n "Checking npm version... "
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    NPM_MAJOR=$(echo $NPM_VERSION | cut -d. -f1)

    if [ "$NPM_MAJOR" -ge 9 ]; then
        echo -e "${GREEN}✓${NC} npm $NPM_VERSION (required: >= 9.x)"
    else
        echo -e "${YELLOW}⚠${NC} npm $NPM_VERSION found, >= 9.x recommended"
        echo "   Upgrade: npm install -g npm@latest"
    fi
else
    echo -e "${RED}✗${NC} npm not found"
    VALIDATION_PASSED=false
fi

# Check git
echo -n "Checking git... "
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | awk '{print $3}')
    echo -e "${GREEN}✓${NC} git $GIT_VERSION"
else
    echo -e "${YELLOW}⚠${NC} git not found (optional, but recommended)"
    echo "   Install from: https://git-scm.com/"
fi

echo ""

if [ "$VALIDATION_PASSED" = true ]; then
    echo -e "${GREEN}✅ Environment validation passed!${NC}"
    echo "You're ready to scaffold React projects."
    exit 0
else
    echo -e "${RED}❌ Environment validation failed.${NC}"
    echo "Please install the required tools listed above."
    exit 1
fi
