import React, { useReducer, useState } from 'react';
import './App.css';

const formReducer = (state, event) => {
    return {
      ...state,
      [event.name]: event.value
    }
   }

function App() {
  const [formData, setFormData] = useReducer(formReducer, {});
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = event => {
    event.preventDefault();
    setSubmitting(true);
    console.log(formData)
    fetch('http://localhost:5000/createplaylist/lyrics', {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify(formData),
    })

    setTimeout(() => {
      setSubmitting(false);
    }, 3000);
  }

  const handleChange = event => {
    setFormData({
      name: event.target.name,
      value: event.target.value,
    });
  }

  return(
    <div className="wrapper">
      <h1>Spotification</h1>
      {submitting &&
       <div>
         You are submitting the following:
         <ul>
           {Object.entries(formData).map(([name, value]) => (
             <li key={name}><strong>{name}</strong>:{value.toString()}</li>
           ))}
         </ul>
       </div>
      }
      <form onSubmit={handleSubmit} action="http://127.0.0.1:5000/createplaylist/lyrics" method="post">
        <fieldset>
          <label>
            <p>Track Name</p>
            <input name="track_name" onChange={handleChange}/>
          </label>
        </fieldset>
        <fieldset>
          <label>
            <p>Artist Name</p>
            <input name="artist_name" onChange={handleChange}/>
          </label>
        </fieldset>
        <fieldset>
          <label>
            <p>Number of Tracks in New Playlist</p>
            <input type="number" name="num_tracks" onChange={handleChange} step="1"/>
          </label>
        </fieldset>
        <button type="submit">Submit</button>
      </form>
    </div>
  )
}

export default App;