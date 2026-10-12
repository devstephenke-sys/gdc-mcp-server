# Publishing Guide: GDC MCP Server to MCP Registry

This guide walks you through publishing your Python-based GDC MCP Server to the MCP Registry via PyPI.

## Overview

The MCP Registry requires two steps:
1. **Publish your package to PyPI** (hosts the actual code)
2. **Publish metadata to MCP Registry** (hosts the server information)

## Prerequisites

✅ **Already Completed:**
- Public GitHub repository: https://github.com/devstephenke-sys/gdc-mcp-server
- MCP name added to README: `mcp-name: io.github.devstephenke-sys/gdc-mcp-server`
- pyproject.toml updated with correct metadata
- v0.1.0 release published on GitHub

⚠️ **You Need:**
- PyPI account (https://pypi.org/account/register/)
- PyPI API token (after account creation)

---

## Step 1: Create PyPI Account

1. Go to https://pypi.org/account/register/
2. Fill in:
   - Username: `devstephenke-sys` (or your preferred username)
   - Email: `devstephen.ke@gmail.com`
   - Password: (create a strong password)
3. Verify your email
4. **Enable 2FA** (required for publishing)
   - Go to Account Settings → Two-factor authentication
   - Set up either authenticator app or SMS
5. Generate API Token:
   - Go to Account Settings → API tokens
   - Click "Add API token"
   - Name: `gdc-mcp-server`
   - Scope: "Entire account"
   - Copy the token (save it securely - you won't see it again!)

---

## Step 2: Install Publishing Tools

Open PowerShell in your project directory:

```powershell
# Install build and twine
pip install build twine

# Or use uv
uv pip install build twine
```

---

## Step 3: Build the Package

```powershell
cd "C:\Users\DBTECH AFRICA\Desktop\Cancer Research\gdc-mcp-server"

# Build the package
python -m build

# Or with uv
uv run python -m build
```

This will create a `dist/` directory with:
- `gdc-mcp-server-0.1.0.tar.gz` (source distribution)
- `gdc_mcp_server-0.1.0-py3-none-any.whl` (wheel)

---

## Step 4: Test the Package Locally (Optional but Recommended)

```powershell
# Check the package metadata
twine check dist/*

# Upload to TestPyPI first
twine upload --repository testpypi dist/*
```

If you use TestPyPI, you'll need to:
1. Create a TestPyPI account at https://test.pypi.org/account/register/
2. Use your TestPyPI username and password
3. Install from TestPyPI to verify:
   ```powershell
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ gdc-mcp-server
   ```

---

## Step 5: Publish to PyPI

```powershell
# Upload to PyPI
twine upload dist/*
```

When prompted:
- **Username**: Your PyPI username
- **Password**: Your PyPI API token (NOT your account password)

You should see:
```
Uploading gdc-mcp-server-0.1.0.tar.gz
Uploading gdc_mcp_server-0.1.0-py3-none-any.whl
Uploaded to https://pypi.org/project/gdc-mcp-server/0.1.0/
```

Verify at: https://pypi.org/project/gdc-mcp-server/

---

## Step 6: Install mcp-publisher CLI

The MCP Registry provides the `mcp-publisher` CLI tool for publishing metadata.

**For Windows (PowerShell):**

```powershell
# Download mcp-publisher
$arch = if ([System.Runtime.InteropServices.RuntimeInformation]::ProcessArchitecture -eq "Arm64") { "arm64" } else { "amd64" }
Invoke-WebRequest -Uri "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_windows_$arch.tar.gz" -OutFile "mcp-publisher.tar.gz"
tar xf mcp-publisher.tar.gz mcp-publisher.exe
rm mcp-publisher.tar.gz

# Move to PATH (choose one directory)
# Option 1: Move to Scripts directory
Move-Item mcp-publisher.exe "C:\Users\DBTECH AFRICA\AppData\Roaming\Python\Python312\Scripts\"

# Option 2: Add to system PATH manually
# Move to a directory in your PATH
```

**Verify installation:**

```powershell
mcp-publisher --help
```

You should see:
```
MCP Registry Publisher Tool

Usage:
  mcp-publisher <command> [arguments]

Commands:
  init          Create a server.json file template
  login         Authenticate with the registry
  logout        Clear saved authentication
  publish       Publish server.json to the registry
```

---

## Step 7: Create server.json

Run the init command in your project directory:

```powershell
cd "C:\Users\DBTECH AFRICA\Desktop\Cancer Research\gdc-mcp-server"
mcp-publisher init
```

This will create a `server.json` file. Edit it to match:

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
  "name": "io.github.devstephenke-sys/gdc-mcp-server",
  "description": "Model Context Protocol server for NCI Genomic Data Commons - enabling AI agents to query and download cancer genomic data",
  "repository": {
    "url": "https://github.com/devstephenke-sys/gdc-mcp-server",
    "source": "github"
  },
  "version": "0.1.0",
  "packages": [
    {
      "registryType": "pypi",
      "identifier": "gdc-mcp-server",
      "version": "0.1.0",
      "transport": {
        "type": "stdio"
      },
      "environmentVariables": [
        {
          "description": "GDC API token for controlled-access data (optional for public data)",
          "isRequired": false,
          "format": "string",
          "isSecret": true,
          "name": "GDC_TOKEN"
        }
      ]
    }
  ]
}
```

**Important:**
- `name` must match the `mcp-name` in your README
- `packages[0].registryType` must be `"pypi"` for Python
- `packages[0].identifier` must match your PyPI package name
- `packages[0].version` must match your PyPI version

---

## Step 8: Authenticate with MCP Registry

Use GitHub authentication:

```powershell
mcp-publisher login github
```

You'll see:
```
Logging in with github...

To authenticate, please:
1. Go to: https://github.com/login/device
2. Enter code: ABCD-1234
3. Authorize this application
Waiting for authorization...
```

1. Visit the link
2. Enter the code
3. Authorize the application
4. Return to terminal - you should see:
   ```
   Successfully authenticated!
   ✓ Successfully logged in
   ```

---

## Step 9: Publish to MCP Registry

```powershell
mcp-publisher publish
```

You should see:
```
Publishing to https://registry.modelcontextprotocol.io...
✓ Successfully published
✓ Server io.github.devstephenke-sys/gdc-mcp-server version 0.1.0
```

---

## Step 10: Verify Publication

Search for your server:

```powershell
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.devstephenke-sys/gdc-mcp-server"
```

Or visit: https://registry.modelcontextprotocol.io/ and search for "gdc-mcp-server"

---

## Troubleshooting

### Error: "Package validation failed"
**Cause**: The `mcp-name` in README doesn't match the server name in `server.json`

**Solution**:
- Ensure README contains: `<!-- mcp-name: io.github.devstephenke-sys/gdc-mcp-server -->`
- Ensure `server.json` has: `"name": "io.github.devstephenke-sys/gdc-mcp-server"`
- Ensure they match exactly

### Error: "Package not found on PyPI"
**Cause**: Package not published to PyPI yet

**Solution**:
- Complete Step 5 (publish to PyPI) first
- Verify at https://pypi.org/project/gdc-mcp-server/

### Error: "Invalid or expired Registry JWT token"
**Cause**: Authentication expired

**Solution**:
```powershell
mcp-publisher login github
```

### Error: "You do not have permission to publish this server"
**Cause**: Authentication method doesn't match namespace

**Solution**:
- With GitHub auth, server name must start with `io.github.YOUR_USERNAME/`
- Your username is `devstephenke-sys`
- Server name should be: `io.github.devstephenke-sys/gdc-mcp-server`

### Error: "Invalid PyPI package name"
**Cause**: Package name doesn't exist on PyPI

**Solution**:
- Ensure you published to PyPI first
- Verify package name matches exactly (case-sensitive)
- Use `gdc-mcp-server` (with hyphens, not underscores)

---

## Next Steps After Publication

1. **Test Installation**:
   ```powershell
   pip install gdc-mcp-server
   ```

2. **Update Documentation**:
   - Add installation from PyPI to README
   - Update MCP Registry link in README

3. **Promote**:
   - Share on social media
   - Post in relevant communities (Reddit r/MCP, Discord)
   - Submit to Python package directories

4. **Monitor**:
   - Watch for issues on GitHub
   - Respond to user feedback
   - Update as needed

---

## Version Updates

When you release a new version:

1. Update version in `pyproject.toml`
2. Update version in `server.json`
3. Build and publish to PyPI:
   ```powershell
   python -m build
   twine upload dist/*
   ```
4. Publish to MCP Registry:
   ```powershell
   mcp-publisher publish
   ```

---

## Resources

- [MCP Registry Package Types](https://modelcontextprotocol.io/registry/package-types)
- [MCP Registry Quickstart](https://modelcontextprotocol.io/registry/quickstart)
- [PyPI Publishing Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [Twine Documentation](https://twine.readthedocs.io/)

---

## Current Status

✅ Repository prepared
✅ README with mcp-name verification
✅ pyproject.toml updated
✅ Ready for PyPI publication

⏳ **Next: Complete Steps 1-9 above**
