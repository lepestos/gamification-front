<template>
  <div class="bingo">
    <div>
      Эта страница ещё не готова, но в будущем обязательно появится :)
    </div>
  </div>
</template>

<script>
import {mapActions} from "vuex"

export default {
  name: "Bingo.vue",
  methods: {
    ...mapActions(['change_active_page'])
  },
  mounted() {
    this.change_active_page('Bingo')
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