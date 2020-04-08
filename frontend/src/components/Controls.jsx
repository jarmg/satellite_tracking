import fetch from 'node-fetch'
import React, { Component } from 'react'

const gallery_style = {
  height: '75vh',
  overflow: 'scroll'
}

export class Controls extends Component {
  constructor(props) {
    super(props)
    this.state = {
      ready: true,
      distance: 10
    }
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
      <div>
        <p> Controls </p>
        <button type="button" onClick={
          () => this.onJog('az', -1)}>
            ← 
        </button>

        <button type="button" onClick={
          () => this.onJog('az', 1)}>
           → 
        </button>

        <button type="button" onClick={
          () => this.onJog('el', 1)}>
           ↑ 
        </button>

        <button type="button" onClick={
          () => this.onJog('el', -1)}>
          ↓
        </button>
      </div>
    )
  }
}
