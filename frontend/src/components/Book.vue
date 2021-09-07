<template>
  <div class="book">
    <h3>
      {{ book.title }}
      <div role="group">
        <i class="fas fa-undo-alt"></i>
        <i @click="toggleExpanded()" class="fas fa-chevron-down"></i>
        <i @click="removeBook(book.id)" class="fas fa-times"></i>
      </div>
    </h3>
    <p>{{ book.author }} ({{ book.year }})</p>
    <ExpandedBook v-show="showExpanded" :book="book"/>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import ExpandedBook from './ExpandedBook'

export default {
  name: 'Book',
  components: {
    ExpandedBook
  },
  data() {
    return {
      showExpanded: false
    }
  },
  props: {
    book: Object
  },
  methods: {
    ...mapActions(['removeBook']),
    toggleExpanded() {
      this.showExpanded = !this.showExpanded
    }
  }

}
</script>

<style scope>
.fas {
  color: red;
}
.book {
  background: #f4f4f4;
  margin: 5px;
  padding: 10px 20px;
  cursor: pointer;
}
.book h3 {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>