"""Task status router — expose Celery task status for frontend polling."""
import logging

from fastapi import APIRouter
from core.celery_app import get_celery_app

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

STATUS_MAP = {
    'PENDING': 'pending',
    'STARTED': 'in_progress',
    'SUCCESS': 'completed',
    'FAILURE': 'failed',
    'RETRY': 'retrying',
    'REVOKED': 'cancelled',
    'PROGRESS': 'in_progress',
}


@router.get("/{task_id}")
async def get_task_status(task_id: str):
    """Return Celery task status, result, and progress metadata."""
    celery = get_celery_app()
    async_result = celery.AsyncResult(task_id)

    mapped_status = STATUS_MAP.get(async_result.status, async_result.status.lower())

    response = {
        "task_id": task_id,
        "status": mapped_status,
        "result": None,
        "error": None,
    }

    try:
        if async_result.status == 'PROGRESS':
            response["result"] = async_result.result or {}
        elif async_result.status == 'SUCCESS':
            response["result"] = async_result.result
        elif async_result.status == 'FAILURE':
            response["error"] = str(async_result.result)
    except Exception as e:
        response["error"] = str(e)

    return response
