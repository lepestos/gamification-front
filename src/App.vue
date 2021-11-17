<template>
  <navbar></navbar>
  <div class="loader_wrapper" v-if="this.is_loading()">
    <loader/>
  </div>
  <div class="content" :class="{transparent: this.is_loading()}">
    <hat></hat>
    <router-view class="page"/>
  </div>
</template>

<script>
  import Navbar from "./views/Navbar.vue";
  import hat from "./components/hat.vue";
  import loader from "./components/loader.vue"
  import {mapGetters, mapActions} from "vuex";

  export default {
    name: "App.vue",
    components: {
      Navbar,
      hat,
      loader,
    },
    methods: {
      ...mapGetters(['is_loading']),
      ...mapActions(['loadProducts'])
    },
    async mounted() {
      await this.loadProducts();
    }
  }
</script>

<style lang="scss">
/* обнуляющие стили */
*{padding: 0;margin: 0;border: 0;}
*,*:before,*:after{-moz-box-sizing: border-box; -webkit-box-sizing: border-box; box-sizing: border-box;}
:focus,:active{outline: none;}
a:focus,a:active{outline: none;}
nav,footer,header,aside{display: block;}
html,body{height: 100%;width: 100%;line-height: 1;font-size: 15px;-ms-text-size-adjust: 100%;-moz-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;}
input,button,textarea{font-family:inherit;}
input::-ms-clear{display: none;}
button{cursor: pointer;}
button::-moz-focus-inner {padding:0;border:0;}
a, a:visited{text-decoration: none;}
a:hover{text-decoration: none;}
ul li{list-style: none;}
img{vertical-align: top;}
h1,h2,h3,h4,h5,h6{font-size:inherit;font-weight: 400;}
/* обнуляющие стили */

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  -moz-appearance: textfield;
}

.content {
  @extend %width-container;
  section {
    margin-top: $section-margin;
    transition: opacity ease 1s;
  }
  .page {
    margin-top: $section-margin;
  }
}

.transparent {
  transition: all ease 1s;
  opacity: .3;
}

.loader_wrapper {
  position: fixed;
  z-index: 100;
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

#app {
  font-family: Circe;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: $background-grey;
  min-height: 100vh;
}

@font-face {
  font-family: './assets/fonts/Circe/Circe';
  src: url('./assets/fonts/Circe/Circe-Regular.eot');
  src: local('./assets/fonts/Circe/Circe'), local('./assets/fonts/Circe/Circe-Regular'),
  url('./assets/fonts/Circe/Circe-Regular.eot?#iefix') format('embedded-opentype'),
  url('./assets/fonts/Circe/Circe-Regular.woff') format('woff'),
  url('./assets/fonts/Circe/Circe-Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: './assets/fonts/Circe/Circe';
  src: url('./assets/fonts/Circe/Circe-ExtraLight.eot');
  src: local('./assets/fonts/Circe/Circe ExtraLight'), local('./assets/fonts/Circe/Circe-ExtraLight'),
  url('./assets/fonts/Circe/Circe-ExtraLight.eot?#iefix') format('embedded-opentype'),
  url('./assets/fonts/Circe/Circe-ExtraLight.woff') format('woff'),
  url('./assets/fonts/Circe/Circe-ExtraLight.ttf') format('truetype');
  font-weight: 200;
  font-style: normal;
}

@font-face {
  font-family: './assets/fonts/Circe/Circe';
  src: url('./assets/fonts/Circe/Circe-Thin.eot');
  src: local('./assets/fonts/Circe/Circe Thin'), local('./assets/fonts/Circe/Circe-Thin'),
  url('./assets/fonts/Circe/Circe-Thin.eot?#iefix') format('embedded-opentype'),
  url('./assets/fonts/Circe/Circe-Thin.woff') format('woff'),
  url('./assets/fonts/Circe/Circe-Thin.ttf') format('truetype');
  font-weight: 100;
  font-style: normal;
}

@font-face {
  font-family: './assets/fonts/Circe/Circe';
  src: url('./assets/fonts/Circe/Circe-Light.eot');
  src: local('./assets/fonts/Circe/Circe Light'), local('./assets/fonts/Circe/Circe-Light'),
  url('./assets/fonts/Circe/Circe-Light.eot?#iefix') format('embedded-opentype'),
  url('./assets/fonts/Circe/Circe-Light.woff') format('woff'),
  url('./assets/fonts/Circe/Circe-Light.ttf') format('truetype');
  font-weight: 300;
  font-style: normal;
}

@font-face {
  font-family: './assets/fonts/Circe/Circe';
  src: url('./assets/fonts/Circe/Circe-Bold.eot');
  src: local('./assets/fonts/Circe/Circe Bold'), local('./assets/fonts/Circe/Circe-Bold'),
  url('./assets/fonts/Circe/Circe-Bold.eot?#iefix') format('embedded-opentype'),
  url('./assets/fonts/Circe/Circe-Bold.woff') format('woff'),
  url('./assets/fonts/Circe/Circe-Bold.ttf') format('truetype');
  font-weight: bold;
  font-style: normal;
}

@font-face {
  font-family: './assets/fonts/Circe/Circe';
  src: url('./assets/fonts/Circe/Circe-ExtraBold.eot');
  src: local('./assets/fonts/Circe/Circe ExtraBold'), local('./assets/fonts/Circe/Circe-ExtraBold'),
  url('./assets/fonts/Circe/Circe-ExtraBold.eot?#iefix') format('embedded-opentype'),
  url('./assets/fonts/Circe/Circe-ExtraBold.woff') format('woff'),
  url('./assets/fonts/Circe/Circe-ExtraBold.ttf') format('truetype');
  font-weight: 800;
  font-style: normal;
}
</style>
