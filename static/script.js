// Load network stats on page load
window.addEventListener('DOMContentLoaded', function() {
    loadNetworkStats();
});

// Allow Enter key to trigger search
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('userId');
    if (input) {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                analyzeUser();
            }
        });
    }
});

function loadNetworkStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            document.getElementById('network-stats').innerHTML = `
                📊 Network: <strong>${data.total_users.toLocaleString()}</strong> users • 
                <strong>${data.total_friendships.toLocaleString()}</strong> friendships • 
                Avg: <strong>${data.avg_friends_per_user}</strong> friends/user
            `;
        })
        .catch(error => {
            document.getElementById('network-stats').innerHTML = 
                '📊 Network statistics unavailable';
        });
}

function analyzeUser() {
    const userId = document.getElementById('userId').value;
    
    if (!userId || userId <= 0) {
        showError('Please enter a valid user ID');
        return;
    }
    
    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('error').style.display = 'none';
    document.getElementById('results').style.display = 'none';
    
    // Call API
    fetch('/api/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: parseInt(userId) })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.error || 'Unknown error');
            });
        }
        return response.json();
    })
    .then(data => {
        displayResults(data);
    })
    .catch(error => {
        showError(error.message);
    })
    .finally(() => {
        document.getElementById('loading').style.display = 'none';
    });
}

function showError(message) {
    const errorBox = document.getElementById('error');
    errorBox.textContent = '❌ ' + message;
    errorBox.style.display = 'block';
    document.getElementById('results').style.display = 'none';
}

function displayResults(data) {
    // User Info
    document.getElementById('userInfo').innerHTML = `
        <div class="info-item">
            <strong>User ID</strong>
            <span>${data.user_id}</span>
        </div>
        <div class="info-item">
            <strong>Current Friends</strong>
            <span>${data.current_friends.count}</span>
        </div>
        <div class="info-item">
            <strong>Recommendations</strong>
            <span>${data.recommended_friends.length}</span>
        </div>
    `;
    
    // Current Friends
    const friendsList = data.current_friends.list;
    if (friendsList.length > 0) {
        document.getElementById('currentFriends').innerHTML = `
            <div class="user-list">
                ${friendsList.map(id => `
                    <div class="user-chip">User ${id}</div>
                `).join('')}
            </div>
            ${data.current_friends.count > friendsList.length ? 
                `<p style="margin-top: 15px; color: #718096;">
                    ... and ${data.current_friends.count - friendsList.length} more
                </p>` : ''}
        `;
    } else {
        document.getElementById('currentFriends').innerHTML = 
            '<p style="color: #718096;">No friends found (isolated user)</p>';
    }
    
    // Recommended Friends
    if (data.recommended_friends.length > 0) {
        document.getElementById('recommendedFriends').innerHTML = `
            <div class="recommendation-list">
                ${data.recommended_friends.map((rec, index) => `
                    <div class="rec-item">
                        <div class="rec-info">
                            <strong>${index + 1}. User ${rec.user_id}</strong>
                            <small>${rec.reason}</small>
                        </div>
                        <div class="rec-badge">${rec.mutual_count} mutual</div>
                    </div>
                `).join('')}
            </div>
        `;
    } else {
        document.getElementById('recommendedFriends').innerHTML = 
            '<p style="color: #718096;">No recommendations available for this user</p>';
    }
    
    // Top Influencers
    if (data.top_influencers.length > 0) {
        document.getElementById('topInfluencers').innerHTML = `
            <div class="recommendation-list">
                ${data.top_influencers.map((inf, index) => `
                    <div class="rec-item">
                        <div class="rec-info">
                            <strong>${index + 1}. User ${inf.user_id}</strong>
                            <small>${inf.reason}</small>
                        </div>
                        <div class="rec-badge">🌟 ${inf.followers} friends</div>
                    </div>
                `).join('')}
            </div>
        `;
    } else {
        document.getElementById('topInfluencers').innerHTML = 
            '<p style="color: #718096;">No influencers found. User may need to add interests to profile.</p>';
    }
    
    // Show results
    document.getElementById('results').style.display = 'block';
    
    // Scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}
