<template>
  <div>
    <p>...</p>
    <div v-show="bookIsOut">
      <p>Laenutuse tahtaeg: {{ book.deadline }}</p>
      <a href="javascript:void(0)" @click="returnBook(book.id)">Margi tagastatuks</a>
    </div>
    <div v-show="bookIsReserved">
      <p>Raamat on broneeritud.</p>
      <a href="javascript:void(0)" @click="cancelReservation(book.id)">Tyhista broneering</a>
    </div>
  </div>

</template>

<script>
import axios from "axios";

export default {
  name: 'ExpandedBook',
  props: {
    book: Object
  },
  computed: {
    bookIsOut() {
      if (this.book.lending === undefined) {
        return false
      } else if (this.book.lending !== null) {
        return true
      } else {
        return false
      }
    },
    bookIsReserved() {
      if (this.book.reservation === undefined) {
        return false
      } else if (this.book.reservation !== null) {
        return true
      } else {
        return false
      }
    }
  },
  methods: {
    lendBook() {},
    async returnBook(id) {
      const res = await axios.post(`book/${id}/return`)
      if (res.status === 200) {
          this.book.lending = null
        }
      this.$store.commit('setMessage', res.data.message)
    },
    async cancelReservation(id) {
      const res = await axios.post(`book/${id}/cancel`)
      if (res.status === 200) {
          this.book.reservation = null
        }
      this.$store.commit('setMessage', res.data.message)
    },
  }
}
</script>

<style scoped>

</style>