import logo from './logo.svg';
import './App.css';
import { useState, useEffect } from 'react';
import SparqlPage from './SparqlPage';

function MainPage({ showLogin,
  setShowLogin,
  auth,
  setAuth,
  page }) {

  let pageToShow;
  if(page == 1) {
    pageToShow = <SparqlPage auth={auth}/>;
  }

  return (
    <div id="main-content">
      {pageToShow}
    </div>
  );
}



export default MainPage;
