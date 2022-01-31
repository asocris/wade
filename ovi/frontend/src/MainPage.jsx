import SparqlPage from './SparqlPage';
import MoviesPage from './MoviesPage';
import FriendsPage from './FriendsPage';
import AboutPage from './AboutPage';

function MainPage({ showLogin,
  setShowLogin,
  auth,
  setAuth,
  page }) {

  let pageToShow;
  if(page === 1) {
    pageToShow = <SparqlPage auth={auth}/>;
  }

  if(page === 2) {
    pageToShow = <MoviesPage auth={auth}/>
  }

  if(page === 3) {
    pageToShow = <FriendsPage auth={auth} />
  }

  if(page === 4) {
    pageToShow = <AboutPage/>
  }

  return (
    <div id="main-content">
      {pageToShow}
    </div>
  );
}



export default MainPage;
