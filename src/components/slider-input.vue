<template>
  <div class="slider-input">
    <h2><slot></slot></h2>
    <input type="number"
           :step="step"
           :min="min"
           :max="max"
           :value="value">
    <input type="range"
           class="styled-slider slider-progress"
           :id="'slider-' + id_key"
           :step="step"
           :min="min"
           :max="max"
           :value="value">
  </div>
</template>

<script>
export default {
  name: "slider-input.vue",
  props: ['min', 'value', 'max', 'step', 'header', 'id_key'],
  methods: {
    updateSliderColor() {
      let e = document.getElementById('slider-' + this.id_key)
      e.style.setProperty('--value', this.value);
      e.style.setProperty('--min', this.min);
      e.style.setProperty('--max', this.max);
    }
  },
  mounted() {
    this.updateSliderColor();
  },
  updated() {
    this.updateSliderColor();
  }
}
</script>

<style scoped lang="scss">

.slider-input {
  display: grid;
  margin-top: $element-margin;
  grid-template-columns: 100px 300px+$similar-element-margin*2;
  grid-gap: $similar-element-margin;
  grid-auto-rows: $input-height;
  line-height: $input-height;
  h2 {
    grid-column: 1/3;
    text-align: left;
  }
  input[type=number] {
    @extend %standard-input;
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