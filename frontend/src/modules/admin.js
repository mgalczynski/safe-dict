export const WORDS_LOADED = 'admin/WORDS_LOADED';
export const URLS_LOADED = 'admin/URLS_LOADED';
export const ORDER_CHANGED = 'admin/ORDER_CHANGED';
export const ERROR_RECEIVED = 'admin/ERROR_RECEIVED';
export const WORD_ASC = 'WORD_ASC';
export const WORD_DESC = 'WORD_DESC';
export const OCCURRENCES_ASC = 'OCCURRENCES_ASC';
export const OCCURRENCES_DESC = 'OCCURRENCES_DESC';

const initialState = {
  words: null,
  order: null,
  error: null,
  urls: null
};

export default (state = initialState, action) => {
  switch (action.type) {
    case WORDS_LOADED:
      return {
        ...state,
        words: action.words,
        order: null,
        error: null
      };
    case ORDER_CHANGED: {
      if (state.words === null) return state;
      const words = state.words.slice(0);
      switch (action.order) {
        case WORD_ASC:
          words.sort((a, b) => a.word.localeCompare(b.word));
          break;
        case WORD_DESC:
          words.sort((a, b) => b.word.localeCompare(a.word));
          break;
        case OCCURRENCES_ASC:
          words.sort((a, b) => a.occurrences - b.occurrences);
          break;
        case OCCURRENCES_DESC:
          words.sort((a, b) => b.occurrences - a.occurrences);
          break;
        default:
          break;
      }
      return {
        ...state,
        order: action.order,
        words,
        error: null
      };
    }
    case ERROR_RECEIVED:
      return {
        ...state,
        words: null,
        order: null,
        error: { code: action.code, reason: action.reason }
      };

    case URLS_LOADED:
      return {
        ...state,
        urls: action.urls
      };

    default:
      return state;
  }
};

export const changeOrder = order => {
  return dispatch => {
    dispatch({ type: ORDER_CHANGED, order });
  };
};

export const loadData = () => {
  return dispatch => {
    fetch('/adminApi/getWords')
      .then(response => {
        if (!response.ok) throw response;
        return response.json();
      })
      .then(response =>
        dispatch({
          type: WORDS_LOADED,
          words: response.result
        })
      )
      .catch(error =>
        dispatch({
          type: ERROR_RECEIVED,
          code: error.status,
          reason: error.statusText
        })
      );
    fetch('/adminApi/getUrls')
      .then(response => response.json())
      .then(response =>
        dispatch({
          type: URLS_LOADED,
          urls: response.result
        })
      );
  };
};
