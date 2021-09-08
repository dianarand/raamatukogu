
<template>
  <li class="list-group-item list-group-item-action d-flex gap-3 py-3">
    <div class="d-flex gap-2 w-100 justify-content-between">
      <i class="fas fa-book fa-3x"></i>
      <div>
        <h5 class="mb-1">{{ book.title }}</h5>
        <p class="mb-1">{{ book.author }}</p>
        <div>
          <ExpandedBook
          v-show="showExpanded"
          :book="book"
          :showAdditional="showAdditional"
          />
        </div>
      </div>
      <div>
        <div role="group">
          <i @click="toggleExpanded()"
             class="fas fa-info-circle"></i>
          <i @click="removeBook(book.id)"
             v-if="ableToRemove"
              class="fas fa-times"></i>
        </div>
        <small class="text-nowrap">{{ book.year }}</small>
      </div>
    </div>
  </li>
</template>

<!--<template>-->
<!--  <div @dblclick="toggleExpanded()" class="book">-->
<!--    <h3>-->
<!--      {{ book.title }}-->
<!--      <div role="group">-->
<!--        <i @click="toggleExpanded()"-->
<!--           class="fas fa-chevron-down"></i>-->
<!--        <i @click="removeBook(book.id)"-->
<!--           v-if="ableToRemove"-->
<!--            class="fas fa-times"></i>-->
<!--      </div>-->
<!--    </h3>-->
<!--    <p>{{ book.author }} ({{ book.year }})</p>-->
    <ExpandedBook
        v-show="showExpanded"
        :book="book"
        :showAdditional="showAdditional"
    />
<!--  </div>-->
<!--</template>-->

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
  computed: {
    ableToRemove() {
      if (this.hasRemoveBook && this.book.lending == null){
        return true
      } else {
        return false
      }
    }
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
  emits: ['removeBook', 'setMessage']
}
</script>

<style scoped>
i {
  margin: 5px;
}

</style>