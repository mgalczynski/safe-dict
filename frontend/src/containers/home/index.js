import React from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogActions from '@material-ui/core/DialogActions';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
import { push } from 'connected-react-router';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { changeUrl, sendRequest } from '../../modules/home';

const styles = theme => ({
  root: {
    textAlign: 'center',
    paddingTop: theme.spacing.unit * 20
  }
});
const Home = props => (
  <div>
    <TextField
      id="url"
      name="url"
      label="url"
      placeholder="url"
      value={props.url}
      onChange={e => props.changeUrl(e.target.value)}
    />
    <Button variant="contained" color="secondary" onClick={props.sendRequest}>
      Super Secret Password
    </Button>
    {props.error && (
      <div>
        {props.error.code} {props.error.reason}
      </div>
    )}
    {props.lastUrl && (
      <div style={{ textAlign: 'center' }}>
        <div>Cloud for: {props.lastUrl}</div>
        {props.wordCloud
          ? props.wordCloud.map(i => (
              <span
                key={i[0]}
                style={{
                  fontSize: i[1] * 90 + 10,
                  wordSpacing: 25,
                  verticalAlign: 'middle'
                }}>
                {i[0] + ' '}
              </span>
            ))
          : 'Cloud is empty :('}
      </div>
    )}
  </div>
);

const mapStateToProps = ({ home }) => ({
  ...home
});

const mapDispatchToProps = dispatch =>
  bindActionCreators(
    {
      changeUrl,
      sendRequest
    },
    dispatch
  );

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withStyles(styles)(Home));
