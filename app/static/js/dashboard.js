document.addEventListener('DOMContentLoaded', function() {
    const queryForm = document.getElementById('query-form');
    const responseContent = document.getElementById('response-content');
    const logoutBtn = document.getElementById('logout-btn');
    const userName = document.getElementById('user-name');
    
    // Check if token exists in localStorage
    const token = localStorage.getItem('accessToken');
    if (!token) {
        window.location.href = '/';
        return;
    }
    
    // Fetch user information
    fetchUserInfo(token);
    
    // Handle logout
    logoutBtn.addEventListener('click', function(e) {
        e.preventDefault();
        localStorage.removeItem('accessToken');
        window.location.href = '/';
    });
    
    // Function to fetch user information
    async function fetchUserInfo(token) {
        try {
            const response = await fetch('/api/users/me', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (response.ok) {
                const userData = await response.json();
                userName.textContent = userData.full_name || userData.username;
            } else {
                // If unauthorized, redirect to login
                if (response.status === 401) {
                    localStorage.removeItem('accessToken');
                    window.location.href = '/';
                }
            }
        } catch (error) {
            console.error('Error fetching user info:', error);
        }
    }
    
    // Handle query submission
    queryForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const query = document.getElementById('query').value;
        
        // Show loading state
        responseContent.innerHTML = '<p class="placeholder">Processing your query...</p>';
        
        try {
            const response = await fetch('/api/secure-query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    query: query
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Create a formatted response HTML
                let responseHTML = `<div class="ai-response">${formatResponse(data.response)}</div>`;
                
                // Display the response
                responseContent.innerHTML = responseHTML;
            } else {
                // Handle error
                responseContent.innerHTML = `<p class="error-message">${data.detail || 'An error occurred while processing your query.'}</p>`;
                
                // If unauthorized, redirect to login
                if (response.status === 401) {
                    localStorage.removeItem('accessToken');
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 2000);
                }
            }
        } catch (error) {
            console.error('Error:', error);
            responseContent.innerHTML = '<p class="error-message">An error occurred. Please try again later.</p>';
        }
    });
    
    // Helper function to format the response text with line breaks
    function formatResponse(text) {
        return text.replace(/\n/g, '<br>');
    }
});
