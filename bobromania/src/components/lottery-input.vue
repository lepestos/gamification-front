<template>
  <section class="lottery-input">
    <form action="">
      <div class="lottery-input__left">
        <div class="lottery-input__lots">
          <h2>Количество и стоимость лотов</h2>
          <input type="number" placeholder="количество" required>
          <input type="number" placeholder="стоимость" required>
          <button>Добавить лот</button>
        </div>
      </div>
      <div class="lottery-input__right">
        <div class="lottery-input__write-off">
          <h2>Дополнительное списание</h2>
          <input type="number" placeholder="введите значение" required>
        </div>
        <div class="lottery-input__referal">
          <h2>Реферальная программа</h2>
          <span>Коэффициент:</span>
          <input type="number" placeholder="число" required>
          <span>Скидка:</span>
          <input type="number" placeholder="число" required>
        </div>
      </div>
      <button type="submit">Рассчитать параметры</button>
    </form>
  </section>
</template>

<script>
export default {
  name: "lottery-input"
}
</script>

<style scoped lang="scss">
  .lottery-input {
    form {
      display: flex;
      flex-flow: row wrap;
      > div {
        flex: 1 1 50%;
      }
      input {
        @extend %standard-input;
      }
    }
    &__lots {
      input {
        margin-top: $similar-element-margin;
        width: 100px;
        margin-right: 10px;
      }
      button {
        margin-top: $similar-element-margin;
        @extend %standard-button-inactive;
        display: block;
      }
    }
    &__write-off {
      input {
        margin-top: $similar-element-margin;
        width: 160px;
      }
    }
    &__referal {
      margin-top: $element-margin;
      input, span {
        margin-top: $similar-element-margin;
        margin-right: 10px;
      }
      input {
        width: 60px;
      }
    }
  }
</style>