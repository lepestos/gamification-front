<template>
  <section class="lottery-recalculate">
    <h2 class="lottery-recalculate__error" v-if="recalc_data.message !== ''">{{recalc_data.message}}</h2>
    <form id="recalc" action="" @submit.prevent="submit()" @reset.prevent="reset()">
      <slider-input
          :id_key="'loyalty'"
          :min="recalc_data.ticket_amount.min"
          :max="recalc_data.ticket_amount.max"
          :step="1"
          :value="recalc_data.ticket_amount.cur"
          @input="recalc_data.ticket_amount.cur = $event.target.value"
      >Изменить количество билетов</slider-input>
      <slider-input
          :id_key="'rentability'"
          :min="recalc_data.ticket_price.min"
          :max="recalc_data.ticket_price.max"
          :step="1"
          :value="recalc_data.ticket_price.cur"
          @input="recalc_data.ticket_price.cur = $event.target.value"
      >Изменить стоимость билета</slider-input>
      <div class="lottery-recalculate__buttons buttons">
        <button type="submit">Перерасчёт параметров</button>
        <button type="reset">Вернуться к первому шагу</button>
      </div>
    </form>
    <form action="" id="save" @submit.prevent="save()">
      <h2 class="message">К сожалению, сейчас сохранение недоступно</h2>
      <input type="text" placeholder="Название" v-model="name" required>
      <button type="submit">Сохранить расчёт</button>
    </form>
  </section>
</template>

<script>
import sliderInput from '@/components/slider-input.vue'
import {mapActions, mapGetters} from "vuex";

export default {
  name: "lottery-recalculate.vue",
  components: {
    sliderInput,
  },
  data() {
    return {
      recalc_data: {
        ticket_amount: {
          min: '',
          cur: '',
          max: ''
        },
        ticket_price: {
          min: '',
          cur: '',
          max: ''
        },
        message: '',
      },
      name: '',
    }
  },
  methods: {
    ...mapGetters(['lottery_recalc_data']),
    ...mapActions(['lotteryRecalculateParametersClicked', 'lotteryReset']),
    async submit() {
      await this.lotteryRecalculateParametersClicked(this.recalc_data)
      this.recalc_data = this.lottery_recalc_data()
    },
    reset() {
      this.lotteryReset()
    },
    save() {
      console.log('TO DO')
    }
  },
  beforeMount() {
    this.recalc_data = this.lottery_recalc_data()
  },
}
</script>

<style scoped lang="scss">
.lottery-recalculate {
  text-align: center;
  &__error {
    color: red
  }
}

#recalc {
  display: flex;
  flex-flow: row wrap;
  div:not(.buttons) {
    flex: 1 1 50%;
  }
  .buttons {
    flex: 1 1 100%;
    margin-top: $element-margin;
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

#save {
  margin-top: $section-margin;
  .message {
    color: red;
  }
  input {
    @extend %standard-input;
    width: 140px;
    margin-right: 20px;
  }
  button {
    @extend %standard-button-active;
  }
}
</style>