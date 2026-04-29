import os
import logging
from typing import Optional
from google.cloud import discoveryengine_v1 as discoveryengine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_website_datastore(
    project_id: str,
    location: str,
    data_store_id: str,
    query: str,
) -> Optional[str]:
    """
    Search a Vertex AI Website Data Store (Discovery Engine).
    """
    try:
        client = discoveryengine.SearchServiceClient()
        
        serving_config = client.serving_config_path(
            project=project_id,
            location=location,
            data_store=data_store_id,
            serving_config="default_search",
        )

        request = discoveryengine.SearchRequest(
            serving_config=serving_config,
            query=query,
            page_size=3,
        )

        response = client.search(request)
        
        results = []
        for result in response.results:
            data = result.document.derived_struct_data
            snippet = data.get("snippets", [{}])[0].get("snippet", "")
            if snippet:
                results.append(snippet)
        
        if not results:
            return None
            
        return "\n\n".join(results)
        
    except Exception as e:
        logger.error(f"Error searching Vertex AI Data Store: {e}")
        return None

def hierarchical_fitness_search(query: str) -> str:
    """
    Hierarchical search logic:
    1. Try Vertex AI Website Data Store (Trusted source).
    2. Fallback to a placeholder if results are empty.
    NOTE: The agent can use its own built-in tools for broader search if needed.
    """
    project_id = os.environ.get("VERTEX_PROJECT_ID")
    location = os.environ.get("VERTEX_LOCATION", "global")
    data_store_id = os.environ.get("VERTEX_DATA_STORE_ID")

    if project_id and data_store_id:
        logger.info(f"Attempting Vertex AI Data Store search for: {query}")
        va_results = search_website_datastore(project_id, location, data_store_id, query)
        
        if va_results:
            logger.info("Vertex AI results found. Using internal data store.")
            return f"SOURCE: Vertex AI Data Store (Internal Knowledge)\n\n{va_results}"

    # Fallback
    logger.info(f"Vertex AI results empty or unavailable for: {query}")
    return f"No specific internal records found for '{query}'. Please proceed with general knowledge or available search tools."
