<template>
  <Box
      @toggle-add-book="toggleAddBook"
      title="Minu raamatud"
      :showAddBook="showAddBook"
      bookFilter="owned_by_me"
  />
  <Box
      @toggle-add-book="toggleAddBook"
      title="Minu laenutused"
      :showAddBook="showAddBook"
      bookFilter="borrowed_by_me"
  />
  <Box
      @toggle-add-book="toggleAddBook"
      title="Minu reserveeringud"
      :showAddBook="showAddBook"
      bookFilter="reserved_by_me"
  />
</template>

<script>
import Box from '../components/Box'

export default {
  name: 'Home',
  data() {
    return {
      showAddBook: false
    }
  },
  components: {
    Box
  },
  methods: {
    toggleAddBook() {
      this.showAddBook = !this.showAddBook
    },
  }
}
</script>