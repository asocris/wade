import { useState, useEffect } from 'react';
import { addFriend, getWatchedByFriends } from './request-utils';
import { useAlert } from 'react-alert'

function FriendsPage({ auth, setResult }) {

  const [friendName, setFriendName] = useState('');
  const [watchedByFriends, setWatchedByFriends] = useState(null);
  const alert = useAlert();

  const isLoggedIn = !!auth.user;
  const addFriends = () => {
    addFriend(friendName, auth.token)
    .then(() => alert.success("User followed successfully."))
    .catch(e => alert.error("Error while following user."));
  }

  const searchWatchedByFriends = () => {
    getWatchedByFriends(auth.token)
      .then(res => setResult(res))
      .catch(err => alert.error("Error while searching movies.."));
  }

  return (
    <div>
      <div className='d-flex mt-3'>
        <input className='form-control' style={{ width: '25rem' }} placeholder="Enter a friend's username..." onChange={e => setFriendName(e.target.value)} disabled={!isLoggedIn} />
        <button className='btn btn-primary' style={{ marginLeft: '1px', width: '4.9rem' }} onClick={addFriends} disabled={friendName.length < 2 || !isLoggedIn}>Follow</button>
        <button className='ml-auto btn btn-primary' onClick={searchWatchedByFriends} disabled={!isLoggedIn}>Watched By Friends</button>
      </div>
    </div>
  );
}



export default FriendsPage;
