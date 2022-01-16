import './App.css';
import { useState, useEffect } from 'react';

import MainPage from './MainPage';
import LoginForm from './LoginForm';

const initialAuth = { user: null, loading: false, error: false };

function App() {

  const [auth, setAuth] = useState(initialAuth);
  const [page, setPage] = useState(1);

  useEffect(() => {
    console.log(auth);
  }, [auth]);


  const logout = () => {
    setAuth(initialAuth);
  }


  return (
    <div id="page">
      <div style={{ height: '70px', width: '100%', display: 'flex', alignItems: 'center', padding:'10px' , paddingRight: '15px', paddingLeft: '15px'}} className='my-header'>
        <h3 title="OVI" style={{ height: '100%', fontFamily: 'Moo Lah Lah', fontSize: '2.25rem', backgroundColor: '#f52e2e', paddingLeft: '9px', paddingRight: '9px', textAlign: 'center', marginBottom: '0px', lineHeight: 'unset', cursor:'pointer'}} onClick={() => setPage(1)}>OVI</h3>
        <div style={{ marginLeft: 'auto', width: '200p', height: '100%', display: 'flex', alignItems: 'center' }}>
          {
            auth.user ?
              <div style={{ display: 'flex', alignItems: 'center' }}>
                Hi,
                <span style={{ color: '#f52e2e', fontWeight: '500', marginLeft: '5px' }}>
                  {auth.user.fullname}
                </span>
                <i className="material-icons ml-3" onClick={logout} title='Logout'>logout</i>
              </div>
              : <LoginForm auth={auth} setAuth={setAuth} />
          }
        </div>
      </div>
      <MainPage
        auth={auth}
        setAuth={auth}
        page={page}
      />
    </div>
  );
}

export default App;
