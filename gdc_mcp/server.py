"""GDC MCP Server - Main server implementation."""

import json
from typing import Any, Dict, List, Optional

from mcp.server import MCPServer

from gdc_mcp.client import GDCClient


# Initialize MCP server
mcp = MCPServer("gdc-mcp")


@mcp.tool()
async def get_status() -> str:
    """Get GDC API status and version information.

    Returns:
        JSON string with API status
    """
    async with GDCClient() as client:
        status = await client.get_status()
        return json.dumps(status, indent=2)


@mcp.tool()
async def search_projects(
    project_id: Optional[str] = None,
    program: Optional[str] = None,
    disease_type: Optional[str] = None,
    primary_site: Optional[str] = None,
    size: int = 10,
    from_: int = 0,
) -> str:
    """Search GDC projects (TCGA, TARGET, CPTAC, etc.).

    Args:
        project_id: Specific project ID (e.g., "TCGA-BRCA")
        program: Program name (e.g., "TCGA", "TARGET")
        disease_type: Disease type (e.g., "Breast Invasive Carcinoma")
        primary_site: Primary site (e.g., "Breast")
        size: Maximum number of results (default: 10)
        from_: Offset for pagination (default: 0)

    Returns:
        JSON string with project search results
    """
    filters = {"op": "and", "content": []}

    if project_id:
        filters["content"].append({"op": "in", "content": {"field": "project_id", "value": [project_id]}})
    if program:
        filters["content"].append({"op": "in", "content": {"field": "program.name", "value": [program]}})
    if disease_type:
        filters["content"].append({"op": "in", "content": {"field": "disease_type", "value": [disease_type]}})
    if primary_site:
        filters["content"].append({"op": "in", "content": {"field": "primary_site", "value": [primary_site]}})

    if not filters["content"]:
        filters = None

    async with GDCClient() as client:
        result = await client.search(
            endpoint="projects",
            filters=filters,
            size=size,
            from_=from_,
        )
        return json.dumps(result, indent=2)


@mcp.tool()
async def get_project_details(project_id: str) -> str:
    """Get detailed information about a specific GDC project.

    Args:
        project_id: Project ID (e.g., "TCGA-BRCA")

    Returns:
        JSON string with project details
    """
    async with GDCClient() as client:
        result = await client.get_by_id("projects", project_id)
        return json.dumps(result, indent=2)


@mcp.tool()
async def search_cases(
    project_id: Optional[str] = None,
    disease_type: Optional[str] = None,
    primary_site: Optional[str] = None,
    gender: Optional[str] = None,
    age_at_diagnosis_min: Optional[int] = None,
    age_at_diagnosis_max: Optional[int] = None,
    vital_status: Optional[str] = None,
    size: int = 10,
    from_: int = 0,
) -> str:
    """Search GDC cases (patients) with clinical filters.

    Args:
        project_id: Project ID to filter by
        disease_type: Disease type
        primary_site: Primary site
        gender: Gender (e.g., "male", "female")
        age_at_diagnosis_min: Minimum age at diagnosis in days
        age_at_diagnosis_max: Maximum age at diagnosis in days
        vital_status: Vital status (e.g., "Alive", "Dead")
        size: Maximum number of results (default: 10)
        from_: Offset for pagination (default: 0)

    Returns:
        JSON string with case search results
    """
    filters = {"op": "and", "content": []}

    if project_id:
        filters["content"].append({"op": "in", "content": {"field": "project.project_id", "value": [project_id]}})
    if disease_type:
        filters["content"].append({"op": "in", "content": {"field": "disease_type", "value": [disease_type]}})
    if primary_site:
        filters["content"].append({"op": "in", "content": {"field": "primary_site", "value": [primary_site]}})
    if gender:
        filters["content"].append({"op": "in", "content": {"field": "demographic.gender", "value": [gender]}})
    if vital_status:
        filters["content"].append({"op": "in", "content": {"field": "demographic.vital_status", "value": [vital_status]}})
    if age_at_diagnosis_min is not None:
        filters["content"].append({"op": ">=", "content": {"field": "demographic.days_to_birth", "value": -age_at_diagnosis_min}})
    if age_at_diagnosis_max is not None:
        filters["content"].append({"op": "<=", "content": {"field": "demographic.days_to_birth", "value": -age_at_diagnosis_max}})

    if not filters["content"]:
        filters = None

    async with GDCClient() as client:
        result = await client.search(
            endpoint="cases",
            filters=filters,
            size=size,
            from_=from_,
        )
        return json.dumps(result, indent=2)


@mcp.tool()
async def get_case_details(case_id: str) -> str:
    """Get detailed information about a specific case/patient.

    Args:
        case_id: Case UUID

    Returns:
        JSON string with case details including clinical data
    """
    async with GDCClient() as client:
        result = await client.get_by_id("cases", case_id)
        return json.dumps(result, indent=2)


