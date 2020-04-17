import React from 'react';

import { ImageViewer } from './components/ImageViewer.jsx';
import { PassSchedule } from './components/Schedule.jsx';
import Controls from './containers/SystemControl';
import { NavBar } from './components/Navigation.jsx';


const rootContainer = {
  height: '100vh',
  display: "grid",
  padding: "15px",
  background: "black",
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
  overflow: "scroll",
  padding: "35px",
  borderRadius: "5px",
}

const navPanel = {
  background: 'purple',
  gridArea: 'nav',
  borderRadius: "5px",
}

const headerPanel = {
  background: 'pink',
  gridArea: 'head',
  borderRadius: "5px",
}

const footerPanel = {
  background: 'blue',
  gridArea: 'footer',
  borderRadius: "5px",
}

const screens = {
  CONTROLS: "controls",
  PASSES: "upcoming_passes",
  IMAGES: "images"
}

class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      main_screen: screens.CONTROLS
    }
  }

  pickScreen = () => {
    switch(this.state.main_screen){
      case screens.CONTROLS:
        return <Controls/>;
      case screens.PASSES:
        return <PassSchedule />;
      case screens.IMAGES:
        return <ImageViewer/>;
    }}

  setScreen = key => {
    console.log("received " + key); 
    this.setState({main_screen: key})
  }

  render(){
    return (
      <div style={rootContainer} className="App">
        <div style={headerPanel}>
        </div>
        <div style={mainPanel}>
          {this.pickScreen()}
        </div>
        <div style={navPanel}>
          <NavBar 
            screens={screens}
            setScreen={this.setScreen}
          />
        </div>
        <div style={footerPanel}>
        </div>
      </div>
   );
  }
}

export default App;
