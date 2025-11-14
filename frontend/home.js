function showHome() {
    document.getElementById("auth-container").style.display = "none";
    document.getElementById("home-container").style.display = "block";
    // Mostrar el nombre de usuario en el saludo si existe
    const username = localStorage.getItem('username') || localStorage.getItem('role') || 'user';
    document.getElementById("user-name").innerText = username;

    if (localStorage.getItem("role") === "admin") {
        document.getElementById("admin-panel").style.display = "block";
    }

    loadSeries();
}

async function loadSeries() {
    const seriesList = document.getElementById("series-list");
    seriesList.innerHTML = "";
    try {
        const series = await apiFetch("/series/");
        const role = localStorage.getItem('role');
        series.forEach(s => {
            const item = document.createElement("div");
            item.className = 'series-item';
            const title = document.createElement('span');
            title.innerText = `${s.id}: ${s.title}`;
            item.appendChild(title);

                        if (role === 'admin') {
                                const actions = document.createElement('div');
                                actions.style.display = 'flex';
                                actions.style.gap = '8px';

                                const editBtn = document.createElement('button');
                                editBtn.className = 'btn-icon';
                                editBtn.innerHTML = `
                                    <svg class="icon-sm" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25z" fill="currentColor"/>
                                        <path d="M20.71 7.04a1 1 0 000-1.41l-2.34-2.34a1 1 0 00-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" fill="currentColor"/>
                                    </svg>
                                    Edit`;
                                editBtn.onclick = () => editSeries(s.id);

                                const delBtn = document.createElement('button');
                                delBtn.className = 'btn-icon btn-danger';
                                delBtn.innerHTML = `
                                    <svg class="icon-sm" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M6 19a2 2 0 002 2h8a2 2 0 002-2V7H6v12z" fill="currentColor"/>
                                        <path d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" fill="currentColor"/>
                                    </svg>
                                    Delete`;
                                delBtn.onclick = () => deleteSeries(s.id);

                                actions.appendChild(editBtn);
                                actions.appendChild(delBtn);
                                item.appendChild(actions);
                        }

            seriesList.appendChild(item);
        });
    } catch (err) {
        console.error(err);
    }
}
