import fetch from 'node-fetch'
import React, { Component } from 'react'
import { Button } from 'rsuite';

const topLevelDiv = {
  display:"grid",
  height: "100%",
  width: "100%",
  border: "20px",
  margin: "20px",
  gridTemplateColumns: "1fr 3fr 3fr 2fr",
  gridTemplateRows: "1fr 7fr 2fr",
  gridTemplateAreas: `
    "head head head head"
    "out1 out1 out2 out2"
    "ctrl1 ctrl2 ctrl3 ctrl4"
  `
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
      ready: true,
      distance: 10
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
    const response = await fetch(query);
    this.setState({ready: true})
  }

  onPick = image => 
  {
    this.setState({image})
  }

  render() {
    return (
      <div style={topLevelDiv}>
        <p style={header}> Controls </p>
        <div style={arrows}>
          <Button style={leftControl} onClick={
            () => this.onJog('az', -1)}>
              ← 
          </Button>

          <Button style={rightControl} onClick={
            () => this.onJog('az', 1)}>
             → 
          </Button>

          <Button style={upControl} onClick={
            () => this.onJog('el', 1)}>
             ↑ 
          </Button>

          <Button style={downControl} onClick={
            () => this.onJog('el', -1)}>
            ↓
          </Button>
        </div>

        <Button style={{gridArea:"ctrl2"}} onClick={
          this.onRun()}>
          Run
        </Button>
      </div>
    )
  }
}
