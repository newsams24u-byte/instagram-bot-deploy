// ======================== GLOBAL STATE ========================

let currentEditingPostId = null;
let sortable = null;

// ======================== INITIALIZATION ========================

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Setup event listeners
    setupTabButtons();
    setupActionButtons();
    setupModalButtons();
    setupSortable();
    
    // Load initial data
    loadPosts();
    loadStats();
    
    // Auto-refresh every 30 seconds
    setInterval(loadPosts, 30000);
    setInterval(loadStats, 60000);
}

// ======================== TAB SYSTEM ========================

function setupTabButtons() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    // Update buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Update panes
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    document.getElementById(tabName).classList.add('active');
    
    // Load appropriate data
    if (tabName === 'history') {
        loadHistory();
    }
}

// ======================== LOAD POSTS ========================

function loadPosts() {
    showLoading();
    
    fetch('/api/posts')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayPosts(data.posts);
            }
        })
        .catch(error => console.error('Error loading posts:', error))
        .finally(() => hideLoading());
}

function displayPosts(posts) {
    const container = document.getElementById('posts-list');
    const emptyState = document.getElementById('no-posts');
    
    if (posts.length === 0) {
        container.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    container.innerHTML = posts.map(post => createPostCard(post)).join('');
    
    // Reattach event listeners
    attachPostCardListeners();
    
    // Reinitialize sortable
    if (sortable) sortable.destroy();
    setupSortable();
}

function createPostCard(post) {
    const timeUntilApprove = post.time_until_auto_approve;
    const minutes = Math.floor(timeUntilApprove / 60);
    const seconds = timeUntilApprove % 60;
    
    let autoApproveHtml = '';
    if (post.status === 'pending' && timeUntilApprove > 0) {
        autoApproveHtml = `
            <div class="auto-approve-timer">
                ⏱️ Auto-approve in ${minutes}m ${seconds}s
            </div>
        `;
    }
    
    return `
        <div class="post-card" data-post-id="${post.id}">
            <img src="${post.image_path}" alt="Post" class="post-image">
            <div class="post-body">
                <span class="post-type">${post.content_type.toUpperCase()}</span>
                <span class="post-status ${post.status}">${post.status.toUpperCase()}</span>
                ${autoApproveHtml}
                <p class="post-caption">${escapeHtml(post.caption)}</p>
                <p class="post-meta">
                    📅 ${formatDate(post.created_at)}
                </p>
                <div class="post-actions">
                    ${getPostActions(post)}
                </div>
            </div>
        </div>
    `;
}

function getPostActions(post) {
    if (post.status === 'pending') {
        return `
            <button class="btn btn-primary btn-edit" onclick="openEditModal(${post.id})">✏️ Edit</button>
            <button class="btn btn-success btn-approve" onclick="approvePost(${post.id})">✅ Approve</button>
            <button class="btn btn-danger btn-reject" onclick="rejectPost(${post.id})">❌ Reject</button>
        `;
    } else if (post.status === 'approved') {
        return `
            <button class="btn btn-warning btn-post" onclick="postToInstagram(${post.id})">📤 Post Now</button>
            <button class="btn btn-secondary" onclick="openEditModal(${post.id})">✏️ Edit</button>
        `;
    } else if (post.status === 'posted') {
        return `<span style="color: var(--text-light);">Posted ✅</span>`;
    } else if (post.status === 'rejected') {
        return `<span style="color: var(--text-light);">Rejected ❌</span>`;
    }
}

// ======================== LOAD HISTORY ========================

function loadHistory() {
    showLoading();
    
    fetch('/api/posts/all?limit=20')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const postedPosts = data.posts.filter(p => p.status === 'posted');
                displayHistory(postedPosts);
            }
        })
        .catch(error => console.error('Error loading history:', error))
        .finally(() => hideLoading());
}

function displayHistory(posts) {
    const container = document.getElementById('history-list');
    const emptyState = document.getElementById('no-history');
    
    if (posts.length === 0) {
        container.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    container.innerHTML = posts.map(post => `
        <div class="post-card">
            <img src="${post.image_path}" alt="Post" class="post-image">
            <div class="post-body">
                <span class="post-type">${post.content_type.toUpperCase()}</span>
                <p class="post-caption">${escapeHtml(post.caption)}</p>
                <p class="post-meta">
                    📅 Posted: ${formatDate(post.posted_at)}
                </p>
            </div>
        </div>
    `).join('');
}

// ======================== EDIT MODAL ========================

function openEditModal(postId) {
    currentEditingPostId = postId;
    
    const postCard = document.querySelector(`[data-post-id="${postId}"]`);
    const image = postCard.querySelector('.post-image').src;
    const caption = postCard.querySelector('.post-caption').textContent;
    
    document.getElementById('modal-image').src = image;
    document.getElementById('modal-caption').value = caption;
    updateCharCount();
    
    document.getElementById('edit-modal').classList.add('active');
}

function setupModalButtons() {
    document.querySelector('.close-btn').addEventListener('click', closeEditModal);
    document.getElementById('modal-cancel').addEventListener('click', closeEditModal);
    document.getElementById('modal-save').addEventListener('click', saveCaption);
    
    document.getElementById('modal-caption').addEventListener('input', updateCharCount);
}

function closeEditModal() {
    document.getElementById('edit-modal').classList.remove('active');
    currentEditingPostId = null;
}

function updateCharCount() {
    const textarea = document.getElementById('modal-caption');
    const count = textarea.value.length;
    document.getElementById('char-counter').textContent = count;
}

function saveCaption() {
    if (!currentEditingPostId) return;
    
    const newCaption = document.getElementById('modal-caption').value;
    
    showLoading();
    
    fetch(`/api/posts/${currentEditingPostId}/caption`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ caption: newCaption })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                closeEditModal();
                loadPosts();
                showNotification('Caption updated successfully!', 'success');
            } else {
                showNotification('Failed to update caption', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error updating caption', 'error');
        })
        .finally(() => hideLoading());
}

