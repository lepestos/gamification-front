<template>
  <section class="lottery-table">
    <table>
      <tr>
        <th class="lottery-table__header-empty-cell">&nbsp;</th>
        <th class="lottery-table__header-empty-cell" colspan="2" rowspan="2">Название</th>
        <th colspan="2" class="lottery-table__header-first-row">Лоты</th>
        <th colspan="2" class="lottery-table__header-first-row">Реф. программа</th>
        <th colspan="2" class="lottery-table__header-first-row">Выгода</th>
        <th colspan="2" class="lottery-table__header-first-row">Рентабельность</th>
        <th rowspan="2"><div>Количество</div> <div>билетов</div></th>
        <th rowspan="2"><div>Цена</div> <div>билета</div></th>
        <th rowspan="2"><div>Стоимость</div> <div>Лотереи</div></th>
      </tr>
      <tr>
        <th class="lottery-table__header-empty-cell">&nbsp;</th>
        <th>Кол-во</th>
        <th>Стоимость</th>
        <th>Коэф.</th>
        <th>Скидка</th>
        <th>От</th>
        <th>До</th>
        <th>От</th>
        <th>До</th>
      </tr>
      <tr v-if="this.saved_lotteries().length !== 0" v-for="lottery in this.saved_lotteries()" class="lottery-table__row">
        <td><img src="@/assets/img/trash.png" alt="" @click="this.deleteLottery(lottery.id)"></td>
        <td colspan="2">{{lottery.truncated_name}}</td>
        <td><input class="lottery-table__lot-amount" v-for="lot in lottery.lots" type="number" v-model="lot.amount" readonly></td>
        <td><input class="lottery-table__lot-cost" v-for="lot in lottery.lots" type="number" v-model="lot.price" readonly></td>
        <td><input type="number" v-model="lottery.referral_coeff" readonly></td>
        <td><input type="number" v-model="lottery.discount" readonly></td>
        <td><input type="number" v-model="lottery.min_profit" readonly></td>
        <td><input type="number" v-model="lottery.write_off" readonly></td>
        <td><input type="number" v-model="lottery.min_rentability" readonly></td>
        <td><input type="number" v-model="lottery.max_rentability" readonly></td>
        <td><input type="number" v-model="lottery.ticket_amount" readonly></td>
        <td><input type="number" v-model="lottery.ticket_price" readonly></td>
        <td><input type="number" v-model="lottery.total_cost" readonly></td>
      </tr>
      <tr v-else>
        <td colspan="13" class="lottery-table__message-empty">К сожалению, сохранённые Black Box не найдены, создайте новый или повторите попытку позже</td>
      </tr>
    </table>
    <div class="lottery-table__buttons">
      <button>Факт</button>
      <button>Ретро</button>
    </div>
  </section>
</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
  name: "lottery-table.vue",
  methods: {
    ...mapGetters(['saved_lotteries']),
    ...mapActions(['loadLotteries', 'deleteLottery'])
  },
  beforeMount() {
    this.loadLotteries()
  }
}
</script>

<style scoped lang="scss">
.lottery-table {
  table{
    border-collapse: collapse;
    width: 90%;
    margin: 0 auto;
    text-align: center;
    th{
      background-color: #fff;
      font-weight: 400;
      line-height: 24px;
      &:not(.lottery-table__header-first-row) {
        padding: $similar-element-margin / 2;
      }
      &:not(.lottery-table__header-empty-cell) {
        border-left: 1px solid $border-grey;
        border-right: 1px solid $border-grey;
      }
    }
    td {
      padding: $similar-element-margin;
    }
    input {
      @extend %standard-input;
      width: 75px;
    }
    img {
      &:hover {
        cursor: pointer;
      }
    }
  }
  &__header-first-row {
    padding-top: $similar-element-margin;
  }
  &__message-empty{
    color: $main-green;
    line-height: $input-height;
  }
  &__row {
    border-bottom: 1px solid $border-grey;
    &:last-of-type {
      border: none;
    }
  }
  &__lot-amount, &__lot-cost {
    margin-bottom: $similar-element-margin;
    &:last-of-type {
      margin-bottom: 0;
    }
  }
  &__buttons {
    text-align: center;
    margin-top: $section-margin;
    button {
      @extend %standard-button-active;
      margin: 0 20px;
    }
  }
}
</style>