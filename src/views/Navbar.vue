<template>
  <div class="navbar">
    <div class="navbar__wrapper">
      <span class="navbar__logo">БОБРОМАНИЯ</span>
      <ul class="navbar__links">
        <li class="navbar__link">Все товары</li>
        <li class="navbar__link">Сервис</li>
        <li class="navbar__link">Сувениры</li>
        <li class="navbar__link">Рабочее место</li>
        <li class="navbar__link">Ещё</li>
      </ul>
      <div class="navbar__profile">
        <span class="navbar__balance">Ваш баланс:  5 700 <img src="@/assets/img/Bobrocoin_green.png" alt="" class="bobrocoin_green"></span>
        <img src="@/assets/img/shopping-cart.png" alt="" class="navbar__cart">
        <img src="@/assets/img/Avatar.png" alt="" class="navbar__avatar">
      </div>
    </div>
  </div>

</template>

<script>
export default {
  name: "Navbar.vue"
}
</script>

<style scoped lang="scss">
.navbar {
  height: $header-height;
  background-color: #fff;
  text-align: center;
  &__wrapper {
    @extend %width-container;
    display: flex;
    align-items: center;
  }
  &__logo {
    text-align: left;
    line-height: $header-height;
    font-size: 24px;
    font-weight: 800;
    color: $main-green;
    flex: 2 2 auto;
  }
  &__links {
    list-style-type: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex: 9 9 auto;
  }
  &__link {
    flex: 1 1 auto;
    font-size: 16px;
    line-height: $header-height;
  }
  &__profile {
    border-left: 1px solid #D5D5D5;
    flex: 3 3 auto;
    max-width: 30%;
    > img {
      height: 30px;
      margin-left: 25px;
      margin-top: $header-height / 2 - 20;
    }
  }
  &__balance {
    font-size: 14px;
    line-height: $header-height;
    > img {
      height: 16px;
      margin-top: $header-height / 2 - 12;
      margin-left: 10px;
    }
  }
}
</style>