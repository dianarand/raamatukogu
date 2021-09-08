<template>
  <form @submit.prevent="searchBook()" class="add-form">
    <div class="form-control">
      <input list="properties" v-model="property" name="property" id="property" placeholder="Otsingu parameeter" />
      <datalist id="properties">
        <option value="title">Pealkiri</option>
        <option value="author">Autor</option>
        <option value="year">Ilmumisaasta</option>
      </datalist>
    </div>
    <div class="form-control">
      <input type="text" v-model="search" name="search" placeholder="Otsi raamatut" />
    </div>
    <input type="submit" value="Otsi" class="btn btn-block" />
  </form>
  <Results v-if="showResults" :books="result"/>
</template>

<script>
import axios from "axios";
import Results from './Results'

export default {
  name: 'Search',
  data() {
    return {
      search: '',
      property: '',
      result: null
    }
  },
  components: {
    Results
  },
  computed: {
    showResults() {
      if (this.result !== null) {
        return true
      } else {
        return false
      }
    }
  },
  methods: {
    async searchBook() {
      const query = `${this.property}=${this.search}`
      const res = await axios.get(`books?${query}`)
      this.result = res.data.books
    },
  }
}
</script>