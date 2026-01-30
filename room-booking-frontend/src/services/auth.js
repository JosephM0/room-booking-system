const API_BASE = "http://127.0.0.1:8000/api/";

export function saveTokens({ access, refresh }) {
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
}

export function getAccessToken(){
    return localStorage.getItem("access_token");
}

export function getRefreshToken() {
    return localStorage.getItem("refresh_token");
}

export function clearTokens(){
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
}

export async function login(username, password) {
    const res = await fetch(API_BASE + "token/", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({ username, password }),
    });

    const data = await res.json();  

    if (!res.ok) throw data;        

    saveTokens(data);
    return data;
}


export async function refreshAccessTokens() {
    const refresh = getRefreshToken();
    if(!refresh) throw new Error("No refresh token");
    
    const res = await fetch(API_BASE + "token/refresh/", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({ refresh }),
    });

    if (!res.ok) throw new Error("Refresh failed");

    const data = await res.json();
    localStorage.setItem("access_token", data.access);
    return data.access;
}


export function authHeaders() {
    const token = getAccessToken();
    return token ? { Authorization: `Bearer ${token}`, "Content-Type": "application/json" } : { "Content-Type": "application/json" };
}