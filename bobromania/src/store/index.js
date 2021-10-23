import { createStore } from 'vuex'
import blackBox from "./modules/blackBox";

export default createStore({
  modules: {
    blackBox
  }
})
