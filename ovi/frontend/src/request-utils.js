export {
    login
}

const URL = 'http://127.0.0.1:5000';

const headers = {
    'Content-Type': 'application/json',
};


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