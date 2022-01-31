const URL = 'http://127.0.0.1:5000';

const headers = {
    'Content-Type': 'application/json',
};

const getAuthHeaders = token => {
    return {
        ...headers,
        'Authorization': token
    }
}


const login = data => fetch(URL + "/login", {
    headers,
    method: 'POST',
    body: JSON.stringify(data),
}).then(res => {
    if (!res.ok) {
        return res.text().then(text => { throw new Error(text) })
    }
    else {
        return res.json();
    }
})

const handleResponse = res => {
    if (!res.ok) {
        return res.text().then(text => { throw new Error(text) })
    }
    else {
        return res.text();
    }
};

const getWatchedByFriends = token => fetch(URL + "/friends/watched", {
    headers: getAuthHeaders(token),
    method: 'GET',
}).then(handleResponse);


const getFreeSparql = query => fetch(URL, {
    headers,
    method: 'POST',
    body: JSON.stringify({query})
}).then(handleResponse);


const addFriend = (friendUsername, token) => fetch(URL + "/friends/add", {
    headers: getAuthHeaders(token),
    method: 'POST',
    body: JSON.stringify({friendUsername})
}).then(handleResponse);

const addMovie = (movieName, token) => fetch(URL + "/movies/watched/add", {
    headers: getAuthHeaders(token),
    method: 'POST',
    body: JSON.stringify({movieName})
}).then(handleResponse);

const searchMovie = (movieName) => fetch(URL + `/movies?name=${movieName}`, {
    headers,
    method: 'GET',
}).then(handleResponse);



export {
    login,
    getFreeSparql,
    addFriend,
    addMovie,
    searchMovie,
    getWatchedByFriends
}