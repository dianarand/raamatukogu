<template>
  <div @dblclick="toggleExpanded()" class="book">
    <h3>
      {{ book.title }}
      <div role="group">
        <i @click="toggleExpanded()"
           class="fas fa-chevron-down"></i>
        <i @click="removeBook(book.id)"
           v-if="hasRemoveBook"
            class="fas fa-times"></i>
      </div>
    </h3>
    <p>{{ book.author }} ({{ book.year }})</p>
    <ExpandedBook
        v-show="showExpanded"
        :book="book"
        :showAdditional="showAdditional"
    />
  </div>
</template>

<script>
import ExpandedBook from './ExpandedBook'
import axios from "axios";

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
    book: Object,
    hasRemoveBook: Boolean,
    showAdditional: Boolean
  },
  methods: {
    async removeBook(id) {
      if(confirm('Kas olete kindel, et soovite eemaldada raamatu laenamise nimekirjast?')) {
        const res = await axios.delete(`http://localhost:5000/book/${id}`)
        if (res.status === 200) {
          this.$emit('removeBook', id)
        }
        this.$emit('setMessage', res.data.message)
      }
    },
    toggleExpanded() {
      this.showExpanded = !this.showExpanded
    }
  },
  emits: ['setMessage']
}
</script>

<style scope>
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