@mcp.tool()
async def search_files(
    project_id: Optional[str] = None,
    case_id: Optional[str] = None,
    data_type: Optional[str] = None,
    experimental_strategy: Optional[str] = None,
    data_format: Optional[str] = None,
    workflow_type: Optional[str] = None,
    access: Optional[str] = None,
    size: int = 10,
    from_: int = 0,
) -> str:
    """Search GDC files (genomic data files).

    Args:
        project_id: Project ID to filter by
        case_id: Case UUID to filter by
        data_type: Data type (e.g., "Copy Number Variation", "Methylation", "Transcriptome Profiling")
        experimental_strategy: Experimental strategy (e.g., "WXS", "WGS", "RNA-Seq", "Methylation Array")
        data_format: File format (e.g., "MAF", "VCF", "BAM", "TXT")
        workflow_type: Analysis workflow type
        access: Access level ("open" or "controlled")
        size: Maximum number of results (default: 10)
        from_: Offset for pagination (default: 0)

    Returns:
        JSON string with file search results
    """
    filters = {"op": "and", "content": []}

    if project_id:
        filters["content"].append({"op": "in", "content": {"field": "cases.project.project_id", "value": [project_id]}})
    if case_id:
        filters["content"].append({"op": "in", "content": {"field": "cases.case_id", "value": [case_id]}})
    if data_type:
        filters["content"].append({"op": "in", "content": {"field": "data_type", "value": [data_type]}})
    if experimental_strategy:
        filters["content"].append({"op": "in", "content": {"field": "experimental_strategy", "value": [experimental_strategy]}})
    if data_format:
        filters["content"].append({"op": "in", "content": {"field": "data_format", "value": [data_format]}})
    if workflow_type:
        filters["content"].append({"op": "in", "content": {"field": "analysis.workflow_type", "value": [workflow_type]}})
    if access:
        filters["content"].append({"op": "in", "content": {"field": "access", "value": [access]}})

    if not filters["content"]:
        filters = None

    async with GDCClient() as client:
        result = await client.search(
            endpoint="files",
            filters=filters,
            size=size,
            from_=from_,
        )
        return json.dumps(result, indent=2)


@mcp.tool()
async def get_file_details(file_id: str) -> str:
    """Get detailed metadata for a specific file.

    Args:
        file_id: File UUID

    Returns:
        JSON string with file metadata
    """
    async with GDCClient() as client:
        result = await client.get_by_id("files", file_id)
        return json.dumps(result, indent=2)


@mcp.tool()
async def search_annotations(
    category: Optional[str] = None,
    classification: Optional[str] = None,
    notes: Optional[str] = None,
    size: int = 10,
    from_: int = 0,
) -> str:
    """Search GDC annotations (curated data annotations).

    Args:
        category: Annotation category
        classification: Classification
        notes: Search in notes field
        size: Maximum number of results (default: 10)
        from_: Offset for pagination (default: 0)

    Returns:
        JSON string with annotation search results
    """
    filters = {"op": "and", "content": []}

    if category:
        filters["content"].append({"op": "in", "content": {"field": "category", "value": [category]}})
    if classification:
        filters["content"].append({"op": "in", "content": {"field": "classification", "value": [classification]}})
    if notes:
        filters["content"].append({"op": "contains", "content": {"field": "notes", "value": notes}})

    if not filters["content"]:
        filters = None

    async with GDCClient() as client:
        result = await client.search(
            endpoint="annotations",
            filters=filters,
            size=size,
            from_=from_,
        )
        return json.dumps(result, indent=2)


@mcp.tool()
async def query_mutations(
    project_id: Optional[str] = None,
    gene_symbol: Optional[str] = None,
    variant_classification: Optional[str] = None,
    size: int = 10,
    from_: int = 0,
) -> str:
    """Query somatic mutations (SSMS) from GDC.

    Args:
        project_id: Project ID to filter by
        gene_symbol: Gene symbol (e.g., "TP53", "BRAF")
        variant_classification: Variant classification (e.g., "Missense_Mutation", "Nonsense_Mutation")
        size: Maximum number of results (default: 10)
        from_: Offset for pagination (default: 0)

    Returns:
        JSON string with somatic mutation data
    """
    filters = {"op": "and", "content": []}

    if project_id:
        filters["content"].append({"op": "in", "content": {"field": "cases.project.project_id", "value": [project_id]}})
    if gene_symbol:
        filters["content"].append({"op": "in", "content": {"field": "gene.symbol", "value": [gene_symbol]}})
    if variant_classification:
        filters["content"].append({"op": "in", "content": {"field": "consequence_type", "value": [variant_classification]}})

    if not filters["content"]:
        filters = None

    async with GDCClient() as client:
        result = await client.query_ssms(filters=filters)
        return json.dumps(result, indent=2)


