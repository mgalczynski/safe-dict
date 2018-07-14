import { combineReducers } from 'redux';
import home from './home';
import admin from './admin';

export default combineReducers({
  home,
  admin
});
