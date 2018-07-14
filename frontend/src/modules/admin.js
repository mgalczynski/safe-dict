export const WORDS_LOADED = 'admin/WORDS_LOADED';
export const ORDER_CHANGED = 'admin/ORDER_CHANGED';
export const ERROR_RECEIVED = 'admin/ERROR_RECEIVED';
export const WORD_ASC = 'WORD_ASC';
export const WORD_DESC = 'WORD_DESC';
export const OCCURRENCES_ASC = 'OCCURRENCES_ASC';
export const OCCURRENCES_DESC = 'OCCURRENCES_DESC';

const initialState = {
  words: null,
  order: null,
  error: null
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
      if (words === null) return state;
      const words = state.words.clone();
      switch (action.order) {
        case WORD_ASC:
          words.sort((a, b) => a.word.localeCompare(b.word));
        case WORD_DESC:
          words.sort((a, b) => b.word.localeCompare(a.word));
        case OCCURRENCES_ASC:
          words.sort((a, b) => a.occurrences - b.occurrences);
        case OCCURRENCES_DESC:
          words.sort((a, b) => b.occurrences - a.occurrences);
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

    default:
      return state;
  }
};

export const changeOrder = order => {
  return dispatch => {
    dispatch({ type: ORDER_CHANGED, order });
  };
};

export const loadWords = () => {
  return dispatch =>
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
};