<template>
  <section class="bingo-discounts-recalculate">
    <form action=""  @submit.prevent="submit()" @reset.prevent="reset()">
      <h2 class="bingo-discounts-recalculate__message">{{message}}</h2>
      <div class="bingo-discounts-recalculate__wrapper">
        <div class="bingo-discounts-recalculate__budget-distribution budget-distribution">
          <span>Цена, Б.</span><h2>Распределение бюджета</h2>
          <template v-for="(price, index) in recalc_data.prices">
            <span class="budget-distribution__price">{{price}}</span>
            <slider-input
                :id_key="`distribution${index}`"
                :min="0"
                :max="1"
                :step="0.01"
                :slider_width="'180px'"
                :has_name="false"
                :value="recalc_data.budget_distribution[index]"
                @input="recalc_data.budget_distribution[index] = $event.target.value"></slider-input>
          </template>
          <span class="budget-distribution__price">Всего:</span><input class="budget-distribution__summar" type="number" :value="recalc_data.budget_distribution.reduce((previousValue, currentValue) => parseFloat(previousValue) + parseFloat(currentValue)).toFixed(2)" readonly>
        </div>
        <div class="bingo-discounts-recalculate__parameters parameters">
          <div class="parameters__wrapper">
            <h2>Ожидаемый бюджет</h2>
            <input type="number" :value="recalc_data.expected_budget"><span>бобров</span>
            <input type="number" :value="recalc_data.expected_budget * this.course().bobr_to_rub"><span>рублей</span>
            <h2>Охват аудитории:</h2>
            <input type="number" :value="recalc_data.total_participants"><span>участников</span>
          </div>
        </div>
        <div class="bingo-discounts-recalculate__unlucky unlucky">
          <slider-input
              :id_key="`unlucky`"
              :min="0"
              :max="0.99"
              :step="0.01"
              :has_name="true"
              :value="recalc_data.unlucky_participants"
              @input="recalc_data.unlucky_participants = $event.target.value">Вероятность неудачи</slider-input>
        </div>
      </div>
      <div class="bingo-discounts-recalculate__buttons buttons">
        <button type="submit">Перерасчёт параметров</button>
        <button type="reset">Вернуться к первому шагу</button>
      </div>
    </form>
  </section>
</template>

<script>
import {mapGetters, mapActions} from "vuex";
import sliderInput from "@/components/slider-input.vue"

export default {
  name: "bingo-recalculate.vue",
  components: {
    sliderInput,
  },
  data() {
    return {
      recalc_data: {
        prices: [],
        budget_distribution: [],
        expected_budget: '',
        total_participants: '',
        unlucky_participants: '',
      },
      message: '',
    }
  },
  methods: {
    ...mapActions(['bingoDiscountsRecalculateParametersClicked', 'bingoDiscountsReset']),
    ...mapGetters(['bingo_discounts_recalculate_data', 'course']),
    async submit() {
      if (this.recalc_data.budget_distribution.reduce((previousValue, currentValue) => parseFloat(previousValue) + parseFloat(currentValue)) <= 1) {
        await this.bingoDiscountsRecalculateParametersClicked(this.recalc_data)
        this.recalc_data = this.bingo_discounts_recalculate_data()
        this.message = ''
      }
      else {
        this.message = 'Суммарное распределение бюджета не может быть больше 1'
      }
    },
    reset() {
      this.bingoDiscountsReset()
    }
  },
  beforeMount() {
    this.recalc_data = this.bingo_discounts_recalculate_data()
  },
}
</script>

<style scoped lang="scss">
  .bingo-discounts-recalculate {
    &__message {
      text-align: center;
      color: red;
    }
    &__wrapper {
      display: flex;
      > div {
        flex: 1 1 33.33%;
      }
    }
    &__buttons {
      margin-top: $section-margin;
    }
    input {
      @extend %standard-input;
    }
  }
  .budget-distribution {
    display: grid;
    grid-template-columns: 100px 300px;
    grid-gap: $similar-element-margin;
    line-height: $input-height;
    text-align: center;
    &__price {
      grid-column: 1 / 2;
    }
    &__summar {
      grid-column: 2 / 3;
      width: 100px;
    }
    .slider-input {
      margin-top: 0;
    }
  }
  .parameters {
    display: flex;
    justify-content: center;
    &__wrapper {
      display: grid;
      grid-template-columns: 100px 80px;
      grid-gap: $similar-element-margin;
      line-height: $input-height;
      text-align: center;
    }
    h2 {
      grid-column: 1 / 3;
    }
    span {
      text-align: left;
    }
  }
  .buttons {
    display: flex;
    justify-content: center;
    align-items: center;
    button {
      margin: 0 $element-margin;
      @extend %standard-button-inactive;
    }
  }
</style>