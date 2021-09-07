<template>
  <div class="container">
    <div class="header">
      <h2>Otsingu tulemused</h2>
    </div>
    <div :key="book.id" v-for="book in books">
      <Book :book="book" />
    </div>
  </div>
</template>

<script>
import Book from './Book'

export default {
  name: 'Results',
  props: {
    books: Array
  },
  components: {
    Book
  }
}
</script>

<style scoped>

</style>