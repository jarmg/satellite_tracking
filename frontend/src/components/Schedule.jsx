import React, { Component } from 'react';
import fetch from 'node-fetch'


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
        <button type="button" onClick={
          () => this.getUpcomingPasses()}>
          Load passes 
        </button>
        <table>
          <tr>
            <th> Satellite </th>
            <th align="right"> Time (PST) </th>
            <th align="right"> Elevation </th>
            <th align="right"> Azimuth (deg)</th>
            <th align="right"> Range (km)</th>
          </tr>
            {this.state.satPasses.map((pass) => (
              <tr key={pass.satellite + pass.time}>
                <td>{pass.satellite}</td>
                <td align="right"> {pass.time} </td>
                <td align="right">{pass.elevation}</td>
                <td align="right">{pass.azimuth}</td>
                <td align="right">{pass.range}</td>
              </tr>
            ))}
        </table>
      </div>
    );
  }
}
