import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    books: [
      {
        id: 1,
        title: "Harry Potter and the Philosopher's Stone",
        author: "J. K. Rowling",
        year: "1997",
        active: true,
        reminder: true,
      },
      {
        id: 2,
        title: "Hunger Games",
        author: "Suzanne Collins",
        year: "2008",
        active: true,
        reminder: true,
      },
      {
        id: 3,
        title: "A Court of Thorns and Roses",
        author: "Sarah J. Maas",
        year: "2015",
        active: true,
        reminder: false,
      }
    ]
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
        // this.msg = res.data.message;
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
          // this.msg = res.data.message;
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
