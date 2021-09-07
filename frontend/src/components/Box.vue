<template>
  <div class="container">
    <div class="header">
      <h2>{{ title }}</h2>
      <Button v-show="hasAddBook"
        @btn-click="$emit('toggle-add-book')"
        :text="showAddBook ? 'Sulge' : 'Lisa raamat'"
        :color="showAddBook ? 'red' : 'green'"/>
    </div>
    <p>{{ $store.state.msg }}</p>
    <AddBook v-show="showAddBook" @hideAddBook="$emit('toggle-add-book')"/>
    <Books :bookFilter="bookFilter"/>
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
    hasAddBook: Boolean,
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
  emits: ['toggle-add-book'],
}
</script>
