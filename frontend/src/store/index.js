import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    books: [],
    msg: '',
  },
  mutations: {
    saveBooks: (state, books) => (state.books = books),
    addBook: (state, book) => (state.books = [...state.books, book]),
    removeBook: (state, id) => (state.books = state.books.filter((book) => book.id != id)),
    setMessage: (state, msg) => (state.msg = msg),
    clearMessage: (state) => (state.msg = ''),
  },
  actions: {
    async fetchBooks({ commit }) {
      // const path = `http://localhost:5000/books?filter=${bookFilter}`;
      const res = await axios.get('books')
      console.log(res.data)
      commit('saveBooks', res.data.books)
    },
    async addBook({ commit }, book) {
      const res = await axios.post('books', {
        title: book.title,
        author: book.author,
        year: book.year
      })
      commit('setMessage', res.data.message)
      if (res.status === 201) {
        commit('addBook', book)
      }
    },
    async removeBook({ commit }, id) {
      if(confirm('Kas olete kindel, et soovite eemaldada raamatu laenamise nimekirjast?')) {
        const res = await axios.delete(`http://localhost:5000/book/${id}`)
        if (res.status === 200) {
          commit('removeBook', id)
        }
        commit('setMessage', res.data.message)
      }
    },
  },
  modules: {
  }
})
