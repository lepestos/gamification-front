<template>
  <section class="bingo-discounts-output">
    <div class="bingo-discounts-output__matrix" :style="{gridTemplateColumns: `1fr repeat(${this.bingo_discounts_output_data().discounts.length + 2}, 100px) 1fr`}">
      <span class="bingo-discounts-output__empty">&nbsp;</span><span class="bingo-discounts-output__price">Цена, Б.</span><span class="bingo-discounts-output__discount" v-for="discount in this.bingo_discounts_output_data().discounts">{{discount}}</span><span>Всего скидок</span>
      <template v-for="(price, index) in this.bingo_discounts_output_data().prices">
        <span class="bingo-discounts-output__empty">&nbsp;</span>
        <span class="bingo-discounts-output__price">{{price}}</span>
        <input type="number" v-for="amount in this.bingo_discounts_output_data().amounts[index]" :value="amount" readonly>
        <input type="number" :value="this.bingo_discounts_output_data().participants_per_lot[index]" readonly>
      </template>
    </div>
  </section>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "bingo-output.vue",
  methods: mapGetters(['bingo_discounts_output_data'])
}
</script>

<style scoped lang="scss">
.bingo-discounts-output {
  &__matrix {
    display: grid;
    grid-gap: $similar-element-margin;
    max-width: 100%;
    line-height: $input-height;
    overflow-x: scroll;
    input {
      @extend %standard-input;
    }
    &::-webkit-scrollbar {
      width: $similar-element-margin;
      background-color: $background-grey;
    }

    &::-webkit-scrollbar-thumb {
      border-radius: $similar-element-margin;
      background-color: $main-green;
    }

    &::-webkit-scrollbar-track {
      border-radius: $similar-element-margin;
      background-color: $background-grey;
    }
  }
  &__empty {
    grid-column: 1 / 2;
  }
  &__price {
    text-align: center;
  }
  &__discount {
    padding-left: $input-padding;
  }
}
</style>