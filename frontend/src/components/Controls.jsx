import fetch from 'node-fetch'
import React, { Component } from 'react'
import { Button } from 'rsuite';

const topLevelDiv = {
  display:"grid",
  height: "100%",
  width: "100%",
  gridTemplateColumns: "1fr 1fr 1fr 1fr",
  gridTemplateRows: "7fr 2fr 1fr",
  gridTemplateAreas: `
    "out1 out1 out2 out2"
    "ctrl1 ctrl2 ctrl3 ctrl4"
    "run run run run"
  `,
  gridGap: "20px",
}

const header = {
  gridArea: "head"
}

const arrows = {
  display: "grid",
  gridArea: "ctrl1",
  gridTemplateColumns: "50px 50px 50px",
  gridTemplateRows: "50px 50px",
  gridGap: "3px",
  gridTemplateAreas: `"c1 up c2" "left down right"`
}

const upControl = {gridArea:'up'}
const downControl = {gridArea:'down'}
const leftControl = {gridArea:'left'}
const rightControl = {gridArea:'right'}


export class Controls extends Component {
  constructor(props) {
    super(props)
    this.state = {
      distance: 10,
      is_jogging: false,
      is_running: false,
    }
  }


  onRun = async () => 
  {
    const response = await fetch("/run");
  }


  onJog = async (axis, multiplier) => 
  {

    this.setState({ready:false})
    const value = this.state.distance * multiplier
    var base = "/jog?azimuth="
    var query = ''
    if (axis == 'az')
    {
      query = base.concat(value, "&elevation=", 0)
    }
    if (axis == 'el')
    {
      query = base.concat(0, "&elevation=", value)
    }
    this.setState({is_jogging: true})
    const response = await fetch(query);
    console.log("done")
    this.setState({is_jogging: false})
  }

  onPick = image => 
  {
    this.setState({image})
  }

  render() {
    return (
      <div style={topLevelDiv}>
        <div style={arrows}>
          <Button 
            style={leftControl}
            onClick={() => this.onJog('az', -1)}
            loading={this.state.is_jogging}
          >
              ← 
          </Button>

          <Button 
            style={rightControl}
            onClick={() => this.onJog('az', 1)}
            loading={this.state.is_jogging}
          >
             → 
          </Button>

          <Button
            style={upControl}
            onClick={() => this.onJog('el', 1)}
            loading={this.state.is_jogging}
          >
             ↑ 
          </Button>

          <Button
            style={downControl}
            onClick={() => this.onJog('el', -1)}
            loading={this.state.is_jogging}
          >
            ↓
          </Button>
        </div>

        <Button
          style={{gridArea:"run"}}
          onClick={this.onRun()}
          loading={this.state.is_jogging}
        >
          Run
        </Button>
      </div>
    )
  }
}
