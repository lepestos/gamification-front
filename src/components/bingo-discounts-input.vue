<template>
  <section class="bingo-discounts-input">
    <form action="" @submit.prevent="submit()">
      <div class="bingo-discounts-input__wrapper">
        <div class="bingo-discounts-input__left">
          <div class="bingo-discounts-input__constants constants">
            <h2>Бюджет и количество участников</h2>
            <input type="number" v-model="form_input_data.budget" placeholder="Бюджет">
            <input type="number" v-model="form_input_data.lucky_participants" placeholder="Количество">
          </div>
          <div class="bingo-discounts-input__lots lots">
            <h2>Цены участвующих лотов, Б.</h2>
            <datalist id="lots">
              <option v-for="lot in this.products()" :value="lot.price">{{lot.name}}</option>
            </datalist>
            <input v-for="(price, index) in form_input_data.prices" class="lots__price" type="number"
                   placeholder="стоимость" v-model="form_input_data.prices[index]" min="1" max="9999999999" step="1"
                   required :disabled="this.bingo_discounts_active_half() !== 'top'" list="lots">
            <button class="lots__add" type="button" @click="form_input_data.prices.push('')" :disabled="this.bingo_discounts_active_half() !== 'top'">Добавить лот</button>
          </div>
        </div>
        <div class="bingo-discounts-input__right">
          <div class="bingo-discounts-input__probability probability">
            <h2>Вероятность использования скидки</h2>
            <input type="number" placeholder="Бюджет" value="1" min="0.01" max="1" step="0.01">
          </div>
          <div class="bingo-discounts-input__discounts discounts">
            <h2>Варианты применяемых скидок</h2>
            <input v-for="(discount, index) in form_input_data.discounts" class="discounts__price" type="number"
                   placeholder="скидка" v-model="form_input_data.discounts[index]" min="0" max="1" step="0.01"
                   required :disabled="this.bingo_discounts_active_half() !== 'top'">
            <button class="discounts__add" type="button" @click="form_input_data.discounts.push('')" :disabled="this.bingo_discounts_active_half() !== 'top'">Добавить скидку</button>
          </div>
        </div>
      </div>
      <button type="submit" class="bingo-discounts-input__submit" :disabled="this.bingo_discounts_active_half() !== 'top'">Рассчитать параметры</button>
    </form>
  </section>
</template>

<script>
import {mapGetters, mapActions} from "vuex";

export default {
  name: "bingo-input.vue",
  data() {
    return {
      form_input_data: {
        budget: '',
        lucky_participants: '',
        usage_probability: '',
        prices: [''],
        discounts: ['', ''],
      }
    }
  },
  methods: {
    ...mapGetters(['bingo_discounts_active_half', 'products', 'bingo_discounts_load_data']),
    ...mapActions(['bingoDiscountsCalculateParametersClicked']),
    async submit() {
        await this.bingoDiscountsCalculateParametersClicked(this.form_input_data)
    },
  },
  async mounted() {
    this.form_input_data = this.bingo_discounts_load_data();
  },
}
</script>

<style scoped lang="scss">
  .bingo-discounts-input {
    text-align: center;

    input {
      @extend %standard-input;
    }
    &__wrapper {
      text-align: left;
      display: flex;
      > div {
        flex: 1 1 50%;
      }
    }
    &__submit {
      @extend %standard-button-active;
      margin-top: $section-margin;
    }
    &__lots, &__discounts {
      margin-top: $element-margin;
    }
  }

  .constants, .probability {
    display: grid;
    grid-auto-columns: 100px;
    grid-gap: $similar-element-margin;
    h2 {
      grid-column: 1 / 4;
    }
  }

  .lots, .discounts{
    display: grid;
    grid-auto-columns: 100px;
    grid-gap: $similar-element-margin;
    h2, button {
      grid-column: 1 / 4;
    }
    button {
      @extend %standard-button-inactive;
    }
  }
</style>