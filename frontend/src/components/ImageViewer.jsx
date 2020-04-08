import fetch from 'node-fetch'
import React, { Component } from 'react'
import ImagePicker from 'react-image-picker'
import 'react-image-picker/dist/index.css'


const gallery_style = {
  height: '75vh',
  overflow: 'scroll'
}

const tl_style = {}

export class ImageViewer extends Component {
  constructor(props) {
    super(props)
    this.state = {
      image: null,
      imageFiles: []
    }
  }


  loadImageList = async (index, count) => 
  {
    const response = await fetch('/image_list');
    const json = await response.json();
    console.log(json)
    this.setState({imageFiles: json})
  }

  onPick = image => 
  {
    this.setState({image})
  }

  render() {
    return (
      <div style={tl_style}>
        <p> Recent images </p>
        <button type="button" onClick={
          () => this.loadImageList(this.state.image_index, 20)}>
          Load Images
        </button>
        <button type="button"> Download Images (coming soon!) </button>
        <div style={gallery_style}>
          <ImagePicker 
            images={this.state.imageFiles.map(
              (imageData, i) => ({src: imageData.file_name, value: i}))}
            onPick={this.onPick}
          />
        </div>
      </div>
    )
  }
}
