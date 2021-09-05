<template>
  <AddBook v-show="showAddBook" @add-book="addBook"/>
  <Books @delete-book="deleteBook" :books="books"/>
  <router-link to="/login">Login</router-link>
</template>

<script>
import Books from '../components/Books'
import AddBook from '../components/AddBook'
import axios from "axios";

export default {
  name: 'Home',
  props: {
    showAddBook: Boolean
  },
  components: {
    Books,
    AddBook
  },
  data() {
    return {
      books: []
    }
  },
  methods: {
    addBook(book) {
      const payload = {
        title: book.title,
        author: book.author,
        year: book.year
      }
      const path = 'http://localhost:5000/books'
      axios.post(path, payload)
      .then ((res) => {
        this.msg = res.data['message']
      })
      .catch ((err) => {
        console.error(err);
      });
      this.books = [...this.books, book]
    },
    deleteBook(id) {
      if(confirm('Kas olete kindel, et soovite eemaldada raamatu laenamise nimekirjast?')) {
        const path = `http://localhost:5000/book/${id}`
        console.log(path)
        axios.delete(path)
            .then((res) => {
              if (res.status === 200) {
                this.books = this.books.filter((book) => book.id != id)
              }
              this.msg = res.data['message']
            })
            .catch((err) => {
              console.error(err);
            });
      }
    },
    fetchBooks() {
      const path = 'http://localhost:5000/books';
      axios.get(path)
      .then ((res) => {
        this.books = res.data['books'];
      })
      .catch ((err) => {
        console.error(err);
      });
    },
  },
  created() {
    this.fetchBooks();
  },
}
</script>