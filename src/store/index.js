import { createStore } from 'vuex'
import blackBox from "./modules/blackBox";
import lottery from "./modules/lottery";
import page_hat from "./modules/page_hat";
import products from "./modules/products";

export default createStore({
  state: {
    base_url: 'http://localhost:8000/api/v1',
    loading: false,
    loading_requests: 0,
  },
  mutations: {
    changeLoading(state, value) {
      if (value) {
        state.loading_requests++;
        state.loading = true;
      }
      else {
        state.loading_requests--;
        state.loading = state.loading_requests !== 0
      }
    }
  },
  getters: {
    base_url(state) {
      return state.base_url;
    },
    is_loading(state) {
      return state.loading;
    }
  },
  modules: {
    blackBox,
    page_hat,
    lottery,
    products
  }
})
