import { combineReducers } from 'redux'

import {JOG_MOUNT, START_RUN, MOUNT_CONNECTED, MOUNT_DISCONNECTED} from './actions'

const initialControlState = {
    jogging: false,
}

const initialSystemState = {
    mount_connected: false,
}



function systemState(state = initialSystemState, action) {
    switch (action.type) {
        case MOUNT_CONNECTED:
            return Object.assign({}, state, {
                mount_connected:  true
            })
        case MOUNT_DISCONNECTED:
            return Object.assign({}, state, {
                mount_connected: false
            }) 
        default:
            return state
    }
}

function controls(state = initialControlState, action) {
    switch (action.type) {
        case JOG_MOUNT:
            return Object.assign({}, state, {
                jogging: true,
                available: false
            })
        case START_RUN:
            return Object.assign({}, state, {
                running: true,
                available: false
            })
 
        default:
            return state
    }
}

const robot = combineReducers({
    controls,
    systemState
})

export default robot