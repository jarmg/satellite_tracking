import { connect } from 'react-redux'
import { jogMount, runObservations } from '../actions'
import Controls from '../components/Controls'

const mapStateToProps = (state) => {
  return {
    jogging: state.controls.jogging
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    onJog: (axis) => {
      dispatch(jogMount(axis, 5))
    },
    onRun: (axis) => {
      dispatch(runObservations())
    }
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Controls)

