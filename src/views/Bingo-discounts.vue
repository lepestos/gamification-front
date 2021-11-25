<template>
  <div class="bingo-discounts">
    <bingo-discounts-input :class="{transparent: this.bingo_discounts_active_half() !== 'top'}"/>
    <hr>
    <transition appear name="fade" v-if="this.bingo_discounts_active_half() === 'bottom'">
        <bingo-discounts-output/>
    </transition>
    <transition appear name="fade" v-if="this.bingo_discounts_active_half() === 'bottom'">
        <bingo-discounts-recalculate/>
    </transition>
  </div>
</template>

<script>
import bingoDiscountsInput from "@/components/bingo-discounts-input.vue"
import bingoDiscountsOutput from "@/components/bingo-discounts-output.vue"
import bingoDiscountsRecalculate from "@/components/bingo-discounts-recalculate.vue"
import {mapActions, mapGetters} from "vuex"

export default {
  name: "Bingo.vue",
  components: {
    bingoDiscountsInput,
    bingoDiscountsOutput,
    bingoDiscountsRecalculate,
  },
  methods: {
    ...mapGetters(['bingo_discounts_active_half']),
    ...mapActions(['change_active_page'])
  },
  mounted() {
    this.change_active_page('Bingo-discounts')
  }
}
</script>

<style scoped lang="scss">
.bingo {
  display: flex;
  align-items: center;
  justify-content: center;
  div {
    font-size: 32px;
    color: $main-green;
  }
}
</style>