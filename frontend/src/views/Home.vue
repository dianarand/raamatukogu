<template>
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
      title="Minu broneeringud"
      :hasAddBook="false"
      :showAddBook="showAddBook"
      bookFilter="reserved_by_me"
      v-if="showForBorrower"
  />
</template>

<script>
import Books from '../components/Books';
import Search from '../components/Search';
import {showForBorrower, showForLender} from '../utils';

export default {
  name: 'Home',
  components: {
    Search,
    Books
  },
  data() {
    return {
      showAddBook: false
    }
  },
  computed: {
    showForBorrower,
    showForLender
  },
  methods: {
    toggleAddBook() {
      this.showAddBook = !this.showAddBook;
    }
  }
}
</script>
<style>
.list-group {
  width: auto;
  max-width: 460px;
  margin: auto;
}
</style>