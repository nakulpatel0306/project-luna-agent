#!/bin/bash

# luna desktop agent - project structure setup
# run this from your project root

echo "🌙 setting up luna project structure..."

# create main directories
mkdir -p src/frontend
mkdir -p src/backend
mkdir -p src/shared
mkdir -p docs
mkdir -p tests

# frontend structure (tauri + react)
mkdir -p src/frontend/src/components
mkdir -p src/frontend/src/hooks
mkdir -p src/frontend/src/utils
mkdir -p src/frontend/src/styles
mkdir -p src/frontend/src/types
mkdir -p src/frontend/public

# backend structure (python)
mkdir -p src/backend/agent
mkdir -p src/backend/api
mkdir -p src/backend/integrations
mkdir -p src/backend/knowledge
mkdir -p src/backend/safety
mkdir -p src/backend/utils

# shared types/models
mkdir -p src/shared/types
mkdir -p src/shared/models

# documentation
mkdir -p docs/architecture
mkdir -p docs/api
mkdir -p docs/user-guide

# tests
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/e2e

# config directory
mkdir -p config

echo "✅ directory structure created"
echo ""
echo "next steps:"
echo "1. initialize tauri project in src/frontend"
echo "2. set up python virtual environment in src/backend"
echo "3. create initial configuration files"
