import React from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogActions from '@material-ui/core/DialogActions';
import TextField from '@material-ui/core/TextField';
import CircularProgress from '@material-ui/core/CircularProgress';
import { withStyles } from '@material-ui/core/styles';
import { push } from 'connected-react-router';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { changeOrder, loadWords } from '../../modules/admin';
import { renderComponent } from 'recompose';

const styles = () => ({
  tdLimited: {
    maxWidth: 40,
    textOverflow: 'ellipsis',
    overflow: 'hidden',
    whiteSpace: 'nowrap'
  }
});

class Admin extends React.Component {
  componentDidMount = () => {
    this.props.loadWords();
  };
  render() {
    console.log(this.props);
    return (
      <div>
        {this.props.words === null ? (
          <CircularProgress size={50} />
        ) : (
          <table border={1}>
            <thead>
              <tr>
                <th>Word</th>
                <th>Occurrences</th>
              </tr>
            </thead>
            <tbody>
              {this.props.words.map(w => (
                <tr key={w.word}>
                  <td>{w.word}</td>
                  <td>{w.occurrences}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    );
  }
}

const mapStateToProps = ({ admin }) => ({
  ...admin
});

const mapDispatchToProps = dispatch =>
  bindActionCreators(
    {
      changeOrder,
      loadWords
    },
    dispatch
  );

export default withStyles(styles)(
  connect(
    mapStateToProps,
    mapDispatchToProps
  )(Admin)
);
