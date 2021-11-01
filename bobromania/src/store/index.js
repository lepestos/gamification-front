import { createStore } from 'vuex'
import blackBox from "./modules/blackBox";
import converter from "./modules/converter";

export default createStore({
  modules: {
    blackBox,
    converter
  }
})
