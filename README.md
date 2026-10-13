# GDC MCP Server

Model Context Protocol (MCP) server for the [NCI Genomic Data Commons (GDC)](https://gdc.cancer.gov/) — enabling AI agents to query, search, and download cancer genomic data directly through natural language interactions.

<!-- mcp-name: io.github.devstephenke-sys/gdc-mcp-server -->

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)

## Overview

The GDC MCP Server provides programmatic access to the NCI Genomic Data Commons API, allowing AI assistants to:

- **Search Projects**: Query cancer research projects and studies
- **Explore Cases**: Access patient cases with clinical and molecular data
- **Retrieve Files**: Find and download genomic data files
- **Query Molecular Data**: Access somatic mutations, copy number variations, gene expression, and methylation data
- **Generate Manifests**: Create download manifests for bulk data retrieval
- **Download Data**: Directly download controlled-access data with authentication

## Features

### Core Capabilities

- ✅ **Project Search**: Query projects by disease, primary site, or study
- ✅ **Case Query**: Search patient cases with filters and sorting
- ✅ **File Discovery**: Find genomic data files by type, format, and metadata
- ✅ **Molecular Data Queries**:
  - Somatic Simple Mutations (SSMs)
  - Copy Number Variations (CNV)
  - Gene Expression (RNA-seq)
  - DNA Methylation
- ✅ **Manifest Generation**: Create bulk download manifests
- ✅ **Controlled Access**: Support for controlled-access data with token authentication
- ✅ **Async/Await**: Modern Python async patterns for efficient API calls

### Technical Highlights

- **Type Hints**: Full type annotations for better IDE support
- **Async/Await**: Non-blocking I/O for improved performance
- **Error Handling**: Comprehensive error handling with HTTP status code validation
- **Context Manager**: Automatic resource cleanup with async context managers
- **Flexible Filtering**: Support for complex GDC filter queries
- **Pagination**: Built-in support for paginated results

## Installation

### Prerequisites

- Python 3.9 or higher
- uv (recommended) or pip
- GDC API token (for controlled-access data, optional for public data)

### Setup

```bash
# Clone the repository
git clone https://github.com/devstephenke-sys/gdc-mcp-server.git
cd gdc-mcp-server

# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

### MCP Configuration

Add to your MCP client configuration (e.g., Claude Desktop, Cursor):

```json
{
  "mcpServers": {
    "gdc": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/gdc-mcp-server",
        "mcp",
        "run",
        "server.py"
      ],
      "env": {
        "GDC_TOKEN": "${env:GDC_TOKEN}"
      }
    }
  }
}
```

For controlled-access data, set the `GDC_TOKEN` environment variable with your GDC API token:

```bash
export GDC_TOKEN="your_gdc_token_here"
```

## Usage

### Basic Usage with MCP

Once configured, your AI assistant can interact with GDC data through natural language:

```
User: "Find all breast cancer projects in TCGA"
Assistant: [Queries GDC API and returns project list]

User: "Get somatic mutations for case TCGA-XX-XXXX"
Assistant: [Retrieves SSM data for the specified case]

User: "Download RNA-seq expression data for project TCGA-BRCA"
Assistant: [Generates manifest and downloads files]
```

### Python API Usage

```python
import asyncio
from gdc_mcp.client import GDCClient

async def main():
    async with GDCClient() as client:
        # Get API status
        status = await client.get_status()
        print(f"GDC API Status: {status}")

        # Search projects
        projects = await client.search(
            endpoint="projects",
            filters={
                "op": "in",
                "content": {
                    "field": "primary_site",
                    "value": ["Breast"]
                }
            }
        )
        print(f"Found {len(projects['data'])} breast cancer projects")

        # Get specific case
        case = await client.get_by_id("cases", "case-id")
        print(f"Case: {case}")

asyncio.run(main())
```

## Available Endpoints

### Core Endpoints

- `/status` - API status and version information
- `/projects` - Cancer research projects
- `/cases` - Patient cases with clinical data
- `/files` - Genomic data files
- `/annotations` - Clinical and molecular annotations

### Molecular Data Endpoints

- `/ssms` - Somatic simple mutations
- `/cnv` - Copy number variations
- `/expression` - Gene expression data
- `/methylation` - DNA methylation data

### Data Access

- `/manifest` - Generate download manifests
- `/data/{file_id}` - Download specific files

## Authentication

### Public Data

No authentication required for public datasets.

### Controlled-Access Data

For controlled-access data (e.g., certain genomic datasets):

1. Apply for access at [GDC Data Portal](https://portal.gdc.cancer.gov/)
2. Generate API token in your GDC profile
3. Set `GDC_TOKEN` environment variable or pass to client:

```python
client = GDCClient(token="your_gdc_token")
```

## Documentation

### GDC API Documentation

- [GDC API Portal](https://gdc.cancer.gov/api/)
- [GDC API Endpoints](https://docs.gdc.cancer.gov/api/)
- [GDC Filters](https://docs.gdc.cancer.gov/api/ Filters)
- [GDC Files and Metadata](https://docs.gdc.cancer.gov/Data_Download/)

### MCP Documentation

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Servers](https://github.com/modelcontextprotocol/servers)

## Examples

### Example 1: Search Breast Cancer Projects

```python
import asyncio
from gdc_mcp.client import GDCClient

async def search_breast_projects():
    async with GDCClient() as client:
        projects = await client.search(
            endpoint="projects",
            filters={
                "op": "in",
                "content": {
                    "field": "primary_site",
                    "value": ["Breast"]
                }
            },
            fields=["project_id", "name", "primary_site", "disease_type"]
        )
        return projects

asyncio.run(search_breast_projects())
```

### Example 2: Get Somatic Mutations

```python
async def get_mutations(case_id):
    async with GDCClient() as client:
        mutations = await client.query_ssms(
            filters={
                "op": "in",
                "content": {
                    "field": "cases.case_id",
                    "value": [case_id]
                }
            },
            expand=["genes"]
        )
        return mutations
```

### Example 3: Download Data Manifest

```python
async def create_manifest(project_id):
    async with GDCClient() as client:
        manifest = await client.get_manifest(
            filters={
                "op": "in",
                "content": {
                    "field": "cases.project.project_id",
                    "value": [project_id]
                }
            }
        )
        return manifest
```

## Development

### Running Tests

```bash
# Install test dependencies
uv sync --extra test

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=gdc_mcp
```

### Code Style

```bash
# Format code
uv run black gdc_mcp

# Lint code
uv run ruff check gdc_mcp

# Type checking
uv run mypy gdc_mcp
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [NCI Genomic Data Commons](https://gdc.cancer.gov/) for providing the API and data
- [Model Context Protocol](https://modelcontextprotocol.io/) for the MCP framework
- The cancer research community for making this data available

## Support

- [GDC Support Portal](https://support.gdc.cancer.gov/)
- [GDC Documentation](https://docs.gdc.cancer.gov/)
- [GDC User Forum](https://gdc.cancer.gov/)

## Citation

If you use this software in your research, please cite:

```bibtex
@software{gdc_mcp_server,
  title = {GDC MCP Server: Model Context Protocol Server for NCI Genomic Data Commons},
  author = {Stephen Mwangi},
  year = {2026},
  url = {https://github.com/devstephenke-sys/gdc-mcp-server}
}
```
