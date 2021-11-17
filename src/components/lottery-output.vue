<template>
  <section class="lottery-output">
    <div class="lottery-output__wrapper">
      <div class="lottery-output__left">
        <div class="lottery-output__parameters parameters">
          <h2>Параметры лотереи</h2>
          <span>Количество билетов:</span>
          <input type="number" :value="this.lottery_output_data().ticket_amount.cur" readonly>
          <span>Стоимость проведения:</span>
          <input type="number" :value="this.lottery_output_data().total_cost" readonly>
        </div>
        <div class="lottery-output__profit profit">
          <h2>Выгода от лотереи</h2>
          <span>От:</span>
          <input type="number" :value="this.lottery_output_data().min_profit" readonly>
          <span>До:</span>
          <input type="number" :value="this.lottery_output_data().write_off" readonly>
        </div>
      </div>
      <div class="lottery-output__right">
        <div class="lottery-output__ticket-cost ticket-cost">
          <h2>Стоимость билета</h2>
          <input type="number" :value="this.lottery_output_data().ticket_price.cur" readonly><span>бобров</span>
          <input type="number" :value="this.lottery_output_data().ticket_price.cur !== '' ? (this.lottery_output_data().ticket_price.cur * this.course().bobr_to_rub) : ''" readonly><span>рублей</span>
        </div>
        <div class="lottery-output__rentability rentability">
          <h2>Рентабильность</h2>
          <span>От:</span>
          <input type="number" :value="this.lottery_output_data().min_rentability" readonly>
          <span>До:</span>
          <input type="number" :value="this.lottery_output_data().max_rentability" readonly>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "lottery-output",
  methods: {
    ...mapGetters(['lottery_output_data', 'course'])
  }
}
</script>

<style scoped lang="scss">
.lottery-output {
  &__wrapper {
    display: flex;
    > div {
      flex: 1 1 50%;
    }
    input {
      @extend %standard-input;
    }
  }
  &__profit, &__rentability {
    margin-top: $element-margin;
  }
}

.parameters, .ticket-cost {
  display: grid;
  grid-template-columns: repeat(2, 160px);
  grid-gap: $similar-element-margin;
  h2 {
    grid-column: 1 / 3;
  }
  input {
    width: 160px;
  }
  span {
    line-height: $input-height;
  }
}

.profit, .rentability {
  display: grid;
  grid-template-columns: repeat(2, 30px 60px);
  grid-gap: $similar-element-margin;
  h2 {
    grid-column: 1 / 5;
  }
  input {
    width: 60px;
  }
  span {
    line-height: $input-height;
  }
}
</style>