<template>
  <div class="lottery">
    <lottery-input :class="{transparent: this.lottery_active_half() !== 'top'}"/>
    <hr>
    <lottery-output :class="{transparent: this.lottery_active_half() !== 'bottom'}"/>
    <transition appear name="fade" v-if="this.lottery_active_half() === 'bottom'">
      <lottery-recalculate/>
    </transition>
  </div>
</template>

<script>
import lotteryInput from "@/components/lottery-input.vue"
import lotteryOutput from "@/components/lottery-output.vue"
import lotteryRecalculate from "@/components/lottery-recalculate.vue"
import {mapGetters} from 'vuex'
import {mapActions} from "vuex";

export default {
  name: "Lottery.vue",
  components: {
    lotteryInput,
    lotteryOutput,
    lotteryRecalculate,
  },
  methods: {
    ...mapGetters(['lottery_active_half']),
    ...mapActions(['change_active_page'])
  },
  mounted() {
    this.change_active_page('Lottery')
  }
}
</script>

<style scoped lang="scss">

hr {
  @extend %standard-hr;
}

</style>