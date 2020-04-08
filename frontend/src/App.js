import React from 'react';
import logo from './logo.svg';
import './App.css';
import { ImageViewer } from './components/ImageViewer.jsx';
import { PassSchedule } from './components/Schedule.jsx';
import { Controls } from './components/Controls.jsx';

const bodyContainer = {
  display: "grid",
  gridTemplateColumns: "25% 50% 25%"
}

function App() {
  return (
    <div className="App">
      <header className="Satellite Camera Interface">
        <p>My Token = {window.token}</p>
      </header>
      <body style={bodyContainer}>
        <div>
          <ImageViewer />
        </div>

        <div>
          <PassSchedule />
        </div>

        <div>
          <Controls />
        </div>
      </body>
    </div>
  );
}

export default App;
