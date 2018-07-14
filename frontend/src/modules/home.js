export const WORD_CLOUD_RECEIVED = 'home/WORD_CLOUD_RECEIVED';
export const CHANGE_URL = 'home/CHANGE_URL';
export const CHANGE_ONLY_TOP_WORDS = 'home/CHANGE_ONLY_TOP_WORDS';
export const ERROR_RECEIVED = 'home/ERROR_RECEIVED';

const initialState = {
  url: 'en.wikipedia.org/wiki/Somerset_Levels',
  lastUrl: null,
  wordCloud: null,
  onlyTopWords: false,
  error: null
};

export default (state = initialState, action) => {
  switch (action.type) {
    case CHANGE_URL:
      return {
        ...state,
        url: action.url
      };
    case WORD_CLOUD_RECEIVED: {
      const wordCloud = action.wordCloud;
      wordCloud.sort((a, b) => a.word.localeCompare(b.word));
      return {
        ...state,
        lastUrl: action.url,
        url: '',
        wordCloud: wordCloud,
        error: null
      };
    }
    case ERROR_RECEIVED:
      return {
        ...state,
        lastUrl: null,
        url: '',
        wordCloud: null,
        error: { code: action.code, reason: action.reason }
      };
    case CHANGE_ONLY_TOP_WORDS:
      return {
        ...state,
        onlyTopWords: !state.onlyTopWords
      };

    default:
      return state;
  }
};

export const changeUrl = url => {
  return dispatch => {
    dispatch({
      type: CHANGE_URL,
      url: url
    });
  };
};

export const changeOnlyTopWords = () => {
  return dispatch => {
    dispatch({ type: CHANGE_ONLY_TOP_WORDS });
  };
};

export const sendRequest = () => {
  return (dispatch, getState) => {
    const state = getState();
    fetch('/api/generateWordCloud', {
      method: 'POST',
      body: JSON.stringify({ url: state.home.url })
    })
      .then(response => {
        if (!response.ok) throw response;
        return response.json();
      })
      .then(response =>
        dispatch({
          type: WORD_CLOUD_RECEIVED,
          wordCloud: response.result,
          url: state.home.url
        })
      )
      .catch(error =>
        dispatch({
          type: ERROR_RECEIVED,
          code: error.status,
          reason: error.statusText
        })
      );
  };
};
