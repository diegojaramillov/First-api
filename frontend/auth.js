async function register() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const role = document.getElementById("role").value;

    try {
        await apiFetch("/auth/register", "POST", {username, password, role});
        alert("Usuario registrado, ahora haz login");
    } catch (err) {
        alert(err.message || JSON.stringify(err));
    }
}

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const data = await apiFetch("/auth/login", "POST", {username, password});
        localStorage.setItem("token", data.access_token);
        // backend returns user inside data.user
        const role = data.user && data.user.role ? data.user.role : 'user';
        const returnedUsername = data.user && data.user.username ? data.user.username : '';
        localStorage.setItem("role", role);
        localStorage.setItem("username", returnedUsername);
        showHome();
    } catch (err) {
        alert(err.message || JSON.stringify(err));
    }
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    document.getElementById("auth-container").style.display = "block";
    document.getElementById("home-container").style.display = "none";
}
