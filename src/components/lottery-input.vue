<template>
  <section class="lottery-input">
      <form action="" @submit.prevent="submit()">
        <div class="lottery-input__wrapper">
          <div class="lottery-input__left">
            <div class="lottery-input__lots lots">
              <h2>Количество и стоимость лотов</h2>
              <template v-for="(value, index) in form_input_data.lots">
                <input class="lots__amount" type="number" placeholder="количество" v-model="value.amount" required :disabled="this.lottery_active_half() !== 'top'">
                <input class="lots__price" type="number" placeholder="стоимость" v-model="value.price" required :disabled="this.lottery_active_half() !== 'top'">
                <button class="lots__delete" v-if="index !== 0" @click="deleteLot(index)" :disabled="this.lottery_active_half() !== 'top'"><img src="../assets/img/trash.png" alt=""></button>
              </template>
              <button class="lots__add" type="button" @click="addLot" :disabled="this.lottery_active_half() !== 'top'">Добавить лот</button>
            </div>
          </div>
          <div class="lottery-input__right">
            <div class="lottery-input__write-off write-off">
              <h2>Дополнительное списание</h2>
              <input type="number" placeholder="введите значение" v-model="form_input_data.write_off" required :disabled="this.lottery_active_half() !== 'top'">
            </div>
            <div class="lottery-input__referral referral">
              <h2>Реферальная программа</h2>
              <switch-input
                  :value="form_input_data.referral_on"
                  @change="form_input_data.referral_on = $event.target.checked"
                  :disabled="this.lottery_active_half() !== 'top'"/>
              <template v-if="form_input_data.referral_on">
                <span>Коэффициент:</span>
                <input type="number" placeholder="число" v-model="form_input_data.referral_coeff" required :disabled="this.lottery_active_half() !== 'top'">
                <span>Скидка:</span>
                <input type="number" step="0.01" placeholder="число" v-model="form_input_data.discount" required :disabled="this.lottery_active_half() !== 'top'">
              </template>
            </div>
          </div>
        </div>
        <button type="submit" class="lottery-input__submit" :disabled="this.lottery_active_half() !== 'top'">Рассчитать параметры</button>
      </form>
  </section>
</template>

<script>
import {mapActions, mapGetters} from "vuex";
import switchInput from "@/components/switch-input.vue"

export default {
  name: "lottery-input",
  components: {
    switchInput,
  },
  data() {
    return {
      form_input_data: {
        lots: [{price:'', amount: ''}],
        write_off: '',
        referral_on: false,
        referral_coeff: '',
        discount: '',
      }
    }
  },
  methods: {
    ...mapActions(['lotteryCalculateParametersClicked', 'loadProducts']),
    ...mapGetters(['lottery_active_half', 'products', 'lottery_load_data']),
    addLot() {
      this.form_input_data.lots.push({price:'', amount: ''})
    },
    deleteLot(id) {
      this.form_input_data.lots.splice(id, 1);
    },
    submit() {
      this.lotteryCalculateParametersClicked(this.form_input_data)
    }
  },
  mounted() {
    this.form_input_data = this.lottery_load_data();
  },
}
</script>

<style scoped lang="scss">
  .lottery-input {
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
    &__referral {
      margin-top: $element-margin;
    }
    &__submit {
      @extend %standard-button-active;
      margin-top: $section-margin;
    }
  }
  
  .lots {
    display: grid;
    grid-template-columns: 100px 100px 20px;
    grid-gap: $similar-element-margin;
    align-items: center;
    h2 {
      grid-column: 1 / 4;
    }
    input {
      width: 100px;
    }
    &__amount {
      grid-column: 1 / 2;
    }
    &__price {
      grid-column: 2 / 3;
    }
    &__delete {
      grid-column: 3 / 4;
      cursor: pointer;
    }
    &__add {
      grid-column: 1 / 4;
      @extend %standard-button-inactive;
    }
  }

  .write-off {
    input {
      margin-top: $similar-element-margin;
      width: 160px;
    }
  }

  .referral {
    display: grid;
    grid-template-columns: 100px repeat(3, 60px);
    grid-gap: $similar-element-margin;
    line-height: $input-height;
    h2 {
      grid-column: 1 / 3;
    }
    .switch {
      grid-column: 3 / 5;
    }
    input {
      width: 60px;
    }
  }


</style>