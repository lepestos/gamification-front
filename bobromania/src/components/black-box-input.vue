<template>
  <section class="black-box-input">
    <div class="black-box-input__wrapper">
      <div class="black-box-input__left">
        <div class="black-box-input_lot-costs lot-costs">
          <h2>Стоимость лотов</h2>
          <div class="lot-costs__inputs">
            <input type="text" class="lot-costs__cheap" placeholder="Дешёвый" v-model="input_data.lot_cost.cheap">
            <input type="text" class="lot-costs__middle" placeholder="Средний" v-model="input_data.lot_cost.middle">
            <input type="text" class="lot-costs__costly" placeholder="Дорогой" v-model="input_data.lot_cost.costly">
          </div>
        </div>
        <button class="black-box-input__choose-from-showcase">Выбрать лоты с витрины</button>
      </div>
      <div class="black-box-input__right">
        <div class="black-box-input__constants constants">
          <h2>Расчётные константы</h2>
          <div class="constants__inputs">
            <span class="constants__span_two-lines">Целевая лояльность:</span><input type="text" v-model="input_data.loyality">
            <span class="constants__span_one-line">Рентабельность:</span><input type="text" v-model="input_data.rentability">
          </div>
        </div>
        <div class="black-box-input__costly-amount costly-amount">
          <h2>Количество дорогих лотов</h2>
          <input type="text" placeholder="Введите количество" v-model="input_data.costly_amount">
        </div>
      </div>
    </div>
    <button class="black-box-input__calculate-parameters" @click="this.calculateParametersClicked(input_data)">Рассчитать параметры</button>
  </section>
</template>

<script>
import {mapActions} from 'vuex'
export default {
  name: "black-box-input.vue",
  methods: mapActions(['calculateParametersClicked']),
  data() {
    return {
      input_data: {
        lot_cost: {
          cheap: '',
          middle: '',
          costly: '',
        },
        loyality: 0.6,
        rentability: 0.15,
        costly_amount: '',
      }
    }
  }
}
</script>

<style scoped lang="scss">
.black-box-input {
  text-align: center;
  &__wrapper {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
  &__left, &__right {
    text-align: left;
    flex: 1 1 50%;
  }
  &__choose-from-showcase {
    margin-top: $element-margin;
    @extend %standard-button-inactive;
  }
  &__costly-amount {
    margin-top: $element-margin;
  }
  &__calculate-parameters {
    margin-top: $section-margin;
    @extend %standard-button-active;
  }
}

.lot-costs {
  &__inputs {
    margin: $similar-element-margin 0 0 -11px;
    display: flex;
    input {
      flex: 1 1 auto;
      margin: 0 11px;
      max-width: 100px;
      @extend %standard-input;
    }
  }
}

.constants {
  &__inputs {
    margin: $similar-element-margin 0 0 -6px;
    display: flex;
    input, span {
      flex: 1 1 auto;
      margin: 0 6px;
      max-width: 100px;
    }
    input {
      @extend %standard-input;
    }
  }
  &__span {
    &_one-line {
      line-height: $input-height;
    }
    &_two-lines {
      line-height: $input-height / 2;
    }
  }
}

.costly-amount {
  input {
    margin-top: $similar-element-margin;
    @extend %standard-input;
  }
}
</style>