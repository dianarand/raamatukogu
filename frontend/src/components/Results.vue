<template>
  <div class="p-2 mb-4 container-fluid py-2">
    <h2 class="display-8">
      Otsingu tulemused
      <button type="button" class="btn-close btn-sm" @click="clearResults"></button>
    </h2>
    <p v-if="books.length === 0">Otsinguparameetritele vastavaid raamatuid ei leitud</p>
    <ul class="list-group" :key="book.id" v-for="book in visibleBooks">
      <Book :book="book"
            :showAdditional="false"/>
    </ul>
    <Pagination v-if="this.visibleBooks < this.books"
                @previousPage="updatePage(this.currentPage - 1)"
                @nextPage="updatePage(this.currentPage + 1)"/>
  </div>
</template>

<script>
import Book from './Book'
import Pagination from "./Pagination";

export default {
  name: 'Results',
  data() {
    return {
      currentPage: 0,
      pageSize: 3,
      visibleBooks: [],
    }
  },
  props: {
    books: Array
  },
  components: {
    Book,
    Pagination
  },
  methods: {
    clearResults() {
      this.$emit('clearResults')
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
    this.updateVisibleBooks()
  }
}
</script>
<style scoped>
.list-group {
  width: auto;
  max-width: 460px;
  margin: auto;
}
</style>