<template>
  <label class="switch">
    <input type="checkbox" name="switch" :checked="value">
    <span class="switch__slider"></span>
  </label>
</template>

<script>
export default {
  name: "switch-input.vue",
  props: ['value']
}
</script>

<style scoped lang="scss">
/* The switch - the box around the slider */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: $input-height;
  input {
    opacity: 0;
    width: 0;
    height: 0;
    &:checked + .switch__slider {
      background-color: $main-green;
      &:before {
        -webkit-transform: translateX(60px - $input-height);
        -ms-transform: translateX(60px - $input-height);
        transform: translateX(60px - $input-height);
      }
    }
    &:focus + .switch__slider {
      box-shadow: 0 0 1px $main-green;
    }
  }
  &__slider {
    border-radius: 34px;
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    -webkit-transition: .4s;
    transition: .4s;
    &:before {
      border-radius: 50%;
      position: absolute;
      content: "";
      height: $input-height - 8;
      width: $input-height - 8;
      left: 4px;
      bottom: 4px;
      background-color: white;
      -webkit-transition: .4s;
      transition: .4s;
    }
  }
}
</style>