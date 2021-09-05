<template>
  <div :key="book.id" v-for="book in books">
    <Book @remove-book="$emit('remove-book', book.id)"
          :book="book" />
  </div>
</template>

<script>
import Book from './Book'
import axios from "axios";

export default {
  name: 'Books',
  props: {
    books: Array
  },
  components: {
    Book
  },
  emits: ['delete-book'],
}
</script>