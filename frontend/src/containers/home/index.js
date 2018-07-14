import React from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import TextField from '@material-ui/core/TextField';
import Checkbox from '@material-ui/core/Checkbox';
import { withStyles } from '@material-ui/core/styles';
import { push } from 'connected-react-router';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { changeUrl, sendRequest, changeOnlyTopWords } from '../../modules/home';

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
        <FormControlLabel
          label="Display only top 100 words"
          control={
            <Checkbox
              checked={props.onlyTopWords}
              onChange={props.changeOnlyTopWords}
              value="onlyTopWords"
            />
          }
        />
        <div>
          {props.wordCloud !== null
            ? props.wordCloud
                .filter(i => !props.onlyTopWords || i.isInTop100)
                .map(i => (
                  <span
                    key={i.word}
                    style={{
                      fontSize: i.size * 90 + 10,
                      wordSpacing: 25,
                      verticalAlign: 'middle',
                      color:
                        i.isInTop100 && !props.onlyTopWords ? 'red' : 'black'
                    }}>
                    {i.word + ' '}
                  </span>
                ))
            : 'Cloud is empty :('}
        </div>
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
      sendRequest,
      changeOnlyTopWords
    },
    dispatch
  );

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withStyles(styles)(Home));
