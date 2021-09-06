<template>
  <div class="container">
    <div class="header">
      <h1>{{ title }}</h1>
      <Button v-show="homePage"
        @btn-click="$emit('toggle-add-book')"
        :text="showAddBook ? 'Sulge' : 'Lisa raamat'"
        :color="showAddBook ? 'red' : 'green'"/>
    </div>
    <p>{{ msg }}</p>
    <AddBook v-show="showAddBook" />
    <Books />
  </div>
</template>

<script>
import Button from './Button'
import AddBook from "./AddBook"
import Books from './Books'

export default {
  name: 'Header',
  props: {
    title: String,
    showAddBook: Boolean,
    bookFilter: String,
  },
  components: {
    Button,
    AddBook,
    Books
  },
  data() {
    return {
      books: [],
      msg: ''
    }
  },
  computed: {
    homePage() {
      return this.$route.path === '/';
    }
  },
  emits: ['toggle-add-book'],
}
</script>
