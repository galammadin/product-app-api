// Authentication and redirection functions

// Check if user is authenticated
function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/api/product/login/';
        return false;
    }
    return true;
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    window.location.href = '/api/product/login/';
}

// Handle 401 Unauthorized responses
function handleUnauthorized(response) {
    if (response.status === 401) {
        localStorage.removeItem('token');
        window.location.href = '/api/product/login/';
        return true;
    }
    return false;
}

// Get authentication headers
function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
        'Authorization': `Token ${token}`
    };
}

// Get authentication headers with content type
function getAuthHeadersWithContentType() {
    return {
        ...getAuthHeaders(),
        'Content-Type': 'application/json'
    };
}