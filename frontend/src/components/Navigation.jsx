import React, { Component } from 'react';
import fetch from 'node-fetch';

import { Sidenav, Nav } from 'rsuite';




export class NavBar extends Component {
  constructor(props) {
    super(props)
    this.state = {}
  }


  render() {
    return (
      <div>
        <Sidenav
          onSelect={this.props.setScreen}
        >
          <Sidenav.Body>
            <Nav>
              <Nav.Item eventKey={this.props.screens.CONTROLS}> 
                Session runner
              </Nav.Item>
              <Nav.Item eventKey={this.props.screens.IMAGES}>
                Collected data
              </Nav.Item>
              <Nav.Item eventKey={this.props.screens.PASSES}>
                Upcoming passes
              </Nav.Item>
            </Nav>
          </Sidenav.Body>
       </Sidenav>
      </div>
    );
  }
}
