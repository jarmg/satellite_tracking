import React from 'react';
import { ImageViewer } from './components/ImageViewer.jsx';
import { PassSchedule } from './components/Schedule.jsx';
import { Controls } from './components/Controls.jsx';

import 'rsuite/lib/styles/index.less';

const rootContainer = {
  height: '100vh',
  display: "grid",
  gridTemplateColumns: "150px 1fr",
  gridTemplateRows: "150px 1fr 50px",
  gridGap: "10px",
  gridTemplateAreas: `
        "head head"
        "nav main"
        "nav footer"`,
}

const mainPanel = {
  background: 'grey',
  gridArea: 'main',
}

const navPanel = {
  background: 'purple',
  gridArea: 'nav',
}

const headerPanel = {
  background: 'pink',
  gridArea: 'head',
}

const footerPanel = {
  background: 'blue',
  gridArea: 'footer',
}

class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      main_screen: 'control'
    }
  }
  
  pickScreen = () => {
    switch(this.state.main_screen){
      case 'control':
        return <Controls />;
      case 'upcoming_passes':
        return <PassSchedule />;
      case 'images':
        return <ImageViewer/>;
    }}


  render(){
    return (
      <div style={rootContainer} className="App">
        <div style={headerPanel}>
        </div>
        <div style={mainPanel}>
          {this.pickScreen()}
        </div>
        <div style={navPanel}>
        </div>
        <div style={footerPanel}>
        </div>
      </div>
   );
  }
}

export default App;