@mcp.tool()
async def query_copy_number(
    project_id: Optional[str] = None,
    gene_symbol: Optional[str] = None,
    alteration_type: Optional[str] = None,
    size: int = 10,
    from_: int = 0,
) -> str:
    """Query copy number variations from GDC.

    Args:
        project_id: Project ID to filter by
        gene_symbol: Gene symbol
        alteration_type: Alteration type (e.g., "DELETION", "AMPLIFICATION")
        size: Maximum number of results (default: 10)
        from_: Offset for pagination (default: 0)

    Returns:
        JSON string with copy number variation data
    """
    filters = {"op": "and", "content": []}

    if project_id:
        filters["content"].append({"op": "in", "content": {"field": "cases.project.project_id", "value": [project_id]}})
    if gene_symbol:
        filters["content"].append({"op": "in", "content": {"field": "gene.symbol", "value": [gene_symbol]}})
    if alteration_type:
        filters["content"].append({"op": "in", "content": {"field": "alteration_type", "value": [alteration_type]}})

    if not filters["content"]:
        filters = None

    async with GDCClient() as client:
        result = await client.query_cnv(filters=filters)
        return json.dumps(result, indent=2)


@mcp.tool()
async def query_expression(
    project_id: Optional[str] = None,
    gene_symbol: Optional[str] = None,
    strategy: Optional[str] = None,
    size: int = 10,
    from_: int = 0,
) -> str:
    """Query gene expression data from GDC.

    Args:
        project_id: Project ID to filter by
        gene_symbol: Gene symbol
        strategy: Experimental strategy (e.g., "RNA-Seq")
        size: Maximum number of results (default: 10)
        from_: Offset for pagination (default: 0)

    Returns:
        JSON string with gene expression data
    """
    filters = {"op": "and", "content": []}

    if project_id:
        filters["content"].append({"op": "in", "content": {"field": "cases.project.project_id", "value": [project_id]}})
    if gene_symbol:
        filters["content"].append({"op": "in", "content": {"field": "gene.symbol", "value": [gene_symbol]}})
    if strategy:
        filters["content"].append({"op": "in", "content": {"field": "experimental_strategy", "value": [strategy]}})

    if not filters["content"]:
        filters = None

    async with GDCClient() as client:
        result = await client.query_expression(filters=filters)
        return json.dumps(result, indent=2)


@mcp.tool()
async def query_methylation(
    project_id: Optional[str] = None,
    platform: Optional[str] = None,
    size: int = 10,
    from_: int = 0,
) -> str:
    """Query DNA methylation data from GDC.

    Args:
        project_id: Project ID to filter by
        platform: Platform (e.g., "Illumina Human Methylation 450")
        size: Maximum number of results (default: 10)
        from_: Offset for pagination (default: 0)

    Returns:
        JSON string with methylation data
    """
    filters = {"op": "and", "content": []}

    if project_id:
        filters["content"].append({"op": "in", "content": {"field": "cases.project.project_id", "value": [project_id]}})
    if platform:
        filters["content"].append({"op": "in", "content": {"field": "platform", "value": [platform]}})

    if not filters["content"]:
        filters = None

    async with GDCClient() as client:
        result = await client.query_methylation(filters=filters)
        return json.dumps(result, indent=2)


@mcp.tool()
async def get_manifest(
    file_ids: Optional[List[str]] = None,
    project_id: Optional[str] = None,
    data_type: Optional[str] = None,
) -> str:
    """Generate a download manifest for GDC files.

    Args:
        file_ids: List of specific file UUIDs to include
        project_id: Project ID to include all files from a project
        data_type: Data type to filter files

    Returns:
        JSON string with manifest information for download
    """
    if file_ids:
        async with GDCClient() as client:
            result = await client.get_manifest(ids=file_ids)
            return json.dumps(result, indent=2)
    else:
        # Build filters for manifest
        filters = {"op": "and", "content": []}

        if project_id:
            filters["content"].append({"op": "in", "content": {"field": "cases.project.project_id", "value": [project_id]}})
        if data_type:
            filters["content"].append({"op": "in", "content": {"field": "data_type", "value": [data_type]}})

        if not filters["content"]:
            raise ValueError("Either file_ids or project_id/data_type must be provided")

        async with GDCClient() as client:
            result = await client.get_manifest(filters=filters)
            return json.dumps(result, indent=2)


@mcp.tool()
async def get_mapping(endpoint: str) -> str:
    """Get field mapping for a GDC endpoint.

    Useful for discovering available fields and their types.

    Args:
        endpoint: GDC endpoint (projects, cases, files, annotations)

    Returns:
        JSON string with field mapping
    """
    async with GDCClient() as client:
        result = await client.get_mapping(endpoint)
        return json.dumps(result, indent=2)


if __name__ == "__main__":
    # Run with: uv run mcp dev gdc_mcp/server.py
    # Or for production: uv run mcp run gdc_mcp/server.py --transport stdio
    pass
