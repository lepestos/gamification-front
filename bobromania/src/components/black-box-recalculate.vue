<template>
  <section class="black-box-recalculate">
    <div class="black-box-recalculate__change-loyality change-loyality">
      <h2>Изменить целевую лояльность</h2>
      <input type="text">
      <input type="range" min="0" max="1" value="0.6" step="0.01">
    </div>
    <div class="black-box-recalculate__change-rentability change-rentability">
      <h2>Изменить целевую рентабильность</h2>
      <input type="text">
      <input type="range" min="0" max="1" value="0.15" step="0.01">
    </div>
    <div class="black-box-recalculate__change-cost change-cost">
      <h2>Изменить стоимость Black Box</h2>
      <input type="text">
      <input type="range" min="20" max="120" value="60" step="10">
    </div>
    <div class="black-box-recalculate__button-recalculate button-recalculate">
      <button>Перерасчёт параметров</button>
    </div>
  </section>
</template>

<script>
export default {
  name: "black-box-recalculate"
}
</script>

<style scoped lang="scss">
.black-box-recalculate {
  display: flex;
  flex-flow: row wrap;
  div:not(.button-recalculate) {
    flex:1 1 50%;
    display: grid;
    margin-bottom: $element-margin;
    grid-template-columns: 100px 300px+$similar-element-margin*2;
    grid-gap: $similar-element-margin;
    grid-auto-rows: $input-height;
    line-height: $input-height;
    h2 {
      grid-column: 1/3;
    }
    input[type=text] {
      @extend %standard-input;
    }
  }
  .button-recalculate {
    flex: 1 1 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    button {
      @extend %standard-button-active;
    }
  }
}
</style>