<template>
    <div class="p-2 mb-4 container-fluid py-2">
      <h1 class="display-5 fw-bold">
        {{ title }}
        <Button v-show="hasAddBook"
          @btn-click="$emit('toggle-add-book')"
          :text="showAddBook ? 'Sulge' : 'Lisa raamat'"/>
      </h1>
      <div v-bind:class="alert" role="alert" v-if="msg !== ''">
        {{ msg }}
        <button type="button" class="btn-close" @click="clearMessage"></button>
      </div>
      <AddBook
        v-show="showAddBook"
        @setMessage="setMessage"
        @addBook="addBook"
        @hideAddBook="$emit('toggle-add-book')"
      />
      <ul class="list-group" :key="book.id" v-for="book in books">
        <Book
            :book="book"
            :hasRemoveBook="showForLender"
            :showAdditional="true"
            @setMessage="setMessage"
            @removeBook="removeBook"
        />
      </ul>
    </div>
</template>

<script>
import Button from "./Button";
import AddBook from "./AddBook";
import Book from "./Book";
import {showForLender, alertClass} from "../utils";
import axios from "axios";

export default {
  name: 'Header',
  props: {
    title: String,
    hasAddBook: Boolean,
    showAddBook: Boolean,
    bookFilter: String
  },
  components: {
    Button,
    AddBook,
    Book
  },
  computed: {
    showForLender
  },
  data() {
    return {
      books: [],
      msg: '',
      alert: "alert alert-primary"
    }
  },
  methods: {
    setMessage(response) {
      this.alert = alertClass(response.status) + ' alert-dismissible fade show'
      this.msg = response.data.message
    },
    clearMessage() {
      this.msg = ''
    },
    async fetchBooks() {
      try {
        const res = await axios.get(`books?filter=${this.bookFilter}`)
        this.books = res.data.books
      } catch(err) {
        // this.$router.push('/login')
      }
    },
    async addBook(id) {
      const res = await axios.get(`book/${id}`)
      this.books = [...this.books, res.data]
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
<style scoped>
.list-group {
  width: auto;
  max-width: 460px;
  margin: auto;
}
.alert {
  width: 100%;
  max-width: 450px;
  margin: 15px auto;
}
</style>
