<template>
  <div :key="book.id" v-for="book in books">
    <Book @delete-book="$emit('delete-book', book.id)"
          :book="book" />
  </div>
</template>

<script>
import Book from './Book'

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