<template>
  <section class="black-box-recalculate">
    <form action="">
      <div class="black-box-recalculate__change-loyalty change-loyalty">
        <h2>Изменить целевую лояльность</h2>
        <input type="text" min="0" max="1" step="0.01" :disabled="this.active_half() === 'top'" v-model="recalc_data.loyalty">
        <input type="range" min="0" max="1" step="0.01" :disabled="this.active_half() === 'top'" v-model="recalc_data.loyalty">
      </div>
      <div class="black-box-recalculate__change-rentability change-rentability">
        <h2>Изменить целевую рентабильность</h2>
        <input type="text" min="0" max="1" step="0.01" :disabled="this.active_half() === 'top'" v-model="recalc_data.rentability">
        <input type="range" min="0" max="1" step="0.01" :disabled="this.active_half() === 'top'" v-model="recalc_data.rentability">
      </div>
      <div class="black-box-recalculate__change-cost change-cost">
        <h2>Изменить стоимость Black Box</h2>
        <input type="text"
               v-bind:min="recalc_data.black_box_cost.min"
               v-bind:max="recalc_data.black_box_cost.max"
               v-model="recalc_data.black_box_cost.cur" step="1" :disabled="this.active_half() === 'top'">
        <input type="range"
               v-bind:min="recalc_data.black_box_cost.min"
               v-bind:max="recalc_data.black_box_cost.max"
               v-model="recalc_data.black_box_cost.cur" step="1" :disabled="this.active_half() === 'top'">
      </div>
      <div class="black-box-recalculate__button-recalculate button-recalculate">
        <button type="submit">Перерасчёт параметров</button>
      </div>
    </form>
  </section>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "black-box-recalculate",
  data() {
    return {
      recalc_data: {
        loyalty: 0,
        rentability: 0,
        black_box_cost: {
          min: 0,
          cur: 0,
          max: 0
        },
      }
    }
  },
  methods: mapGetters(['active_half', 'recalculate_data']),
  mounted() {
    this.recalc_data = this.recalculate_data()
  }
}
</script>

<style scoped lang="scss">
.black-box-recalculate {
  form {
    display: flex;
    flex-flow: row wrap;

    div:not(.button-recalculate) {
      flex: 1 1 50%;
      display: grid;
      margin-bottom: $element-margin;
      grid-template-columns: 100px 300px+$similar-element-margin*2;
      grid-gap: $similar-element-margin;
      grid-auto-rows: $input-height;
      line-height: $input-height;

      h2 {
        grid-column: 1/3;
      }

      input[type=text] {
        @extend %standard-input;
      }
    }

    .button-recalculate {
      flex: 1 1 50%;
      display: flex;
      justify-content: center;
      align-items: center;

      button {
        @extend %standard-button-active;
      }
    }
  }
}
</style>