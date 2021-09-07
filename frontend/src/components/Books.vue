<template>
  <div :key="book.id" v-for="book in $store.state.books">
    <Book :book="book" />
  </div>
</template>

<script>
import Book from './Book'
import {mapActions} from "vuex";

export default {
  name: 'Books',
  props: {
    bookFilter: String
  },
  components: {
    Book
  },
  methods: mapActions(['fetchBooks']),
  created() {
    this.fetchBooks(this.bookFilter)
  }
}
</script>