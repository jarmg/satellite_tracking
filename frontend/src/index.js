import React from 'react';
import ReactDOM from 'react-dom';
import { createStore, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import { Provider } from 'react-redux'

import App from './App';
import robot from './reducers'
import * as serviceWorker from './serviceWorker';

import './index.css';
import 'rsuite/dist/styles/rsuite-default.css';

const store = createStore(robot, applyMiddleware(thunk))

const unsubscribe = store.subscribe(() =>
  console.log(store.getState()))

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.register();
