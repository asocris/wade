import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
import { login } from './request-utils';

function LoginForm({
    auth,
    setAuth }) {

    const [username, setUsername] = useState(null);
    const [password, setPassword] = useState(null);


    const onSubmit = e => {
        e.preventDefault();
        login({ username, password })
            .then(data => setAuth({
                user: {
                    username: data.username,
                    fullname: data.fullname
                },
                token: data.token
            }))
            .catch(e => console.log(e.message));
    }

    return (
        <>
            <form className="form-inline" style={{display:'flex', alignItems: 'center'}} onSubmit={onSubmit}>
                <div className="form-group">
                    <label htmlFor="staticEmail2" className="sr-only">Email</label>
                    <input type="text" className="form-control" id="staticEmail2" placeholder='Username' onChange={e => setUsername(e.target.value)} />
                </div>
                <div className="form-group mx-sm-3">
                    <label htmlFor="inputPassword2" className="sr-only">Password</label>
                    <input type="password" className="form-control" id="inputPassword2" placeholder="Password" onChange={e => setPassword(e.target.value)} />
                </div>
                <button type="submit" className="btn btn-primary"
                    disabled={!password || !username || password.length < 2 || username.length < 2}
                >Login</button>
            </form>
        </>
    );
}



export default LoginForm;
