<template>
  <div class="p-2 mb-4 container-fluid py-2">
    <h2 class="display-8">
      Otsingu tulemused
      <button type="button" class="btn-close btn-sm" @click="clearResults"></button>
    </h2>
    <ul class="list-group" :key="book.id" v-for="book in books">
      <Book :book="book"
            :showAdditional="false"/>
    </ul>
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
  },
  methods: {
    clearResults() {
      this.$emit('clearResults')
    }
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