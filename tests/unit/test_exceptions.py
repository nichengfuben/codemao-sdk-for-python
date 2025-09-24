"""Unit tests for exceptions."""

import pytest
from pycodemao.exceptions import (
    CodeMaoError,
    AuthenticationError,
    APIError,
    RateLimitError,
    ValidationError,
    ResourceNotFoundError,
    PermissionError,
    ServerError,
    NetworkError,
    TimeoutError
)


class TestCodeMaoError:
    """Test cases for base CodeMaoError."""
    
    def test_base_error_creation(self):
        """Test creating base error."""
        error = CodeMaoError("Test error message")
        
        assert str(error) == "Test error message"
        assert error.message == "Test error message"
        assert error.code is None
        assert error.details is None
    
    def test_base_error_with_code(self):
        """Test creating base error with code."""
        error = CodeMaoError("Test error", code="TEST_ERROR")
        
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.code == "TEST_ERROR"
    
    def test_base_error_with_details(self):
        """Test creating base error with details."""
        error = CodeMaoError("Test error", details={"key": "value"})
        
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.details == {"key": "value"}
    
    def test_base_error_with_all_fields(self):
        """Test creating base error with all fields."""
        error = CodeMaoError("Test error", code="TEST_ERROR", details={"key": "value"})
        
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.code == "TEST_ERROR"
        assert error.details == {"key": "value"}


class TestAuthenticationError:
    """Test cases for AuthenticationError."""
    
    def test_authentication_error_creation(self):
        """Test creating authentication error."""
        error = AuthenticationError("Invalid credentials")
        
        assert str(error) == "Invalid credentials"
        assert error.message == "Invalid credentials"
        assert isinstance(error, CodeMaoError)
    
    def test_authentication_error_with_code(self):
        """Test creating authentication error with code."""
        error = AuthenticationError("Invalid token", code="INVALID_TOKEN")
        
        assert str(error) == "Invalid token"
        assert error.code == "INVALID_TOKEN"
        assert isinstance(error, CodeMaoError)


class TestAPIError:
    """Test cases for APIError."""
    
    def test_api_error_creation(self):
        """Test creating API error."""
        error = APIError("API request failed", status_code=500)
        
        assert str(error) == "API request failed"
        assert error.message == "API request failed"
        assert error.status_code == 500
        assert isinstance(error, CodeMaoError)
    
    def test_api_error_without_status_code(self):
        """Test creating API error without status code."""
        error = APIError("API error")
        
        assert str(error) == "API error"
        assert error.status_code is None
        assert isinstance(error, CodeMaoError)


class TestRateLimitError:
    """Test cases for RateLimitError."""
    
    def test_rate_limit_error_creation(self):
        """Test creating rate limit error."""
        error = RateLimitError("Rate limit exceeded", retry_after=60)
        
        assert str(error) == "Rate limit exceeded"
        assert error.message == "Rate limit exceeded"
        assert error.retry_after == 60
        assert isinstance(error, CodeMaoError)
    
    def test_rate_limit_error_without_retry_after(self):
        """Test creating rate limit error without retry_after."""
        error = RateLimitError("Rate limited")
        
        assert str(error) == "Rate limited"
        assert error.retry_after is None
        assert isinstance(error, CodeMaoError)


class TestValidationError:
    """Test cases for ValidationError."""
    
    def test_validation_error_creation(self):
        """Test creating validation error."""
        error = ValidationError("Invalid input", field="username")
        
        assert str(error) == "Invalid input"
        assert error.message == "Invalid input"
        assert error.field == "username"
        assert isinstance(error, CodeMaoError)
    
    def test_validation_error_without_field(self):
        """Test creating validation error without field."""
        error = ValidationError("Validation failed")
        
        assert str(error) == "Validation failed"
        assert error.field is None
        assert isinstance(error, CodeMaoError)


class TestResourceNotFoundError:
    """Test cases for ResourceNotFoundError."""
    
    def test_resource_not_found_error_creation(self):
        """Test creating resource not found error."""
        error = ResourceNotFoundError("User not found", resource_type="User", resource_id="123")
        
        assert str(error) == "User not found"
        assert error.message == "User not found"
        assert error.resource_type == "User"
        assert error.resource_id == "123"
        assert isinstance(error, CodeMaoError)
    
    def test_resource_not_found_error_minimal(self):
        """Test creating resource not found error with minimal fields."""
        error = ResourceNotFoundError("Not found")
        
        assert str(error) == "Not found"
        assert error.resource_type is None
        assert error.resource_id is None
        assert isinstance(error, CodeMaoError)


