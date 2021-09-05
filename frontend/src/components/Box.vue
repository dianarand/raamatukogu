<template>
  <div class="container">
    <div class="header">
      <h1>{{ title }}</h1>
      <Button v-show="homePage"
        @btn-click="$emit('toggle-add-book')"
        :text="showAddBook ? 'Sulge' : 'Lisa raamat'"
        :color="showAddBook ? 'red' : 'green'"/>
    </div>
    <AddBook v-show="showAddBook" @add-book="addBook"/>
    <Books @remove-book="deleteBook" :books="books"/>
  </div>
</template>

<script>
import Button from './Button'
import AddBook from "./AddBook"
import Books from './Books'
import axios from "axios";

export default {
  name: 'Header',
  props: {
    title: String,
    showAddBook: Boolean,
    bookFilter: String,
  },
  components: {
    Button,
    AddBook,
    Books
  },
  data() {
    return {
      books: []
    }
  },
  computed: {
    homePage() {
      return this.$route.path === '/';
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
      // const path = `http://localhost:5000/books?filter=${self.bookFilter}`;
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
  emits: ['toggle-add-book'],
}
</script>
