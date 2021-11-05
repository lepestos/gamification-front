<template>
  <section class="black-box-table">
    <table>
      <tr>
        <th colspan="2">&nbsp;</th>
        <th colspan="3" class="black-box-table__header-first-row">Цены лотов</th>
        <th colspan="2">&nbsp;</th>
        <th colspan="3" class="black-box-table__header-first-row">Количества лотов</th>
        <th rowspan="2">Цена BlackBox</th>
      </tr>
      <tr>
        <th colspan="2">Название</th>
        <th>Дешёвый</th>
        <th>Средний</th>
        <th>Дорогой</th>
        <th>Лояльность</th>
        <th>Рентабельность</th>
        <th>Дешёвый</th>
        <th>Средний</th>
        <th>Дорогой</th>
      </tr>
      <tr v-for="box in this.saved_boxes()">
        <td colspan="2">{{box.name}}</td>
        <td><input type="number" v-model="box.lot_cost.cheap" readonly></td>
        <td><input type="number" v-model="box.lot_cost.middle" readonly></td>
        <td><input type="number" v-model="box.lot_cost.costly" readonly></td>
        <td><input type="number" v-model="box.loyalty" readonly></td>
        <td><input type="number" v-model="box.rentability" readonly></td>
        <td><input type="number" v-model="box.lot_amount.cheap" readonly></td>
        <td><input type="number" v-model="box.lot_amount.middle" readonly></td>
        <td><input type="number" v-model="box.lot_amount.costly" readonly></td>
        <td><input type="number" v-model="box.price" readonly></td>
      </tr>
    </table>
    <div class="black-box-table__buttons">
      <button>Факт</button>
      <button>Ретро</button>
    </div>
  </section>
</template>

<script>
import {mapGetters} from "vuex";
import {mapActions} from "vuex";

export default {
  name: "black-box-table",
  methods: {
    ...mapGetters(['saved_boxes']),
    ...mapActions(['loadBlackBoxes'])
  },
  beforeMount() {
    this.loadBlackBoxes()
  }
}
</script>

<style scoped lang="scss">
.black-box-table {
  table{
    border-collapse: collapse;
    width: 90%;
    margin: 0 auto;
    text-align: center;
    th:not(.black-box-table__header-first-row) {
      background-color: #fff;
      font-weight: 400;
      line-height: 24px;
      padding: $similar-element-margin / 2;
    }
    td {
      padding: $similar-element-margin;
    }
    input {
      @extend %standard-input;
      width: 75px;
    }
  }
  &__header-first-row {
    background-color: #fff;
    font-weight: 400;
    line-height: 14px;
    padding-top: $similar-element-margin;
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