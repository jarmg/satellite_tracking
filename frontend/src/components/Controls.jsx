import fetch from 'node-fetch'
import React, { Component } from 'react'
import { Button } from 'rsuite';
import PropTypes from 'prop-types'


const topLevelDiv = 
{
  display:"grid",
  height: "100%",
  width: "100%",
  gridTemplateColumns: "1fr 1fr 1fr 1fr",
  gridTemplateRows: "7fr 2fr 1fr",
  gridTemplateAreas: `
    "out1 out1 out2 out2"
    "ctrl1 ctrl2 ctrl3 ctrl4"
    "run run stop stop"
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


const Controls = ({ jogging, onRun, onJog }) => {
    return (
      <div style={topLevelDiv}>
        <div style={arrows}>
          <Button 
            style={leftControl}
            onClick={() => onJog('az')}
            loading={jogging}
          >
              ← 
          </Button>

          <Button 
            style={rightControl}
            onClick={() => onJog('az')}
            loading={jogging}
          >
             → 
          </Button>

          <Button
            style={upControl}
            onClick={() => onJog('el')}
            loading={jogging}
          >
             ↑ 
          </Button>

          <Button
            style={downControl}
            onClick={() => onJog('el')}
            loading={jogging}
          >
            ↓
          </Button>
        </div>

        <Button
          style={{gridArea:"run"}}
          onClick={onRun}
          loading={jogging}
          color="green"
        >
          Run
        </Button>

        <Button
          style={{gridArea:"stop"}}
          loading={jogging}
          color="red"
        >
          Stop
        </Button>

      </div>
    )

}

Controls.propTypes = {
  jogging: PropTypes.bool.isRequired,
  onJog: PropTypes.func.isRequired,
  onRun: PropTypes.func.isRequired
}

export default Controls