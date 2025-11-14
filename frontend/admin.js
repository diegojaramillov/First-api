async function createSeries() {
    const title = document.getElementById("new-series-title").value;
    try {
        await apiFetch("/series/", "POST", { title });
        loadSeries();
        document.getElementById("new-series-title").value = "";
    } catch (err) {
        showError(err.message || JSON.stringify(err));
    }
}

async function deleteSeries(seriesId) {
    if (!confirm('Are you sure you want to delete this series?')) return;
    try {
        await apiFetch(`/series/${seriesId}`, 'DELETE');
        loadSeries();
    } catch (err) {
        showError(err.message || JSON.stringify(err));
    }
}

async function editSeries(seriesId) {
    const newTitle = prompt('New title:');
    if (!newTitle) return;
    try {
        await apiFetch(`/series/${seriesId}`, 'PUT', { title: newTitle });
        loadSeries();
    } catch (err) {
        showError(err.message || JSON.stringify(err));
    }
}

function showError(msg){
    // simple non-blocking toast
    const existing = document.getElementById('app-toast');
    if(existing) existing.remove();
    const t = document.createElement('div');
    t.id = 'app-toast';
    t.innerText = msg;
    t.style.position='fixed';
    t.style.right='20px';
    t.style.bottom='20px';
    t.style.background='rgba(0,0,0,0.7)';
    t.style.color='white';
    t.style.padding='12px 16px';
    t.style.borderRadius='10px';
    t.style.zIndex=9999;
    document.body.appendChild(t);
    setTimeout(()=>t.remove(),3500);
}
