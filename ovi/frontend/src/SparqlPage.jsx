import './App.css';
import { useState, useEffect } from 'react';
import {getFreeSparql} from './request-utils';
import { useAlert } from 'react-alert'
import FriendsPage from './FriendsPage';
import MoviesPage from './MoviesPage';

function SparqlPage({auth}) {

  const [result, setResult] = useState('Results will be shown here...');
  const [query, setQuery] = useState('');
  const alert = useAlert();

  const sendQuery = () => {
    getFreeSparql(query)
    .then(res => setResult(res))
    .catch(() => alert.error("Invalid query."));
  }

  return (
    <div>
      <div className='d-flex'>
        <div style={{width: '40%', paddingRight: '10px'}}>
          <textarea style={{height: '400px'}}  className="form-control" placeholder='Write a SPARQL query...' onChange={e => setQuery(e.target.value)}/>
          <button className='ml-auto btn btn-primary w-100' onClick={sendQuery}>Send</button>
          <FriendsPage auth={auth} setResult={setResult}/>
          <MoviesPage auth={auth} setResult={setResult}/>

        </div>
        <pre style={{width: '60%', marginTop: '1rem'}}>{result}</pre>
      </div>
    </div>
  
  );
}



export default SparqlPage;
