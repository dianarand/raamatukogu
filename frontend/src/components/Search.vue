<template>
  <div class="container">
  <form @submit.prevent="searchBook()">
    <div class="input-group mb-3">
      <select v-model="property" class="input-group-text">
        <option value="title">Pealkiri</option>
        <option value="author">Autor</option>
        <option value="year">Ilmumisaasta</option>
      </select>
      <input type="search" v-model="search" class="form-control" placeholder="Otsi..." />
    </div>
  </form>
  <Results
      v-if="showResults"
      :books="result"
      @clearResults="clearResults"
  />
  </div>
</template>

<script>
import axios from 'axios';
import Results from './Results'

export default {
  name: 'Search',
  components: {
    Results
  },
  data() {
    return {
      search: '',
      property: 'title',
      result: null
    }
  },
  computed: {
    showResults() {
      return this.result !== null;
    }
  },
  methods: {
    async searchBook() {
      this.clearResults();
      const query = `${this.property}=${this.search}`;
      const res = await axios.get(`books?${query}`);
      this.result = res.data.books;
    },
    clearResults() {
      this.result = null;
    }
  }
}
</script>

<style scoped>
form {
  width: 100%;
  margin: auto;
}
</style>