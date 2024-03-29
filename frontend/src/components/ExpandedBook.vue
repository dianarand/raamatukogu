<template>
  <div>
    <hr>
    <div v-bind:class="alert" role="alert" v-if="msg !== ''">
      {{ msg }}
    </div>
    <div v-show="bookIsOut">
      <p>Raamat on välja laenutatud.</p>
      <div v-if="showAdditional">
        <p :style="{ color: bookColor}">Laenutuse tähtaeg: {{ dateFormat(book.deadline) }}</p>
        <a href="javascript:void(0)" @click="returnBook(book.id)">Märgi tagastatuks</a>
      </div>
    </div>
    <div v-show="bookIsReserved">
      <p>Raamat on broneeritud.</p>
      <div v-if="showAdditional">
        <a href="javascript:void(0)" @click="cancelReservation(book.id)">Tühista broneering</a>
        <a href="javascript:void(0)"
         @click="borrowBook(book.id)"
         v-if="showForBorrower"><br>Laenuta raamat</a>
        <a href="javascript:void(0)"
         @click="openLend"
         v-if="showForLender"><br>Märgi raamat laenutatuks</a>
      </div>
    </div>
    <div v-show="!bookIsOut && !bookIsReserved && !showLend">
      <a href="javascript:void(0)"
         @click="openLend"
         v-if="showForLender">Märgi raamat laenutatuks</a>
      <a href="javascript:void(0)"
         @click="borrowBook(book.id)"
         v-if="showForBorrower">Laenuta raamat</a><br>
      <a href="javascript:void(0)"
         @click="reserveBook(book.id)"
         v-if="showForBorrower">Broneeri raamat</a>
    </div>
    <div v-show="showLend">
      <form @submit.prevent="lendBook(book.id)">
        <div class="mb-3">
          <label for="username">Millisele kasutajale laenutad raamatu?</label>
          <input type="text" v-model="username" class="form-control" id="username" placeholder="Kasutajatunnus">
        </div>
        <div class="mb-3">
          <label for="username">Mitmeks nädalaks?</label>
          <input type="number" min="1" max="52" v-model="weeks" class="form-control" id="weeks" placeholder="Laenutuse kestvus">
        </div>
        <div class="d-grid gap-2 d-md-block">
          <button class="btn btn-primary float-start" type="submit">Laenuta</button>
          <button class="btn btn-outline-secondary float-end" type="button" @click="cancelLend">Tühista</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import {showForLender, showForBorrower, alertClass} from '../utils';
import axios from 'axios';
import moment from 'moment';

export default {
  name: 'ExpandedBook',
  props: {
    book: Object,
    bookColor: String,
    showAdditional: Boolean
  },
  data() {
    return {
      msg: '',
      alert: "alert alert-primary",
      showLend: false,
      username: '',
      weeks: 4
    }
  },
  computed: {
    bookIsOut() {
      if (this.book.lending === undefined) {
        return false;
      } else return this.book.lending !== null;
    },
    bookIsReserved() {
      if (this.book.reservation === undefined) {
        return false;
      } else return this.book.reservation !== null;
    },
    showForLender,
    showForBorrower
  },
  methods: {
    openLend() {
      this.showLend = true
    },
    async lendBook(id) {
      try {
        const res = await axios.post(`book/${id}/lend`, {
          'borrower': this.username,
          'weeks': this.weeks
        })
        if (res.status === 200) {
            this.book.lending = res.data.user;
            this.book.deadline = res.data.deadline;
          }
        this.alert = alertClass(res.status);
        this.msg = res.data.message;
        this.showLend = false;
        this.book.reservation = null;
      } catch(err) {
        this.alert = alertClass(err.response.status);
        this.msg = err.response.data.message;
      }
      this.username = '';
      this.weeks = 4;
    },
    async borrowBook(id) {
      const res = await axios.post(`book/${id}/borrow`);
      if (res.status === 200) {
        this.book.lending = res.data.user;
        this.book.deadline = res.data.deadline;
      }
      this.alert = alertClass(res.status)
      this.msg = res.data.message;
      this.book.reservation = null;
    },
    async reserveBook(id) {
      const res = await axios.post(`book/${id}/reserve`);
      if (res.status === 200) {
        this.book.reservation = res.data.user;
      }
      this.alert = alertClass(res.status);
      this.msg = res.data.message;
    },
    async returnBook(id) {
      const res = await axios.post(`book/${id}/return`);
      if (res.status === 200) {
          this.book.lending = null;
        }
      this.alert = alertClass(res.status);
      this.msg = res.data.message;
    },
    async cancelReservation(id) {
      const res = await axios.post(`book/${id}/cancel`);
      if (res.status === 200) {
          this.book.reservation = null;
        }
      this.alert = alertClass(res.status);
      this.msg = res.data.message;
    },
    cancelLend() {
      this.showLend = false;
    },
    dateFormat(date) {
      if (date != null) {
        return moment(String(date)).format('DD.MM.YYYY');
      }
    }
  }
}
</script>
<style scoped>
.alert {
  width: 100%;
  margin: 15px 0;
}
</style>