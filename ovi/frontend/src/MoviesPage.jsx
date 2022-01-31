import { useState, useEffect } from 'react';
import { addMovie, searchMovie } from './request-utils';
import { useAlert } from 'react-alert'

function MoviesPage({ auth, setResult }) {

  const [movieName, setMovieName] = useState('');
  const alert = useAlert();
  const isLoggedIn = !!auth.user;

  const addMovies = () => {
    addMovie(movieName, auth.token)
      .then(res => alert.success("Added to watched."))
      .catch(err => alert.error("Couldn't add to watched."));
  }

  const searchMovies = () => {
    searchMovie(movieName)
      .then(res => setResult(res))
      .catch(err => alert.error("Error while searching a movie.."));
  }

  

  return (
    <div>
      <div className='d-flex mt-3'>
        <input className='form-control' style={{ width: '25rem' }} placeholder="Enter a movie / TV show name..." onChange={e => setMovieName(e.target.value)}  />
        <button className='btn btn-primary' style={{ marginLeft: '1px' }} onClick={searchMovies}><i className="fa fa-search"></i></button>
        <button className='btn btn-primary' style={{ marginLeft: '1px' }} onClick={addMovies} disabled={movieName.length < 2 || !isLoggedIn}><i className="fa fa-plus"></i></button>

      </div>
    </div>
  );
}



export default MoviesPage;
