<template>
  <div class="container">
    <div class="header">
      <h2>{{ title }}</h2>
      <Button v-show="hasAddBook"
        @btn-click="$emit('toggle-add-book')"
        :text="showAddBook ? 'Sulge' : 'Lisa raamat'"
        :color="showAddBook ? 'red' : 'green'"/>
    </div>
    <p>{{ msg }}</p>
    <AddBook
        v-show="showAddBook"
        @setMessage="setMessage"
        @addBook="addBook"
        @hideAddBook="$emit('toggle-add-book')"
    />
    <div :key="book.id" v-for="book in books">
      <Book
          :book="book"
          @setMessage="setMessage"
          @removeBook="removeBook"
      />
    </div>
  </div>
</template>

<script>
import Button from "./Button";
import AddBook from "./AddBook";
import Book from "./Book";
import axios from "axios";

export default {
  name: 'Header',
  props: {
    title: String,
    hasAddBook: Boolean,
    showAddBook: Boolean,
    bookFilter: String,
  },
  components: {
    Button,
    AddBook,
    Book
  },
  data() {
    return {
      books: [],
      msg: '',
    }
  },
  methods: {
    setMessage(message) {
      this.msg = message
    },
    async fetchBooks() {
      const res = await axios.get(`books?filter=${this.bookFilter}`)
      this.books = res.data.books
    },
    addBook(book) {
      this.books = [...this.books, book]
    },
    removeBook(id) {
      this.books = this.books.filter((book) => book.id != id)
    }
  },
  created() {
    this.fetchBooks()
  },
  emits: ['toggle-add-book'],
}
</script>
