"""Core utilities and helpers for PyCodeMao."""

import asyncio
import logging
import time
from typing import Any, Callable, Dict, Optional, TypeVar, Union
from functools import wraps
import hashlib
import hmac
from urllib.parse import urlencode, quote

logger = logging.getLogger(__name__)

T = TypeVar('T')


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
) -> Callable:
    """Retry decorator with exponential backoff."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        logger.error(f"Failed after {max_attempts} attempts: {e}")
                        raise
                    
                    wait_time = delay * (backoff ** attempt)
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
            
            raise last_exception or RuntimeError("Unexpected retry loop exit")
        
        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        logger.error(f"Failed after {max_attempts} attempts: {e}")
                        raise
                    
                    wait_time = delay * (backoff ** attempt)
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
            
            raise last_exception or RuntimeError("Unexpected retry loop exit")
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator


def rate_limit(
    calls: int = 10,
    period: float = 1.0
) -> Callable:
    """Rate limiting decorator."""
    def decorator(func: Callable) -> Callable:
        call_times: list = []
        
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal call_times
            now = time.time()
            
            # Remove old calls outside the period
            call_times = [t for t in call_times if now - t < period]
            
            if len(call_times) >= calls:
                sleep_time = period - (now - call_times[0])
                logger.debug(f"Rate limit reached, sleeping for {sleep_time:.2f}s")
                await asyncio.sleep(sleep_time)
            
            call_times.append(now)
            return await func(*args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal call_times
            now = time.time()
            
            # Remove old calls outside the period
            call_times = [t for t in call_times if now - t < period]
            
            if len(call_times) >= calls:
                sleep_time = period - (now - call_times[0])
                logger.debug(f"Rate limit reached, sleeping for {sleep_time:.2f}s")
                time.sleep(sleep_time)
            
            call_times.append(now)
            return func(*args, **kwargs)
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator


def validate_email(email: str) -> bool:
    """Validate email address format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_username(username: str) -> bool:
    """Validate username format."""
    if len(username) < 3 or len(username) > 20:
        return False
    return username.replace('_', '').isalnum()


def generate_signature(
    method: str,
    path: str,
    params: Optional[Dict[str, Any]] = None,
    secret: Optional[str] = None
) -> str:
    """Generate API request signature."""
    if not secret:
        return ""
    
    # Sort parameters
    if params:
        sorted_params = sorted(params.items())
        param_string = urlencode(sorted_params)
    else:
        param_string = ""
    
    # Create signature string
    signature_string = f"{method.upper()}:{path}:{param_string}"
    
    # Generate HMAC signature
    signature = hmac.new(
        secret.encode('utf-8'),
        signature_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return signature


def safe_get(dictionary: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get value from nested dictionary."""
    keys = key.split('.')
    result = dictionary
    
    for k in keys:
        if isinstance(result, dict) and k in result:
            result = result[k]
        else:
            return default
    
    return result


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_timestamp(timestamp: Union[int, float]) -> str:
    """Format timestamp to human readable string."""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))


def parse_timestamp(timestamp_str: str) -> float:
    """Parse timestamp string to float."""
    try:
        return time.mktime(time.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S'))
    except ValueError:
        return time.mktime(time.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S'))


def chunk_list(lst: list, chunk_size: int) -> list:
    """Split list into chunks."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system usage."""
    import re
    # Remove or replace unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    # Ensure not empty
    if not filename:
        filename = 'unnamed'
    return filename


def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return filename.split('.')[-1].lower() if '.' in filename else ''