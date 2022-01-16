import logo from './logo.svg';
import './App.css';
import { useState, useEffect } from 'react';

function SparqlPage() {

  const [result, setResult] = useState('Results will be shown here...');
  const [query, setQuery] = useState('');

  const sendQuery = () => {


    setResult(query);
  }

  return (
    <div>
      <div className='d-flex'>
        <div style={{width: '40%', paddingRight: '10px'}}>
          <textarea style={{height: '400px'}}  class="form-control" placeholder='Write a SPARQL query...' onChange={e => setQuery(e.target.value)}/>
          <button className='ml-auto btn btn-primary w-100' onClick={sendQuery}>Send</button>
        </div>
        <div>{result}</div>
      </div>
    </div>
  );
}



export default SparqlPage;
