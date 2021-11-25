<template>
  <section class="hat">
    <h1 class="hat__headline">Калькулятор игровых механик</h1>
    <div class="courses">
      <h2>Курс перевода валют</h2>
      <div class="courses__rub-to-bobr">
        <span>1 рубль =</span> <input type="number" placeholder="введите значение" name="rub-to-bobr" v-model="courseInput.rub_to_bobr" @input="rtbchanged()"> <span>бобров</span>
      </div>
      <div class="courses__bobr-to-rub">
        <span>1 бобр =</span> <input type="number" placeholder="введите значение" name="rub-to-bobr" v-model="courseInput.bobr_to_rub" @input="btrchanged()"> <span>рублей</span>
      </div>
      <h2 v-if="message !== ''" class="courses__message">{{message}}</h2>
    </div>
    <ul class="hat__navigation">
      <li class="hat__link" :class="{hat__link_active: this.active_page() === 'BlackBox'}"><router-link to="/BlackBox">Black Box</router-link></li>
      <li class="hat__link" :class="{hat__link_active: this.active_page() === 'Lottery'}"><router-link to="/Lottery">Лотерея</router-link></li>
      <li class="hat__link" :class="{hat__link_active: this.active_page() === 'Bingo-discounts' || this.active_page() === 'Bingo-boosters'}"><router-link to="/Bingo-discounts">Бинго</router-link></li>
    </ul>
    <div class="hat__bingo-tabs" v-if="this.active_page() === 'Bingo-discounts' || this.active_page() === 'Bingo-boosters'">
      <router-link
          :class="{'hat__bingo-tabs_active': this.active_page() === 'Bingo-discounts',
                   'hat__bingo-tabs_inactive': this.active_page() !== 'Bingo-discounts'}"
          to="/Bingo-discounts">Скидки</router-link>
      <router-link
          :class="{'hat__bingo-tabs_active': this.active_page() === 'Bingo-boosters',
                   'hat__bingo-tabs_inactive': this.active_page() !== 'Bingo-boosters'}"
          to="/Bingo-boosters">Бустеры</router-link>
    </div>
  </section>
</template>

<script>
import {mapGetters} from "vuex";
import {mapActions} from "vuex";

export default {
  name: "hat.vue",
  data() {
    return {
      courseInput: {
        rub_to_bobr: 1,
        bobr_to_rub: 1
      },
      message: '',
    }
  },
  methods: {
    ...mapGetters(['course', 'active_page']),
    ...mapActions(['rub_to_bobr_changed', 'bobr_to_rub_changed', 'change_active_page']),
    rtbchanged() {
      if (0.01 <= this.courseInput.rub_to_bobr && this.courseInput.rub_to_bobr <= 100 || this.courseInput.rub_to_bobr == 0) {
        this.rub_to_bobr_changed(this.courseInput.rub_to_bobr)
        this.courseInput.bobr_to_rub = this.course().bobr_to_rub
        this.message = ''
      }
      else {
        this.message = 'Максимальное соотношение 100 к 1!'
      }
    },
    btrchanged() {
      if (0.01 <= this.courseInput.bobr_to_rub && this.courseInput.bobr_to_rub <= 100 || this.courseInput.bobr_to_rub == 0) {
        this.bobr_to_rub_changed(this.courseInput.bobr_to_rub)
        this.courseInput.rub_to_bobr = this.course().rub_to_bobr
        this.message = ''
      }
      else {
        this.message = 'Максимальное соотношение 100 к 1!'
      }
    }
  },
  beforeMount() {
    this.courseInput = this.course()
  },
}
</script>

<style scoped lang="scss">
.hat {
  &__headline {
    font-size: 28px;
    font-weight: 400;
    text-align: center;
  }
  &__courses {
    margin-top: $element-margin;
  }
  &__navigation {
    margin-top: $element-margin;
    list-style-type: none;
    display: flex;
    width: 50%;
    text-align: center;
  }
  &__link {
    flex: 1 1 auto;
    a {
      font-size: 24px;
      color: $main-grey;
    }
    a:hover {
      color: $main-green;
    }
  }
  &__link_active {
    border-bottom: 3px solid $main-green;
    a:hover {
      cursor: default;
      color: $main-grey;
    }
  }
  &__bingo-tabs {
    margin-top: $element-margin;
    display: flex;
    flex-direction: row;
    text-align: center;
    height: $input-height;
    line-height: $input-height;
    &_inactive {
      background-color: rgba(255, 255, 255, 0.2);
      &:hover {
        background-color: rgba(0, 164, 96, 0.05);
        cursor: pointer;
      }
    }
    &_active {
      background-color: rgba(0, 164, 96, 0.2);
      &:hover {
        cursor: default;
      }
    }
    a {
      flex: 1 1 50%;
      color: $main-green;
      display: inline-block;
      width: 100%;

    }
  }
}

.courses {
  h2, span {
    font-weight: 400;
    font-size: 15px;
  }
  span {
    display: inline-block;
    min-width: 65px;
  }
  &__message {
    color: red;
    font-size: 12px;
  }
  &__rub-to-bobr, &__bobr-to-rub {
    margin-top: $similar-element-margin;
  }
  input {
    margin: 0 $similar-element-margin;
    width: 135px;
    @extend %standard-input;
  }
}

</style>