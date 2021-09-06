<template>
  <div :key="book.id" v-for="book in $store.state.books">
    <Book :book="book" />
  </div>
</template>

<script>
import Book from './Book'

export default {
  name: 'Books',
  components: {
    Book
  },
  created() {
    this.$store.dispatch('fetchBooks');
  }
}
</script>