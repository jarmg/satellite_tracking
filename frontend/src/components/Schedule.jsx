import React, { Component } from 'react';
import fetch from 'node-fetch'

import { List, Button, FlexboxGrid } from 'rsuite';

 
const styleCenter = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '20px'
};

export class PassSchedule extends Component {
  constructor(props) {
    super(props)
    this.state = {
      satPasses: []
    }
  }

  
  getUpcomingPasses = async (index, count) => 
  {
    const response = await fetch('/upcoming_passes');
    const json = await response.json();
    console.log(json)
    this.setState({satPasses: json})
  }


  render() {
    return (
      <div>
        <Button type="button" onClick={
          () => this.getUpcomingPasses()}>
          Load passes 
        </Button>
        <div style={{padding: "10px", height: "60vh", overflow: "scroll"}}>
          <List>
            {this.state.satPasses.map((pass) => (
              <List.Item>
                <FlexboxGrid>
                  <FlexboxGrid.Item style={styleCenter} colspan={6}> 
                    {pass.satellite}
                  </FlexboxGrid.Item>

                  <FlexboxGrid.Item style={styleCenter} colspan={6}> 
                    {pass.time}
                  </FlexboxGrid.Item>

                  <FlexboxGrid.Item style={styleCenter} colspan={6}> 
                    {pass.azimuth}
                  </FlexboxGrid.Item>

                  <FlexboxGrid.Item style={styleCenter} colspan={6}> 
                    {pass.elevation}
                  </FlexboxGrid.Item>
              
                  <FlexboxGrid.Item style={styleCenter} colspan={6}> 
                    {pass.range}
                  </FlexboxGrid.Item>
                </FlexboxGrid>
              </List.Item>
            ))}
            ))}
            </List>
          </div>
        </div>
    );
  }
}
