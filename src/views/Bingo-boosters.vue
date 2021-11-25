<template>
  <div class="message">
    Эта вкладка ещё не готова, загляните позже :)
  </div>
</template>

<script>
import {mapActions} from "vuex";

export default {
  name: "Bingo-boosters",
  methods: {
    ...mapActions(['change_active_page'])
  },
  mounted() {
    this.change_active_page('Bingo-boosters')
  }
}
</script>

<style scoped lang="scss">
.message {
  font-size: 32px;
  color: $main-green;
  text-align: center;
}
</style>