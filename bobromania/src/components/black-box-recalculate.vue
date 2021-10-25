<template>
  <section class="black-box-recalculate">
    <form action="" @submit.prevent="submit()">
      <div class="black-box-recalculate__change-loyalty change-loyalty">
        <h2>Изменить целевую лояльность</h2>
        <input type="text" min="0" max="1" step="0.01" v-model="recalc_data.loyalty">
        <input type="range" class="styled-slider slider-progress" min="0" max="1" step="0.01" v-model="recalc_data.loyalty">
      </div>
      <div class="black-box-recalculate__change-rentability change-rentability">
        <h2>Изменить целевую рентабильность</h2>
        <input type="text" min="0" max="1" step="0.01" v-model="recalc_data.rentability">
        <input type="range" class="styled-slider slider-progress" min="0" max="1" step="0.01" v-model="recalc_data.rentability">
      </div>
      <div class="black-box-recalculate__change-cost change-cost">
        <h2>Изменить стоимость Black Box</h2>
        <input type="text"
               v-bind:min="recalc_data.black_box_cost.min"
               v-bind:max="recalc_data.black_box_cost.max"
               v-model="recalc_data.black_box_cost.cur" step="1">
        <input type="range"
               class="styled-slider slider-progress"
               v-bind:min="recalc_data.black_box_cost.min"
               v-bind:max="recalc_data.black_box_cost.max"
               v-model="recalc_data.black_box_cost.cur" step="1">
      </div>
      <div class="black-box-recalculate__button-recalculate button-recalculate">
        <button type="submit">Перерасчёт параметров</button>
      </div>
    </form>
  </section>
</template>

<script>
import {mapGetters} from "vuex";
import {mapActions} from "vuex";

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
  methods: {
    ...mapGetters(['active_half', 'recalculate_data']),
    ...mapActions(['recalculateParametersClicked']),
    async submit() {
      await this.recalculateParametersClicked(this.recalc_data)
    }
  },
  mounted() {
    this.recalc_data = this.recalculate_data()
    for (let e of document.querySelectorAll('input[type="range"].slider-progress')) {
      e.style.setProperty('--value', e.value);
      e.style.setProperty('--min', e.min);
      e.style.setProperty('--max', e.max);
      e.addEventListener('input', () => e.style.setProperty('--value', e.value));
    }
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


/*generated with Input range slider CSS style generator (version 20210711)
https://toughengineer.github.io/demo/slider-styler*/
input[type=range].styled-slider {
  -webkit-appearance: none;
  background-color: $background-grey;
}

/*progress support*/
input[type=range].styled-slider.slider-progress {
  --range: calc(var(--max) - var(--min));
  --ratio: calc((var(--value) - var(--min)) / var(--range));
  --sx: calc(0.5 * 17px + var(--ratio) * (100% - 17px));
}

input[type=range].styled-slider:focus {
  outline: none;
}

/*webkit*/
input[type=range].styled-slider::-webkit-slider-thumb {
  width: 17px;
  height: 17px;
  border-radius: 17px;
  background: #FFFFFF;
  border: 1px solid #7B7B7B;
  box-shadow: none;
  margin-top: calc(max((10px - 1px - 1px) * 0.5,0px) - max(17px * 0.5,1px));
  -webkit-appearance: none;
}

input[type=range].styled-slider::-webkit-slider-runnable-track {
  height: 10px;
  border-radius: 8px;
  background: #FFF;
  border: 1px solid #b2b2b2;
  box-shadow: none;
}
input[type=range].styled-slider:hover::-webkit-slider-runnable-track {
  background: #F3F3F3;
}

input[type=range].styled-slider.slider-progress::-webkit-slider-runnable-track {
  background: linear-gradient(#00A460,#00A460) 0/var(--sx) 100% no-repeat, #FFF;
}

input[type=range].styled-slider.slider-progress:hover::-webkit-slider-runnable-track {
  background: linear-gradient(#00A460,#00A460) 0/var(--sx) 100% no-repeat, #F3F3F3;
}

/*mozilla*/
input[type=range].styled-slider::-moz-range-thumb {
  width: max(calc(17px - 1px - 1px),0px);
  height: max(calc(17px - 1px - 1px),0px);
  border-radius: 17px;
  background: #FFFFFF;
  border: 1px solid #7B7B7B;
  box-shadow: none;
}

input[type=range].styled-slider::-moz-range-track {
  height: max(calc(10px - 1px - 1px),0px);
  border-radius: 8px;
  background: #FFF;
  border: 1px solid #b2b2b2;
  box-shadow: none;
}

input[type=range].styled-slider:hover::-moz-range-track {
  background: #F3F3F3;
}

input[type=range].styled-slider.slider-progress::-moz-range-track {
  background: linear-gradient(#00A460,#00A460) 0/var(--sx) 100% no-repeat, #FFF;
}

input[type=range].styled-slider.slider-progress:hover::-moz-range-track {
  background: linear-gradient(#00A460,#00A460) 0/var(--sx) 100% no-repeat, #F3F3F3;
}

/*ms*/
input[type=range].styled-slider::-ms-fill-upper {
  background: transparent;
  border-color: transparent;
}

input[type=range].styled-slider::-ms-fill-lower {
  background: transparent;
  border-color: transparent;
}

input[type=range].styled-slider::-ms-thumb {
  width: 17px;
  height: 17px;
  border-radius: 17px;
  background: #FFFFFF;
  border: 1px solid #7B7B7B;
  box-shadow: none;
  margin-top: 0;
  box-sizing: border-box;
}

input[type=range].styled-slider::-ms-track {
  height: 10px;
  border-radius: 8px;
  background: #FFF;
  border: 1px solid #b2b2b2;
  box-shadow: none;
  box-sizing: border-box;
}

input[type=range].styled-slider:hover::-ms-track {
  background: #F3F3F3;
}

input[type=range].styled-slider.slider-progress::-ms-fill-lower {
  height: max(calc(10px - 1px - 1px),0px);
  border-radius: 8px 0 0 8px;
  margin: -1px 0 -1px -1px;
  background: #00A460;
  border: 1px solid #b2b2b2;
  border-right-width: 0;
}


</style>