// ======================== POST ACTIONS ========================

function approvePost(postId) {
    showLoading();
    
    fetch(`/api/posts/${postId}/approve`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ caption: null })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadPosts();
                loadStats();
                showNotification('Post approved! ✅', 'success');
            }
        })
        .catch(error => console.error('Error:', error))
        .finally(() => hideLoading());
}

function rejectPost(postId) {
    if (confirm('Are you sure you want to reject this post?')) {
        showLoading();
        
        fetch(`/api/posts/${postId}/reject`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    loadPosts();
                    loadStats();
                    showNotification('Post rejected ❌', 'success');
                }
            })
            .catch(error => console.error('Error:', error))
            .finally(() => hideLoading());
    }
}

function postToInstagram(postId) {
    if (confirm('Post this to Instagram now?')) {
        showLoading();
        
        fetch(`/api/posts/${postId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    loadPosts();
                    loadStats();
                    showNotification('Posted to Instagram! 📸', 'success');
                } else {
                    showNotification('Failed to post to Instagram', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error posting to Instagram', 'error');
            })
            .finally(() => hideLoading());
    }
}

// ======================== SORTABLE ========================

function setupSortable() {
    const container = document.getElementById('posts-list');
    
    if (container.children.length === 0) return;
    
    sortable = Sortable.create(container, {
        animation: 150,
        ghostClass: 'sortable-ghost',
        onEnd: function(evt) {
            savePostOrder();
        }
    });
}

function savePostOrder() {
    const postCards = document.querySelectorAll('[data-post-id]');
    const postIds = Array.from(postCards).map(card => parseInt(card.getAttribute('data-post-id')));
    
    fetch('/api/posts/reorder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ post_ids: postIds })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Post order saved! 📋', 'success');
            }
        })
        .catch(error => console.error('Error:', error));
}

// ======================== STATISTICS ========================

function loadStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateStats(data.stats);
            }
        })
        .catch(error => console.error('Error loading stats:', error));
}

function updateStats(stats) {
    document.querySelector('.pending-count').textContent = stats.pending;
    document.querySelector('.approved-count').textContent = stats.approved;
    document.querySelector('.posted-count').textContent = stats.posted;
    document.querySelector('.rejected-count').textContent = stats.rejected;
}

// ======================== ACTION BUTTONS ========================

function setupActionButtons() {
    document.getElementById('refresh-btn').addEventListener('click', loadPosts);
    document.getElementById('refresh-history').addEventListener('click', loadHistory);
    document.getElementById('auto-post-all').addEventListener('click', postAllApproved);
}

function postAllApproved() {
    if (confirm('Post all approved posts to Instagram?')) {
        showLoading();
        
        const approvedCards = document.querySelectorAll('[data-post-id]');
        const approvedIds = [];
        
        approvedCards.forEach(card => {
            const statusSpan = card.querySelector('.post-status');
            if (statusSpan && statusSpan.textContent.includes('APPROVED')) {
                approvedIds.push(parseInt(card.getAttribute('data-post-id')));
            }
        });
        
        Promise.all(
            approvedIds.map(id => 
                fetch(`/api/posts/${id}`, { method: 'POST' })
                    .then(r => r.json())
            )
        )
            .then(() => {
                loadPosts();
                loadStats();
                showNotification('All approved posts posted! 📸', 'success');
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error posting to Instagram', 'error');
            })
            .finally(() => hideLoading());
    }
}

// ======================== UTILITIES ========================

function showLoading() {
    document.getElementById('loading').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function attachPostCardListeners() {
    // Already handled by onclick attributes
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function formatDate(isoDate) {
    const date = new Date(isoDate);
    return date.toLocaleString();
}

function showNotification(message, type) {
    // Simple notification (can be enhanced with a toast library)
    console.log(`[${type.toUpperCase()}] ${message}`);
    // Could add a visual toast here
}

// Auto-refresh posts every 30 seconds
setInterval(() => {
    if (document.querySelector('.tab-btn.active').getAttribute('data-tab') === 'pending') {
        loadPosts();
        loadStats();
    }
}, 30000);
