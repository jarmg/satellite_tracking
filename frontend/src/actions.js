import io from 'socket.io-client';

var socket = io();

/*
socket.on('connect', function() {
    window.setInterval(function() {
      socket.emit('get_system_status')
    }, 3000)
});

socket.on('system_status', function(status_data) {
    dispatchEvent(updateSystemStatus(status_data))
});
*/


// Control Actions
export const JOG_MOUNT = "JOG_MOUNT"
export const START_RUN = "START_RUN"
export const LOAD_IMAGES = "LOAD_IMAGES"
export const LOAD_PASSES = "LOAD_PASSES"

// System State Actions
export const MOUNT_CONNECTED = "MOUNT_CONNECTED"
export const MOUNT_DISCONNECTED = "MOUNT_DISCONNECTED"
export const SYSTEM_STATUS = "SYSTEM_STATUS"

// Action creators
export function jogMount(axis, degrees) {
    socket.emit(JOG_MOUNT, {"axis": axis, "value": degrees})
    return {type: JOG_MOUNT}
}

export function runObservations() {
    return {type: START_RUN}
}

export function updateSystemStatus(status_response) {
    const status = JSON(status_response)
    if (status.mount_connected){
        return {type: MOUNT_CONNECTED}
    }
    return {type: MOUNT_DISCONNECTED}
}