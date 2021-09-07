<template>
  <a href="javascript:void(0)" @click="logOut">Logi välja</a>
  <Search v-if="showForBorrower"/>
  <Books
      @toggle-add-book="toggleAddBook"
      title="Minu raamatud"
      :hasAddBook="true"
      :showAddBook="showAddBook"
      bookFilter="owned_by_me"
      v-if="showForLender"
  />
  <Books
      @toggle-add-book="toggleAddBook"
      title="Minu laenutused"
      :hasAddBook="false"
      :showAddBook="showAddBook"
      bookFilter="borrowed_by_me"
      v-if="showForBorrower"
  />
  <Books
      @toggle-add-book="toggleAddBook"
      title="Minu reserveeringud"
      :hasAddBook="false"
      :showAddBook="showAddBook"
      bookFilter="reserved_by_me"
      v-if="showForBorrower"
  />
</template>

<script>
import Search from '../components/Search'
import Books from '../components/Books'

export default {
  name: 'Home',
  data() {
    return {
      showAddBook: false
    }
  },
  components: {
    Search,
    Books
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
    logOut() {
      localStorage.removeItem('token');
      console.log(localStorage.getItem('token'))
      this.$router.push('/login')
    },
  }
}
</script>