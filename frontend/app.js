const API = "http://127.0.0.1:5000"; 
let token = localStorage.getItem("token");
let currentUser = JSON.parse(localStorage.getItem("user"));

if (token && currentUser) {
    showApp();
}

function showApp() {
    document.getElementById("authSection").style.display = "none";
    document.getElementById("appSection").style.display = "block";
    document.getElementById("welcome").innerText = `Bienvenido ${currentUser.username} (rol: ${currentUser.role})`;
    document.getElementById("adminPanel").style.display = currentUser.role === "admin" ? "block" : "none";
}

function showAuth() {
    document.getElementById("authSection").style.display = "block";
    document.getElementById("appSection").style.display = "none";
}

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const res = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    if (!data.access_token) {
        document.getElementById("authResult").innerText = data.message;
        return;
    }

    token = data.access_token;
    currentUser = data.user;

    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(currentUser));

    showApp();
}

async function registerUser() {
    const username = document.getElementById("newUsername").value;
    const password = document.getElementById("newPassword").value;
    const role = document.getElementById("newRole").value;

    const res = await fetch(`${API}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password, role })
    });

    const data = await res.json();
    document.getElementById("authResult").innerText = data.message || JSON.stringify(data);
}

function logout() {
    token = null;
    currentUser = null;
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    showAuth();
}

async function loadSeries() {
    const res = await fetch(`${API}/series/`);
    const data = await res.json();
    document.getElementById("seriesList").innerText = JSON.stringify(data, null, 2);
}

async function createSeries() {
    const title = document.getElementById("title").value;

    const res = await fetch(`${API}/series/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ title })
    });

    document.getElementById("actionResult").innerText = JSON.stringify(await res.json());
}

async function updateSeries() {
    const id = document.getElementById("editId").value;
    const title = document.getElementById("editTitle").value;

    const res = await fetch(`${API}/series/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ title })
    });

    document.getElementById("actionResult").innerText = JSON.stringify(await res.json());
}

async function deleteSeries() {
    const id = document.getElementById("deleteId").value;

    const res = await fetch(`${API}/series/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${token}` }
    });

    document.getElementById("actionResult").innerText = JSON.stringify(await res.json());
}
