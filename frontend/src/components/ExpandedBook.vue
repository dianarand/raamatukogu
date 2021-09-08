<template>
  <div>
    <p>{{ msg }}</p>
    <br>
    <div v-show="bookIsOut">
      <p>Raamat on valja laenutatud.</p>
      <div v-if="showAdditional">
        <p>Laenutuse tahtaeg: {{ book.deadline }}</p>
        <a href="javascript:void(0)" @click="returnBook(book.id)">Margi tagastatuks</a>
      </div>
    </div>
    <div v-show="bookIsReserved">
      <p>Raamat on broneeritud.</p>
      <div>
        <a href="javascript:void(0)" @click="cancelReservation(book.id)">Tyhista broneering</a>
      </div>
    </div>
    <div v-show="!bookIsOut && !bookIsReserved">
      <a href="javascript:void(0)"
         @click="lendBook(book.id)"
         v-if="showForLender">Margi raamat laenutatuks</a>
      <a href="javascript:void(0)"
         @click="borrowBook(book.id)"
         v-if="showForBorrower">Laenuta raamat</a><br>
      <a href="javascript:void(0)"
         @click="reserveBook(book.id)"
         v-if="showForBorrower">Broneeri raamat</a>
    </div>
  </div>

</template>

<script>
import axios from "axios";
import {showForLender, showForBorrower} from "../utils";

export default {
  name: 'ExpandedBook',
  data() {
    return {
      msg: ''
    }
  },
  props: {
    book: Object,
    showAdditional: Boolean
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
    },
    showForLender,
    showForBorrower
  },
  methods: {
    async lendBook(id) {
      console.log('click')
      const borrower = prompt('Millisele kasutajale laenutad raamatu?', 'kasutajanimi')
      console.log(borrower)
      const res = await axios.post(`book/${id}/lend`, {'borrower': borrower})
      if (res.status === 200) {
          this.book.lending = res.data.user
          this.book.deadline = res.data.deadline
        }
      this.msg = res.data.message
    },
    async borrowBook(id) {
      const res = await axios.post(`book/${id}/borrow`)
      if (res.status === 200) {
        this.book.lending = res.data.user
        this.book.deadline = res.data.deadline
      }
      this.msg = res.data.message
    },
    async reserveBook(id) {
      const res = await axios.post(`book/${id}/reserve`)
      if (res.status === 200) {
        this.book.reservation = res.data.user
        console.log(this.book.reservation)
        console.log(this.bookIsReserved)
      }
      this.msg = res.data.message
    },
    async returnBook(id) {
      const res = await axios.post(`book/${id}/return`)
      if (res.status === 200) {
          this.book.lending = null
        }
      this.msg = res.data.message
    },
    async cancelReservation(id) {
      const res = await axios.post(`book/${id}/cancel`)
      if (res.status === 200) {
          this.book.reservation = null
        }
      this.msg = res.data.message
    },
  }
}
</script>

<style scoped>

</style>