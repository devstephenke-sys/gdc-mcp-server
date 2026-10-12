"""GDC API Client for interacting with NCI Genomic Data Commons."""

import httpx
from typing import Any, Dict, List, Optional


class GDCClient:
    """Client for the NCI Genomic Data Commons API."""

    BASE_URL = "https://api.gdc.cancer.gov"

    def __init__(self, token: Optional[str] = None):
        """Initialize GDC client.

        Args:
            token: Optional GDC authentication token for controlled-access data
        """
        self.token = token
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """Async context manager entry."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.token:
            headers["X-Auth-Token"] = self.token

        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers=headers,
            timeout=60.0,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the GDC API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON request body

        Returns:
            Response data as dictionary
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use async context manager.")

        response = await self._client.request(
            method=method,
            url=endpoint,
            params=params,
            json=json_data,
        )
        response.raise_for_status()
        return response.json()

    async def get_status(self) -> Dict[str, Any]:
        """Get GDC API status and version information."""
        return await self._request("GET", "/status")

    async def search(
        self,
        endpoint: str,
        filters: Optional[Dict[str, Any]] = None,
        fields: Optional[List[str]] = None,
        size: int = 10,
        from_: int = 0,
        sort: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Search GDC data using filters.

        Args:
            endpoint: GDC endpoint (projects, cases, files, annotations)
            filters: Query filters in GDC filter format
            fields: Fields to return in results
            size: Maximum number of results
            from_: Offset for pagination
            sort: Sort order (e.g., ["field:asc", "field:desc"])

        Returns:
            Search results with data and metadata
        """
        params = {
            "size": size,
            "from": from_,
            "pretty": True,
        }

        if fields:
            params["fields"] = ",".join(fields)
        if sort:
            params["sort"] = ",".join(sort)

        if filters:
            # POST request with filters in body
            return await self._request("POST", f"/{endpoint}", params=params, json_data=filters)
        else:
            # GET request without filters
            return await self._request("GET", f"/{endpoint}", params=params)

    async def get_by_id(
        self,
        endpoint: str,
        entity_id: str,
        fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Get a specific entity by ID.

        Args:
            endpoint: GDC endpoint (projects, cases, files, annotations)
            entity_id: Entity UUID or project ID
            fields: Fields to return

        Returns:
            Entity data
        """
        params = {"pretty": True}
        if fields:
            params["fields"] = ",".join(fields)

        return await self._request("GET", f"/{endpoint}/{entity_id}", params=params)

    async def get_mapping(self, endpoint: str) -> Dict[str, Any]:
        """Get field mapping for an endpoint.

        Args:
            endpoint: GDC endpoint

        Returns:
            Field mapping with available fields and their types
        """
        return await self._request("GET", f"/{endpoint}/_mapping")

    async def get_manifest(
        self,
        filters: Optional[Dict[str, Any]] = None,
        ids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Generate a download manifest.

        Args:
            filters: Query filters
            ids: List of file UUIDs

        Returns:
            Manifest with file download information
        """
        if ids:
            # Manifest from specific file IDs
            return await self._request("POST", "/manifest", json_data={"ids": ids})
        elif filters:
            # Manifest from filters
            return await self._request("POST", "/manifest", json_data=filters)
        else:
            raise ValueError("Either filters or ids must be provided")

    async def get_data(self, file_id: str) -> bytes:
        """Download a file from GDC.

        Args:
            file_id: File UUID

        Returns:
            File content as bytes
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use async context manager.")

        response = await self._client.get(f"/data/{file_id}")
        response.raise_for_status()
        return response.content

    async def query_ssms(
        self,
        filters: Dict[str, Any],
        expand: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Query somatic simple mutations (SSMS).

        Args:
            filters: Query filters
            expand: Fields to expand

        Returns:
            Somatic mutation data
        """
        params = {"pretty": True}
        if expand:
            params["expand"] = ",".join(expand)

        return await self._request("POST", "/ssms", params=params, json_data=filters)

    async def query_cnv(
        self,
        filters: Dict[str, Any],
        expand: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Query copy number variations.

        Args:
            filters: Query filters
            expand: Fields to expand

        Returns:
            Copy number variation data
        """
        params = {"pretty": True}
        if expand:
            params["expand"] = ",".join(expand)

        return await self._request("POST", "/cnv", params=params, json_data=filters)

    async def query_expression(
        self,
        filters: Dict[str, Any],
        expand: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Query gene expression data.

        Args:
            filters: Query filters
            expand: Fields to expand

        Returns:
            Gene expression data
        """
        params = {"pretty": True}
        if expand:
            params["expand"] = ",".join(expand)

        return await self._request("POST", "/expression", params=params, json_data=filters)

    async def query_methylation(
        self,
        filters: Dict[str, Any],
        expand: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Query DNA methylation data.

        Args:
            filters: Query filters
            expand: Fields to expand

        Returns:
            Methylation data
        """
        params = {"pretty": True}
        if expand:
            params["expand"] = ",".join(expand)

        return await self._request("POST", "/methylation", params=params, json_data=filters)
