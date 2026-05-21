"""Task status router - expose Celery task status for frontend polling
"""
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
}


@router.get("/{task_id}")
async def get_task_status(task_id: str):
    """Return Celery task status and result (if available)."""
    celery = get_celery_app()
    async_result = celery.AsyncResult(task_id)

    mapped_status = STATUS_MAP.get(async_result.status, async_result.status.lower())
    logger.info(f"Task {task_id} polled → Celery state={async_result.status!r}, mapped={mapped_status!r}")

    response = {
        "task_id": task_id,
        "status": mapped_status,
        "result": None,
        "error": None,
    }

    try:
        if async_result.status == 'SUCCESS':
            response["result"] = async_result.result
        elif async_result.status == 'FAILURE':
            res = async_result.result
            response["error"] = str(res)
    except Exception as e:
        response["error"] = str(e)

    return response
