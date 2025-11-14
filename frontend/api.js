const API_URL = "http://127.0.0.1:5000";

function _getToken() {
    return localStorage.getItem('token');
}

async function apiFetch(endpoint, method = "GET", data = null, token = null) {
    const authToken = token || _getToken();
    const headers = {};
    // Only set content-type when we have a JSON body
    if (data) headers["Content-Type"] = "application/json";
    if (authToken) headers["Authorization"] = `Bearer ${authToken}`;

    const options = { method, headers };
    if (data) options.body = JSON.stringify(data);

    const res = await fetch(`${API_URL}${endpoint}`, options);

    // No content
    if (res.status === 204) return null;

    const contentType = res.headers.get('content-type') || '';
    const isJson = contentType.includes('application/json');

    if (!res.ok) {
        if (isJson) {
            const err = await res.json();
            throw err;
        }
        const txt = await res.text();
        throw { message: txt };
    }

    if (isJson) return await res.json();
    return await res.text();
}
