---
name: init-git-repo
description: Initialize a new git repository with a .gitignore and main as the default branch, without committing files.
---

# Init Git Repo

## Overview

Initialize a new git repository for a project. Create or update `.gitignore`, set the default branch to `main`, and leave the repo uncommitted.

## When to use

- New project directory that is not yet a git repository.
- You need a baseline `.gitignore` before adding files.

## Inputs

- `project_root` (required): Path to the project directory.
- `custom_ignores` (optional): Additional ignore patterns to append.

## Workflow

1. Confirm `project_root` exists and does not already contain a `.git` directory.
2. Create or update `.gitignore`:
   - If missing, create with the template below.
   - If present, append missing patterns; do not overwrite existing content.
3. Run `git init` in `project_root`.
4. Set the default branch to `main` using `git branch -M main`.
5. Do not commit any files.

## .gitignore template (base + conditional)

Always include the base section. Then append sections based on detected project files.

### Base (always include)

```gitignore
# vim: ft=gitignore

# 构建文件和目录
build*
*/build
build/

# 编辑器相关
.vim/
.root/
.vscode/
.idea/
*.swp
*.swo

# 开发工具配置
.ccls
.clangd
.cache
.clang-format
.vimspector.json
.vim-bookmarks
compile_commands.json
.clinerules/
.opencode/
.sisyphus/

# OSX脏文件
.DS_Store

# 编译输出
*.out
*.o
*.so
*.a
*.dot
*.tasks
*.vimrc

# 环境变量
.env
.venv
.envrc
env/
venv/
ENV/
env.bak/
venv.bak/
.pyenv
```

### Python (if `requirements.txt`, `setup.py`, or `pyproject.toml`)

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.pyc
.Python
.python-version

# 分发/打包
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
*.egg-info
.installed.cfg
*.egg
*.whl

# 测试和覆盖率报告
htmlcov/
.tox/
.coverage
.coverage.*
nosetests.xml
coverage.xml
*.cover
.hypothesis/
```

### Node.js (if `package.json`)

```gitignore
# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*
.npm
.yarn-integrity
dist/
.next/
.nuxt/
```

### Rust (if `Cargo.toml`)

```gitignore
# Rust
Cargo.lock
**/*.rs.bk
*.pdb
```

### Go (if `go.mod`)

```gitignore
# Go
*.exe
*.exe~
*.dll
*.dylib
*.test
vendor/
go.work
```

### Java/Maven (if `pom.xml`)

```gitignore
# Java/Maven
*.class
*.jar
*.war
*.ear
.mvn/
```

### Java/Gradle (if `build.gradle` or `build.gradle.kts`)

```gitignore
# Gradle
.gradle/
gradle-app.setting
!gradle-wrapper.jar
```

### C/C++ (if `.c`, `.cpp`, or `.h` files present)

```gitignore
# C/C++
*.exe
*.app
*.i*86
*.x86_64
*.hex
cmake-build-*/
CMakeCache.txt
CMakeFiles/
```

## Verification

- `git status` shows no commits and lists untracked files as expected.
- `git branch --show-current` returns `main`.

## Example requests

- "Initialize git in ./my-app and add a .gitignore. Keep it uncommitted."
- "Set up a new repo in this folder and make main the default branch."
