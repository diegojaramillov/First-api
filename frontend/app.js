function getToken() {
    return localStorage.getItem('token');
}

function getUserRole() {
    return localStorage.getItem('role');
}

function showLogin() {
    document.getElementById('auth-container').style.display = 'block';
    document.getElementById('home-container').style.display = 'none';
    setHeaderAuthState(false);
}

function showAdmin() {
    showHome();
    document.getElementById('admin-panel').style.display = 'block';
    setHeaderAuthState(true);
}

window.onload = () => {
    const token = getToken();
    const role = getUserRole();

    if (!token) {
        showLogin();
        return;
    }

    if (role === "admin") showAdmin();
    else showHome();
    // Attach ripple handlers to buttons
    attachRipples();
};

function setHeaderAuthState(loggedIn){
    const headerActions = document.querySelector('.header-actions');
    if(!headerActions) return;
    headerActions.style.display = loggedIn ? 'flex' : 'none';
}

function attachRipples(){
    document.querySelectorAll('button, .btn-icon').forEach(btn=>{
        btn.addEventListener('click', function(e){
            const rect = this.getBoundingClientRect();
            const r = document.createElement('span');
            r.className='ripple';
            const size = Math.max(rect.width, rect.height);
            r.style.width = r.style.height = size + 'px';
            r.style.left = (e.clientX - rect.left - size/2) + 'px';
            r.style.top = (e.clientY - rect.top - size/2) + 'px';
            this.appendChild(r);
            setTimeout(()=>{ r.remove(); }, 700);
        });
    });
}
