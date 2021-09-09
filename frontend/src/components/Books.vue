<template>
    <div class="p-2 mb-4 container-fluid py-2">
      <h1 class="display-5 fw-bold">
        {{ title }}
        <Button v-show="hasAddBook"
          @btn-click="$emit('toggle-add-book')"
          :text="showAddBook ? 'Sulge' : 'Lisa raamat'"/>
        <i class="fas fa-sync fs-6" @click="fetchBooks" v-if="showForBorrower"></i>
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
      <ul class="list-group" :key="book.id" v-for="book in visibleBooks">
        <Book
            :book="book"
            :hasRemoveBook="showForLender"
            :showAdditional="true"
            @setMessage="setMessage"
            @removeBook="removeBook"
        />
      </ul>
      <Pagination v-if="this.visibleBooks < this.books"
                  @previousPage="updatePage(this.currentPage - 1)"
                  @nextPage="updatePage(this.currentPage + 1)"/>
    </div>
</template>

<script>
import Button from "./Button";
import AddBook from "./AddBook";
import Book from "./Book";
import Pagination from "./Pagination";
import {showForLender, showForBorrower, alertClass} from "../utils";
import axios from "axios";

export default {
  name: 'Header',
    data() {
    return {
      books: [],
      currentPage: 0,
      pageSize: 3,
      visibleBooks: [],
      msg: '',
      alert: "alert alert-primary"
    }
  },
  props: {
    title: String,
    hasAddBook: Boolean,
    showAddBook: Boolean,
    bookFilter: String
  },
  components: {
    Pagination,
    Button,
    AddBook,
    Book
  },
  computed: {
    showForLender,
    showForBorrower
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
        this.$router.push('/login')
      }
      this.updateVisibleBooks()
    },
    async addBook(id) {
      const res = await axios.get(`book/${id}`)
      this.books = [...this.books, res.data]
      this.updateVisibleBooks();
    },
    removeBook(id) {
      this.books = this.books.filter((book) => book.id != id)
      this.updateVisibleBooks();
    },
    updatePage(pageNumber) {
      this.currentPage = pageNumber;
      this.updateVisibleBooks();
    },
    updateVisibleBooks() {
      this.visibleBooks = this.books.slice(this.currentPage * this.pageSize,
          (this.currentPage * this.pageSize) + this.pageSize);
      if (this.visibleBooks.length === 0 && this.currentPage > 0) {
        this.updatePage(this.currentPage - 1);
      } else if (this.visibleBooks.length === 0 && this.currentPage < 0) {
        this.updatePage(this.currentPage + 1);
      }
    }
  },
  created() {
    this.fetchBooks()
    if (this.showForLender === true) {
      this.pageSize = 8;
    }
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
