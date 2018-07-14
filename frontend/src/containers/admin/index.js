import React from 'react';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import RadioGroup from '@material-ui/core/RadioGroup';
import Radio from '@material-ui/core/Radio';
import CircularProgress from '@material-ui/core/CircularProgress';
import { withStyles } from '@material-ui/core/styles';
import { push } from 'connected-react-router';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import {
  changeOrder,
  loadData,
  WORD_ASC,
  WORD_DESC,
  OCCURRENCES_ASC,
  OCCURRENCES_DESC
} from '../../modules/admin';

const styles = () => ({
  tdLimited: {
    maxWidth: 350,
    textOverflow: 'ellipsis',
    overflow: 'hidden',
    whiteSpace: 'nowrap'
  }
});

class Admin extends React.Component {
  componentDidMount = () => {
    this.props.loadData();
  };
  render() {
    return (
      <div>
        {/*urls*/}
        {this.props.urls === null ? (
          <CircularProgress size={50} />
        ) : (
          <table border={1}>
            <thead>
              <tr>
                <th>Created</th>
                <th>Url</th>
                <th>Hash</th>
                <th>Analysis</th>
                <th>Confidence</th>
              </tr>
            </thead>
            <tbody>
              {this.props.urls.map(u => (
                <tr key={u.Hash}>
                  <td>{u.created}</td>
                  <td className={this.props.classes.tdLimited}>{u.url}</td>
                  <td className={this.props.classes.tdLimited}>
                    {u.hashOfUrl}
                  </td>
                  <td>{u.analysis}</td>
                  <td>{u.confidence}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        {/*words*/}
        {this.props.words === null ? (
          <CircularProgress size={50} />
        ) : (
          <div>
            <RadioGroup
              value={this.props.order}
              onChange={e => this.props.changeOrder(e.target.value)}>
              <FormControlLabel
                value={WORD_ASC}
                control={<Radio />}
                label="Word ascending"
              />
              <FormControlLabel
                value={WORD_DESC}
                control={<Radio />}
                label="Word descening"
              />
              <FormControlLabel
                value={OCCURRENCES_ASC}
                control={<Radio />}
                label="Occurrences ascending"
              />
              <FormControlLabel
                value={OCCURRENCES_DESC}
                control={<Radio />}
                label="Occurrences descending"
              />
            </RadioGroup>
            <table border={1}>
              <thead>
                <tr>
                  <th>Word</th>
                  <th>Occurrences</th>
                  <th>Created</th>
                  <th>Last modified</th>
                </tr>
              </thead>
              <tbody>
                {this.props.words.map(w => (
                  <tr key={w.word}>
                    <td className={this.props.classes.tdLimited}>{w.word}</td>
                    <td>{w.occurrences}</td>
                    <td>{w.created}</td>
                    <td>{w.lastModified}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
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
      loadData
    },
    dispatch
  );

export default withStyles(styles)(
  connect(
    mapStateToProps,
    mapDispatchToProps
  )(Admin)
);
