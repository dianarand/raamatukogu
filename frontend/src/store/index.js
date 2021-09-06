import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    books: [],
    msg: '',
  },
  mutations: {
    saveBooks(state, books) {
      state.books = books
    },
    addBook(state, book) {
      state.books = [...state.books, book]
    },
    removeBook(state, id) {
      state.books = state.books.filter((book) => book.id != id)
    },
    setMessage(state, msg) {
      state.msg = msg
    },
    clearMessage(state) {
      state.msg = ''
    }
  },
  actions: {
    fetchBooks({ commit }) {
      // const path = `http://localhost:5000/books?filter=${self.bookFilter}`;
      const path = 'http://localhost:5000/books';
      axios.get(path)
      .then ((res) => {
        commit('saveBooks', res.data.books)
      })
      .catch ((err) => {
        console.error(err);
      });
    },
    addBook({ commit }, book) {
      const payload = {
        title: book.title,
        author: book.author,
        year: book.year
      }
      const path = 'http://localhost:5000/books'
      axios.post(path, payload)
      .then ((res) => {
        commit('setMessage', res.data.message)
        if (res.status === 201) {
          commit('addBook', book)
        }
      })
      .catch ((err) => {
        console.error(err);
      });
    },
    removeBook({ commit }, id) {
      if(confirm('Kas olete kindel, et soovite eemaldada raamatu laenamise nimekirjast?')) {
        const path = `http://localhost:5000/book/${id}`
        axios.delete(path)
        .then((res) => {
          if (res.status === 200) {
            commit('removeBook', id)
          }
          commit('setMessage', res.data.message)
        })
        .catch((err) => {
          console.error(err);
        });
      }
    }
  },
  modules: {
  }
})
