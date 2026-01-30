import { getAccessToken, authHeaders, refreshAccessTokens } from "./auth";
const API_BASE = "http://127.0.0.1:8000/api/";

export async function fetchCurrentUser() {
    if (!getAccessToken()) {
        return null;
    }

    let res = await fetch(API_BASE + "users/me/", {
        headers: authHeaders(),
    });

    if (res.status === 401){
        try {
            await refreshAccessTokens();
        } catch(err) {
            return null;
        }

        res = await fetch(API_BASE + "users/me/", {
            headers: authHeaders(),
        })
    }

    if(!res.ok) {
        return null;
    }
    return await res.json();
}