<template>
  <Box
      @toggle-add-book="toggleAddBook"
      title="Minu raamatud"
      :showAddBook="showAddBook"
      bookFilter="owned_by_me"
      v-show="showForLender"
  />
  <Box
      @toggle-add-book="toggleAddBook"
      title="Minu laenutused"
      :showAddBook="showAddBook"
      bookFilter="borrowed_by_me"
      v-show="showForBorrower"
  />
  <Box
      @toggle-add-book="toggleAddBook"
      title="Minu reserveeringud"
      :showAddBook="showAddBook"
      bookFilter="reserved_by_me"
      v-show="showForBorrower"
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
  computed: {
    showForLender() {
      if (this.$store.state.role === 'lender') {
        return true
      } else {
        return false
      }
    },
    showForBorrower() {
      if (this.$store.state.role === 'borrower') {
        return true
      } else {
        return false
      }
    }
  },
  methods: {
    toggleAddBook() {
      this.showAddBook = !this.showAddBook
    },
  }
}
</script>