<template>
  <section class="black-box-recalculate">
    <h2 class="black-box-recalculate__error" v-if="recalc_data.message !== ''">{{recalc_data.message}}</h2>
    <form id="recalc" action="" @submit.prevent="submit()" @reset.prevent="reset()">
      <slider-input
          :id_key="'loyalty'"
          :min="0.3"
          :max="0.9"
          :step="0.01"
          :value="recalc_data.loyalty"
          @input="recalc_data.loyalty = $event.target.value"
      >Изменить целевую лояльность</slider-input>
      <slider-input
          :id_key="'rentability'"
          :min="0"
          :max="1"
          :step="0.01"
          :value="recalc_data.rentability"
          @input="recalc_data.rentability = $event.target.value"
      >Изменить целевую рентабельность</slider-input>
      <slider-input
          :id_key="'cost'"
          :min="recalc_data.black_box_cost.min"
          :max="recalc_data.black_box_cost.max"
          :step="10 "
          :value="recalc_data.black_box_cost.cur"
          @input="recalc_data.black_box_cost.cur = $event.target.value"
      >Изменить стоимость Black Box</slider-input>
      <div class="black-box-recalculate__buttons buttons">
        <button type="submit">Перерасчёт параметров</button>
        <button type="reset">Вернуться к первому шагу</button>
      </div>
    </form>
    <form action="" id="save" @submit.prevent="save()">
      <input type="text" placeholder="Название" v-model="name" required>
      <button type="submit">Сохранить расчёт</button>
    </form>
  </section>
</template>

<script>
import {mapGetters} from "vuex";
import {mapActions} from "vuex";
import sliderInput from '@/components/slider-input.vue'

export default {
  name: "black-box-recalculate",
  components: {
    sliderInput
  },
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
        message: '',
      },
      name: '',
    }
  },
  methods: {
    ...mapGetters(['black_box_recalculate_data']),
    ...mapActions(['blackBoxRecalculateParametersClicked', 'blackBoxReset', 'saveBlackBox']),
    async submit() {
      await this.blackBoxRecalculateParametersClicked(this.recalc_data)
      this.recalc_data = this.black_box_recalculate_data()
    },
    reset() {
      this.blackBoxReset()
    },
    save() {
      this.saveBlackBox(this.name)
    }
  },
  beforeMount() {
    this.recalc_data = this.black_box_recalculate_data()
  },
}
</script>

<style scoped lang="scss">
.black-box-recalculate {
  text-align: center;
  &__error {
    color: red
  }
  #recalc {
    display: flex;
    flex-flow: row wrap;
    div:not(.buttons) {
      flex: 1 1 50%;
    }
    .buttons {
      flex: 1 1 50%;
      display: flex;
      justify-content: space-around;
      align-items: center;
      button {
        @extend %standard-button-inactive;
      }
    }
  }
  #save {
    margin-top: $section-margin;
    input {
      @extend %standard-input;
      width: 140px;
      margin-right: 20px;
    }
    button {
      @extend %standard-button-active;
    }
  }
}
</style>