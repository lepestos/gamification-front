<template>
  <div class="black-box">
    <black-box-input :class="{transparent: this.black_box_active_half() !== 'top'}"/>
    <hr>
    <black-box-output :class="{transparent: this.black_box_active_half() !== 'bottom'}"/>
    <transition appear name="fade" v-if="this.black_box_active_half() === 'bottom'">
      <black-box-recalculate/>
    </transition>
    <hr>
    <black-box-table/>
  </div>
</template>

<script>
import blackBoxInput from "../components/black-box-input.vue"
import blackBoxOutput from "../components/black-box-output.vue"
import blackBoxRecalculate from "../components/black-box-recalculate.vue"
import blackBoxTable from "../components/black-box-table.vue"
import {mapGetters} from 'vuex'
import {mapActions} from "vuex"

export default {
  name: "BlackBox.vue",
  components: {
    blackBoxInput,
    blackBoxOutput,
    blackBoxRecalculate,
    blackBoxTable
  },
  methods: {
    ...mapGetters(['black_box_active_half']),
    ...mapActions(['change_active_page'])
  },
  mounted() {
    this.change_active_page('BlackBox')
  }
}
</script>

<style scoped lang="scss">

.fade-enter-active{
  transition: opacity 1s ease;
}
.fade-enter-from{
  opacity: 0;
}

hr {
  @extend %standard-hr;
}

</style>