class TestPermissionError:
    """Test cases for PermissionError."""
    
    def test_permission_error_creation(self):
        """Test creating permission error."""
        error = PermissionError("Access denied", required_permission="admin")
        
        assert str(error) == "Access denied"
        assert error.message == "Access denied"
        assert error.required_permission == "admin"
        assert isinstance(error, CodeMaoError)
    
    def test_permission_error_without_permission(self):
        """Test creating permission error without permission."""
        error = PermissionError("Permission denied")
        
        assert str(error) == "Permission denied"
        assert error.required_permission is None
        assert isinstance(error, CodeMaoError)


class TestServerError:
    """Test cases for ServerError."""
    
    def test_server_error_creation(self):
        """Test creating server error."""
        error = ServerError("Internal server error", status_code=500)
        
        assert str(error) == "Internal server error"
        assert error.message == "Internal server error"
        assert error.status_code == 500
        assert isinstance(error, CodeMaoError)
    
    def test_server_error_without_status_code(self):
        """Test creating server error without status code."""
        error = ServerError("Server error")
        
        assert str(error) == "Server error"
        assert error.status_code is None
        assert isinstance(error, CodeMaoError)


class TestNetworkError:
    """Test cases for NetworkError."""
    
    def test_network_error_creation(self):
        """Test creating network error."""
        error = NetworkError("Network connection failed", url="https://api.example.com")
        
        assert str(error) == "Network connection failed"
        assert error.message == "Network connection failed"
        assert error.url == "https://api.example.com"
        assert isinstance(error, CodeMaoError)
    
    def test_network_error_without_url(self):
        """Test creating network error without URL."""
        error = NetworkError("Connection failed")
        
        assert str(error) == "Connection failed"
        assert error.url is None
        assert isinstance(error, CodeMaoError)


class TestTimeoutError:
    """Test cases for TimeoutError."""
    
    def test_timeout_error_creation(self):
        """Test creating timeout error."""
        error = TimeoutError("Request timed out", timeout_seconds=30)
        
        assert str(error) == "Request timed out"
        assert error.message == "Request timed out"
        assert error.timeout_seconds == 30
        assert isinstance(error, CodeMaoError)
    
    def test_timeout_error_without_timeout(self):
        """Test creating timeout error without timeout."""
        error = TimeoutError("Timeout")
        
        assert str(error) == "Timeout"
        assert error.timeout_seconds is None
        assert isinstance(error, CodeMaoError)


class TestExceptionHierarchy:
    """Test exception hierarchy and inheritance."""
    
    def test_all_exceptions_inherit_from_base(self):
        """Test that all custom exceptions inherit from CodeMaoError."""
        exceptions = [
            AuthenticationError("test"),
            APIError("test"),
            RateLimitError("test"),
            ValidationError("test"),
            ResourceNotFoundError("test"),
            PermissionError("test"),
            ServerError("test"),
            NetworkError("test"),
            TimeoutError("test")
        ]
        
        for exception in exceptions:
            assert isinstance(exception, CodeMaoError)
    
    def test_exception_attributes(self):
        """Test that exceptions have required attributes."""
        error = CodeMaoError("Test message", code="TEST", details={"key": "value"})
        
        assert hasattr(error, 'message')
        assert hasattr(error, 'code')
        assert hasattr(error, 'details')
        assert error.message == "Test message"
        assert error.code == "TEST"
        assert error.details == {"key": "value"}
    
    def test_exception_string_representation(self):
        """Test string representation of exceptions."""
        error = CodeMaoError("Test message")
        
        assert str(error) == "Test message"
        assert repr(error) == "CodeMaoError('Test message')"
    
    def test_exception_with_none_values(self):
        """Test exceptions with None values."""
        error = CodeMaoError("Test message", code=None, details=None)
        
        assert error.code is None
        assert error.details is None


class TestExceptionUsage:
    """Test exception usage patterns."""
    
    def test_raising_and_catching_exceptions(self):
        """Test raising and catching exceptions."""
        with pytest.raises(AuthenticationError) as exc_info:
            raise AuthenticationError("Invalid credentials")
        
        assert str(exc_info.value) == "Invalid credentials"
        assert isinstance(exc_info.value, CodeMaoError)
    
    def test_catching_base_exception(self):
        """Test catching base exception type."""
        with pytest.raises(CodeMaoError) as exc_info:
            raise ValidationError("Validation failed")
        
        assert str(exc_info.value) == "Validation failed"
        assert isinstance(exc_info.value, ValidationError)
    
    def test_multiple_exception_catching(self):
        """Test catching multiple exception types."""
        with pytest.raises((AuthenticationError, PermissionError)) as exc_info:
            raise PermissionError("Access denied")
        
        assert str(exc_info.value) == "Access denied"
        assert isinstance(exc_info.value, PermissionError)