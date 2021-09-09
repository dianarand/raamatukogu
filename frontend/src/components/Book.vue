<template>
  <li @dblclick="toggleExpanded()" class="list-group-item list-group-item-action d-flex gap-3 py-3">
    <div class="d-flex gap-2 w-100 justify-content-between">
      <i class="fas fa-book fa-3x" :style="{ color: bookColor}"></i>
      <div>
        <h5 class="mb-1">{{ book.title }}</h5>
        <p class="mb-1">{{ book.author }}</p>
        <div>
          <ExpandedBook
          v-show="showExpanded"
          :book="book"
          :showAdditional="showAdditional"
          :bookColor="bookColor"
          />
          <div v-show="showRemove">
            <hr>
            <form @submit.prevent="removeBook(book.id)">
              <div class="mb-3">
                <label for="submit">Kas olete kindel, et soovite eemaldada raamatu laenamise nimekirjast?</label>
              </div>
              <div class="d-grid gap-2 d-md-block">
                <button class="btn btn-danger float-start" type="submit" id="submit">Eemalda</button>
                <button class="btn btn-outline-secondary float-end" type="button" @click="cancelRemove">Tühista</button>
              </div>
            </form>
          </div>
        </div>
      </div>
      <div class="text-nowrap">
        <div role="group">
          <i @click="toggleExpanded()"
             class="fas fa-info-circle"></i>
          <i @click="openRemove"
             v-if="ableToRemove"
             class="fas fa-times"></i>
        </div>
        <small>{{ book.year }}</small>
      </div>
    </div>
  </li>
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
      showExpanded: false,
      showRemove: false
    }
  },
  props: {
    book: Object,
    hasRemoveBook: Boolean,
    showAdditional: Boolean
  },
  computed: {
    ableToRemove() {
      if (this.hasRemoveBook && this.book.lending == null){
        return true
      } else {
        return false
      }
    },
    bookColor() {
      if (this.book.overtime === true && this.showAdditional === true) {
        return "#dc3545";
      } else {
        return "black";
      }
    }
  },
  methods: {
    async removeBook(id) {
      try {
        const res = await axios.delete(`http://localhost:5000/book/${id}`)
        if (res.status === 200) {
          this.$emit('removeBook', id)
        }
        this.$emit('setMessage', res)
      } catch(err) {
        this.$emit('setMessage', err.response)
      }
    },
    toggleExpanded() {
      this.showExpanded = !this.showExpanded
    },
    openRemove() {
      this.showRemove = true
    },
    cancelRemove() {
      this.showRemove = false
    }
  },
  emits: ['removeBook', 'setMessage']
}
</script>

<style scoped>

i {
  margin: 5px;
}

</style>