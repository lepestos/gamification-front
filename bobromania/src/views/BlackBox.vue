<template>
  <div class="BlackBox">
    <black-box-input :class="{transparent: this.active_half() === 'bottom'}"/>
    <hr>
    <black-box-output :class="{transparent: this.active_half() === 'top'}"/>
    <black-box-recalculate :class="{transparent: this.active_half() === 'top'}"/>
  </div>
</template>

<script>
import blackBoxInput from "../components/black-box-input.vue"
import blackBoxOutput from "../components/black-box-output.vue"
import blackBoxRecalculate from "../components/black-box-recalculate.vue"
import {mapGetters} from 'vuex'
export default {
  name: "BlackBox.vue",
  components: {
    blackBoxInput,
    blackBoxOutput,
    blackBoxRecalculate,
  },
  methods: mapGetters(['active_half'])
}
</script>

<style scoped lang="scss">

section:last-of-type {
  margin-bottom: $section-margin*2;
}

hr {
  height: 3px;
  background-color: $main-green;
  margin-top: $section-margin;
}

.transparent {
  opacity: .3;
}

</style>