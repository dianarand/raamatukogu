<template>
  <Box
      @toggle-add-book="toggleAddBook"
      title="Minu raamatud"
      :hasAddBook="true"
      :showAddBook="showAddBook"
      bookFilter="owned_by_me"
      v-if="showForLender"
  />
  <Box
      @toggle-add-book="toggleAddBook"
      title="Minu laenutused"
      :hasAddBook="false"
      :showAddBook="showAddBook"
      bookFilter="borrowed_by_me"
      v-if="showForBorrower"
  />
  <Box
      @toggle-add-book="toggleAddBook"
      title="Minu reserveeringud"
      :hasAddBook="false"
      :showAddBook="showAddBook"
      bookFilter="reserved_by_me"
      v-if="showForBorrower"
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
      if (localStorage.getItem('role') === 'lender') {
        return true
      } else {
        return false
      }
    },
    showForBorrower() {
      if (localStorage.getItem('role') === 'borrower') {
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